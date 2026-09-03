"""Exercise the real optional provider adapter through its HTTP transport."""
import base64
from contextlib import contextmanager
from email.message import Message
import http.server
import io
import json
from pathlib import Path
import socket
import sys
import threading
import urllib.error
import urllib.request

from PIL import Image
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'adapters/openai/src'))
import sprite_openai_adapter as adapter


class Response(io.BytesIO):
    def __init__(self, data, request_id='req_local_test'):
        super().__init__(data)
        self.headers = {'x-request-id': request_id}


def case(tmp_path, *, seed_policy='allow_unsupported', params=None, size=(1024,1024)):
    refs = tmp_path/'references';refs.mkdir()
    path = refs/'shape.png';Image.new('RGBA', size, (40,180,240,128)).save(path)
    req = {'request_version':1,'request_id':'demo','adapter':{'id':'openai-images','version':'0.1.0','model':'gpt-image-1',
            'seed_policy':seed_policy,'parameters':params or {}},'items':[{'id':'shape','item_digest':'sha256:'+'1'*64,
            'instruction':'A geometric square','seed':123,'source':{'path':'references/shape.png','sha256':adapter.sha(path.read_bytes())},
            'output':{'width':size[0],'height':size[1]}}]}
    output=tmp_path/'output';output.mkdir()
    response=json.dumps({'data':[{'b64_json':base64.b64encode(path.read_bytes()).decode()}]}).encode()
    return req,output,response


def test_real_adapter_http_construction_and_local_server_response(tmp_path):
    req,out,payload=case(tmp_path)
    observed=[]
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            observed.append((self.path,dict(self.headers),self.rfile.read(int(self.headers['Content-Length']))))
            self.send_response(200);self.send_header('x-request-id','req_local');self.end_headers();self.wfile.write(payload)
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    def local_transport(request,timeout):
        assert request.full_url=='https://api.openai.com/v1/images/edits'
        local=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/v1/images/edits', data=request.data, headers=dict(request.headers),method='POST')
        return urllib.request.urlopen(local,timeout=timeout)
    try: result=adapter.generate(req,tmp_path,out,api_key='local-test-credential',transport=local_transport)
    finally: server.shutdown();server.server_close();thread.join()
    assert result['seed_supported'] is False
    assert result['results'][0]['provider_request_id']=='req_local'
    _,headers,body=observed[0]
    assert headers['Authorization']=='Bearer local-test-credential'
    for fragment in [b'name="image[]"',b'name="model"\r\n\r\ngpt-image-1',b'name="background"\r\n\r\ntransparent',
                     b'name="output_format"\r\n\r\npng',b'name="size"\r\n\r\n1024x1024',b'name="input_fidelity"\r\n\r\nhigh']:
        assert fragment in body
    assert b'name="seed"' not in body
    assert 'local-test-credential' not in json.dumps(result)
    assert (out/'shape.png').read_bytes()==(tmp_path/'references/shape.png').read_bytes()


@pytest.mark.parametrize('status,code', [(401,'PROVIDER_AUTH_FAILED'),(403,'PROVIDER_AUTH_FAILED'),(429,'PROVIDER_RATE_LIMITED'),(400,'PROVIDER_REJECTED'),(500,'PROVIDER_UNAVAILABLE')])
def test_http_errors_are_redacted_and_bounded(tmp_path,status,code):
    req,out,_=case(tmp_path,params={'rate_limit_retries':1})
    calls=[]
    def fail(request,timeout):
        calls.append(1)
        raise urllib.error.HTTPError(request.full_url,status,'secret-canary',{},io.BytesIO(b'secret-canary'))
    with pytest.raises(adapter.AdapterError) as exc:
        adapter.generate(req,tmp_path,out,api_key='secret-canary',transport=fail,sleep=lambda _:None)
    assert exc.value.code==code
    assert 'secret-canary' not in str(exc.value)
    assert len(calls)==(2 if status==429 else 1)
    assert not list(out.iterdir())


def test_rate_limit_retry_can_succeed(tmp_path):
    req,out,data=case(tmp_path,params={'rate_limit_retries':1});calls=[];sleeps=[]
    def transport(request,timeout):
        calls.append(1)
        if len(calls)==1: raise urllib.error.HTTPError(request.full_url,429,'limited',{},io.BytesIO())
        return Response(data)
    assert adapter.generate(req,tmp_path,out,api_key='test',transport=transport,sleep=sleeps.append)['results']
    assert len(calls)==2 and sleeps==[1]


@pytest.mark.parametrize('failure,code',[(socket.timeout,'PROVIDER_TIMEOUT'),(lambda:urllib.error.URLError('secret-canary'),'PROVIDER_UNAVAILABLE')])
def test_unknown_outcome_never_retries(tmp_path,failure,code):
    req,out,_=case(tmp_path,params={'rate_limit_retries':1});calls=[]
    def transport(*a,**k): calls.append(1);raise failure()
    with pytest.raises(adapter.AdapterError) as exc: adapter.generate(req,tmp_path,out,api_key='test',transport=transport)
    assert exc.value.code==code and len(calls)==1


@pytest.mark.parametrize('payload',[b'not json',b'{"data":[]}',b'{"data":[{"url":"https://example.invalid/image.png"}]}',b'{"data":[{"b64_json":"!bad"}]}',b'{"data":[{"b64_json":"bm90IHB uZw=="}]}'])
def test_malformed_image_response(tmp_path,payload):
    req,out,_=case(tmp_path)
    with pytest.raises(adapter.AdapterError): adapter.generate(req,tmp_path,out,api_key='test',transport=lambda *a,**k:Response(payload))
    assert not list(out.iterdir())


@pytest.mark.parametrize('mode,size',[('RGB',(1024,1024)),('RGBA',(8,8))])
def test_provider_must_return_exact_size_and_alpha(tmp_path,mode,size):
    req,out,_=case(tmp_path);stream=io.BytesIO();Image.new(mode,size).save(stream,format='PNG')
    payload=json.dumps({'data':[{'b64_json':base64.b64encode(stream.getvalue()).decode()}]}).encode()
    with pytest.raises(adapter.AdapterError) as exc: adapter.generate(req,tmp_path,out,api_key='test',transport=lambda *a,**k:Response(payload))
    assert exc.value.code=='PROVIDER_OUTPUT_INVALID'


@pytest.mark.parametrize('setting', ['seed','size','credential','params','version'])
def test_unsupported_capabilities_rejected_before_network(tmp_path,setting):
    req,out,_=case(tmp_path,seed_policy='required' if setting=='seed' else 'allow_unsupported',size=(8,8) if setting=='size' else (1024,1024))
    if setting=='params': req['adapter']['parameters']={'seed':42}
    if setting=='version': req['request_version']=True
    with pytest.raises(adapter.AdapterError):
        adapter.generate(req,tmp_path,out,api_key=None if setting=='credential' else 'test',transport=lambda *a,**k:pytest.fail('network called'))


def test_oversized_response_and_secret_request_id(tmp_path,monkeypatch):
    req,out,data=case(tmp_path)
    monkeypatch.setattr(adapter,'MAX_RESPONSE',2)
    with pytest.raises(adapter.AdapterError) as exc: adapter.generate(req,tmp_path,out,api_key='test',transport=lambda *a,**k:Response(data))
    assert exc.value.code=='PROVIDER_INVALID_RESPONSE'
    monkeypatch.setattr(adapter,'MAX_RESPONSE',48*1024*1024)
    result=adapter.generate(req,tmp_path,out,api_key='secret-canary',transport=lambda *a,**k:Response(data,'secret-canary'))
    assert result['results'][0]['provider_request_id'] is None


def test_redirects_do_not_forward_credentials():
    request=urllib.request.Request('https://api.openai.com/v1/images/edits',headers={'Authorization':'Bearer test'})
    assert adapter._NoRedirect().redirect_request(request,None,302,'moved',{},'https://other.invalid') is None


def test_interrupted_download_maps_unknown_outcome_without_retry(tmp_path):
    import http.client
    req,out,_=case(tmp_path,params={'rate_limit_retries':1});calls=[]
    class Interrupted(Response):
        def read(self,*args):raise http.client.IncompleteRead(b'partial')
    def transport(*a,**k):calls.append(1);return Interrupted(b'')
    with pytest.raises(adapter.AdapterError) as exc:adapter.generate(req,tmp_path,out,api_key='test',transport=transport)
    assert exc.value.code=='PROVIDER_UNAVAILABLE' and len(calls)==1

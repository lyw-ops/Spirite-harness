"""Packaging parity and strict duplicate/nonfinite boundaries."""
import json
from pathlib import Path

import jsonschema
import pytest
from sprite_harness.contracts import read_json, schema_document
from sprite_harness.spec import SpecLoadError

ROOT=Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('name',['generation-spec','generation-request','generation-response','generated-inputs','export-spec','export-config','atlas'])
def test_packaged_schemas_match_canonical_schemas(name):
    schema=json.loads((ROOT/'schemas'/f'{name}.schema.json').read_text())
    assert schema_document(name)==schema
    jsonschema.Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize('value',['{"generation_version":1,"generation_version":1}', '{"value":NaN}', '{"value":Infinity}', '{"value":1e9999}'])
def test_strict_json_loader(tmp_path,value):
    p=tmp_path/'spec.json';p.write_text(value)
    with pytest.raises(SpecLoadError):read_json(p)


@pytest.mark.parametrize('args',[['export','--json'],['generate','b','--timeout','bad','--json'],['unknown','--json']])
def test_json_cli_argument_errors_remain_json(capsys,args):
    from sprite_harness.cli import main
    assert main(args)==2
    captured=capsys.readouterr()
    assert not captured.err
    assert json.loads(captured.out)['errors'][0]['code']=='MALFORMED_COMMAND'

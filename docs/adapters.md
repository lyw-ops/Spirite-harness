# External generation adapters

The core has no provider SDK, prompt template, credential lookup or network
client. `generate` alone executes the explicitly supplied JSON argv array with
`shell=False`. It appends `--request ABS_FILE --response ABS_FILE --output
ABS_DIRECTORY`. The request is generation-request v1; the response is
generation-response v1. All reference PNGs and spec.json are copied beside
request.json before invocation, so their paths resolve correctly both while
staging and after publication. No original source path is needed by an adapter.

An adapter must write a new response file and direct-child candidate files
within the supplied output directory. Every result echoes its item id/digest
and declares candidate id, filename, SHA-256, width, height and a nullable
provider request id. Only one candidate per item is accepted; the item's
explicit frames array defines reuse. The core checks every result before
copying candidates into managed inputs. Response order is not mapping order.
Response files are bounded to 4 MiB, each PNG to 32 MiB, each dimension to
16384, and the generation set to 256 items / 64 million pixels. The process
output quota is 256 MiB. Stdout/stderr are discarded, never copied into QA or
exceptions. A default 120-second whole-process deadline (explicit override up
to 3600) kills/reaps the process group, including children. Core retries: zero.
Executables are explicitly trusted local code, not sandboxed by this protocol.

Success means candidates passed structural/integrity checks. No semantic or
quality judgment is claimed. On failure an adapter may write only
`{"error_code":"PROVIDER_TIMEOUT"}` and exit nonzero. The core returns only
allowlisted error codes, never adapter-supplied exception text. Missing/malformed
contracts use exits 3/2; integrity/semantic failures 1; process/provider failures
4. See generation.py for the small stable allowlist.

## Offline test substitute

```bash
sprite-harness generate build/demo --spec generation.json \
  --adapter-argv '["/absolute/python", "/absolute/repo/scripts/offline_test_adapter.py"]'
sprite-harness render build/demo --generated-input
sprite-harness validate build/demo --write-qa
```

The programmatic geometric adapter is a **test substitute**, not real AI.
It intentionally returns results in reverse order to exercise explicit mapping.
It has no network behavior or provider dependencies.

## Optional real OpenAI adapter (outside core)

Install separately with the same Python environment:

```bash
python -m pip install ./adapters/openai
```

Set the credential through the explicit `OPENAI_API_KEY` environment variable
in your local secret manager or shell. Never put a key in argv, parameters,
plans, response JSON, logs, QA, or Git. The adapter does not scan env files or
auto-select a provider. Before a live run, authorize the paid request and upload
of the chosen source PNG; the supplied smoke script requires an explicit flag.

Select `adapter.id: openai-images`, `version: 0.1.0`, `model: gpt-image-1`,
`seed_policy: allow_unsupported`. Parameters are optional `quality` (`medium`
or `high`, default medium), `input_fidelity` (`high` or `low`, default high),
`timeout_seconds` (0 < value <= 300, default 90) and `rate_limit_retries`
(0 or 1, default 0). Unknown parameters are rejected before network access.
These defaults are part of adapter version 0.1.0. Only existing sources of
1024x1024, 1024x1536 or 1536x1024 pixels are supported. Tiny example sprites
are explicitly refused; the adapter never resizes or fabricates transparency.

The adapter uses authenticated HTTPS multipart POST to the official image edit
endpoint with the original reference image, explicit prompt, native size,
`n=1`, PNG output and transparent background. It decodes the base64 image
response, validates size/alpha/PNG before writing, and captures sanitized
`x-request-id` when available. The response-body bound is 48 MiB; output PNG
bound is 32 MiB. URL image responses are rejected and HTTP redirects are disabled so credentials
and source artwork are never forwarded to a redirect destination.
These capabilities were checked against the official
[image edit API reference](https://developers.openai.com/api/reference/resources/images/methods/edit)
and [image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
on 2026-09-03. The chosen endpoint documents no seed parameter, so the adapter
reports seed unsupported and sends no seed. Transparency is requested and
verified as a channel; neither alpha presence nor hashes prove artistic quality.

Authentication failures map to PROVIDER_AUTH_FAILED; 429 to
PROVIDER_RATE_LIMITED; timeout to PROVIDER_TIMEOUT; 5xx/connectivity to
PROVIDER_UNAVAILABLE; other HTTP rejection to PROVIDER_REJECTED; malformed
JSON/base64 to PROVIDER_INVALID_RESPONSE; invalid PNG/size/alpha to
PROVIDER_OUTPUT_INVALID. With retries=1 only a 429 may be retried once after
one second. Timeouts, disconnects and 5xx can have unknown paid outcomes and
are never automatically retried. Raw error bodies, headers and exception text
are not returned or persisted. Output collisions fail instead of overwriting.

The local test suite exercises the **real adapter implementation**, including a
loopback HTTP service, multipart construction, success decoding, timeouts,
429 retries, malformed output and credential redaction. This is transport
verification, not proof that a live model call succeeded.

**Live provider acceptance is not completed:** this session had no credential
and no authorization for a paid call/source upload. The rest of M4/M5 is
independently testable offline. The remaining optional live command is:

```bash
python scripts/live_provider_smoke.py --output build/live-smoke --authorize-paid-call
```

This draws an original 1024x1024 geometric source, uses the installed real
adapter, and performs generation/render/validate/export/validate-export. It
requires `OPENAI_API_KEY` and saves a redacted command log. A fresh directory is
required. It does not promise byte-identical outputs across model invocations.

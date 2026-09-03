# Optional OpenAI image edit adapter

This is a separate installable Python distribution, outside the harness core.
Install with `python -m pip install ./adapters/openai`, then use the
`sprite-openai-adapter` executable as explicit generate argv.

See [the complete adapter contract](../../docs/adapters.md) for credentials,
capabilities, limits, error mapping, retry behavior and live acceptance status.
The main harness never imports this package or calls a model implicitly.

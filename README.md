# Minder plugin template

A starter for building a [**Minder**](https://github.com/minderhq/minder) plugin,
wired against the [**plugin-sdk**](https://github.com/minderhq/plugin-sdk).

> Click **“Use this template”** on GitHub to create your own repo from this one.

## What you get

- [`plugin.py`](plugin.py) — a working `PluginBase` plugin with `DISPLAY`,
  `REQUIRES`, a `CONFIG_SCHEMA` (rendered as a form in the client), and a
  `collect_data` stub to fill in.
- [`tests/test_plugin.py`](tests/test_plugin.py) — contract tests using the SDK's
  `check_plugin` / `run_lifecycle` harness.
- CI that lints, runs `minder-plugin validate`, and tests on every push.

## Quick start

```bash
pip install -e ".[dev]"          # installs the plugin-sdk (from git) + tooling

minder-plugin validate plugin.py # does your plugin honour the contract?
minder-plugin inspect  plugin.py # capabilities, config schema, requirements
pytest -q                        # run the contract tests
```

Then:

1. Rename `plugin.py` / the `TemplatePlugin` class and update the `register()`
   metadata (`name`, `version`, `description`, `author`).
2. Implement `collect_data()` (and/or add `ACTIONS` + `AI_TOOLS`). For HTTP, add
   `httpx` to `dependencies` in `pyproject.toml`.
3. Declare what you need in `REQUIRES` and how your config renders via each
   field's `widget` (see the SDK's
   [plugin-driven UI](https://github.com/minderhq/plugin-sdk#plugin-driven-ui-the-plugin-owns-its-presentation)).
4. Keep `pytest` green and open a PR to
   [`minderhq/plugins`](https://github.com/minderhq/plugins) to publish it.

## Scaffold from the CLI instead

The SDK ships a generator, if you'd rather start from nothing:

```bash
pip install "git+https://github.com/minderhq/plugin-sdk"
minder-plugin scaffold my-plugin
```

## License

Apache-2.0 — change it to whatever suits your plugin.

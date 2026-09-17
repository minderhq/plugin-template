# Examples: two plugin shapes

Minder plugins come in two shapes, and picking the right one first saves a
rewrite. The [runtime-plugin-loading ADR][adr] (Recommendation point 2) is
explicit: **third-party plugins are _installed_, not compiled in, and run no
arbitrary uploaded code.** So if you are a third party integrating an external
system, reach for the **manifest + webhook** shape below; write an **in-process
code plugin** only when the behaviour is genuinely first-party and must run
inside the platform.

## 1. Manifest + webhook (the third-party default)

Files here:

- [`webhook_manifest.yaml`](webhook_manifest.yaml) — a declarative manifest that
  tells Minder to expose an inbound webhook path and pipe each delivery into the
  vector store. **No code is compiled into the platform** and it **installs at
  runtime**. Your third-party code (if any) runs on _your_ own infra and is
  reached via this webhook.
- [`webhook_plugin.py`](webhook_plugin.py) — an optional, tiny `handle_webhook`
  stub for when the declarative `store-vector` mapping isn't enough and a payload
  must be reshaped before storing. It documents the exact request/response
  contract:

  | Direction | Shape |
  |-----------|-------|
  | **request** (Minder → handler) | the parsed JSON body of the webhook, as a `dict`. Minder verifies the secret named by `spec.trigger.webhook.secretRef` **before** calling. |
  | **response** (handler → Minder) | the record to store — `{"text": <str>, "metadata": <dict>}`, matching `spec.action.store.input`. Return `{}` to acknowledge but store nothing. |

Validate the manifest the same way CI does:

```bash
minder-plugin validate examples/webhook_manifest.yaml
```

## 2. In-process code plugin (first-party only)

The [`../plugin.py`](../plugin.py) at the repo root is the code-plugin shape: a
Python class the registry loads and drives through a lifecycle, running **inside**
the platform. Because it runs in-process it is built into a Minder deployment and
reviewed — it is not something a third party uploads and Minder executes.

## See also

- The SDK's decision guide with a worked example of each shape:
  [`minderhq/plugin-sdk` › `docs/plugins/webhook-vs-code-plugin.md`][guide].
- [runtime-plugin-loading ADR][adr] — the recommendation this example mirrors.

[adr]: https://github.com/minderhq/adrs/blob/main/decisions/runtime-plugin-loading.md
[guide]: https://github.com/minderhq/plugin-sdk/blob/main/docs/plugins/webhook-vs-code-plugin.md

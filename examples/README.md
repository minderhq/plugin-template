# Examples: two plugin shapes

Minder plugins come in two shapes, and picking the right one first saves a
rewrite. the [SDK decision guide][guide] has the details.
A plugin is either **reviewed Python code**, merged to the catalog by pull
request, or a **declarative manifest** that runs no plugin code. Both run
isolated, out of process, in a `plugin-runner`, and no user-uploaded code runs.
AI tools declare an `effect`, and write/send/destructive ones pause for user
approval. If you are integrating an external system, start with the
**manifest + webhook** shape below; write a **code plugin** when you need Python
logic.

## 1. Manifest + webhook (the third-party default)

Files here:

- [`webhook_manifest.yaml`](webhook_manifest.yaml) — a declarative manifest that
  tells Minder to expose an inbound webhook path and pipe each delivery into the
  vector store. **It runs no plugin code** and it **installs at
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

## 2. Code plugin (reviewed, merged by pull request)

The [`../plugin.py`](../plugin.py) at the repo root is the code-plugin shape: a
Python class the registry drives through a lifecycle, hosted by a `plugin-runner`
(isolated, out of process). It is reviewed and merged into the catalog by pull
request — it is not something a user uploads and Minder executes.

## See also

- The SDK's decision guide with a worked example of each shape:
  [`minderhq/plugin-sdk` › `docs/plugins/webhook-vs-code-plugin.md`][guide].

[guide]: https://github.com/minderhq/plugin-sdk/blob/main/docs/plugins/webhook-vs-code-plugin.md

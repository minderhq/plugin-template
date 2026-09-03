"""My Minder plugin.

Rename this file, the class, and the metadata below, then implement
``collect_data`` (and/or add actions / AI tools). See the reference:
https://github.com/minderhq/plugin-sdk (examples/weather_plugin.py).
"""

from minder_plugin_sdk import PluginBase, PluginMetadata

__all__ = ["TemplatePlugin"]


class TemplatePlugin(PluginBase):
    # ── how the client renders this plugin's card (optional) ──────────────────
    DISPLAY = {
        "label": "Template",
        "summary": "A starter plugin — replace me.",
        "logo": "puzzle",  # a lucide icon name
        "color": "#6366f1",
        "category": "data-source",
    }

    # ── what this plugin needs from the platform (optional) ───────────────────
    # e.g. {"services": ["influxdb"], "bundles": ["rag"]}
    REQUIRES: dict[str, list[str]] = {
        "services": [],
        "optional_services": [],
        "bundles": [],
    }

    # ── runtime-editable config, rendered as a form in the client (optional) ──
    CONFIG_SCHEMA = [
        {
            "key": "TEMPLATE_GREETING",
            "type": "string",
            "default": "hello",
            "description": "An example setting.",
            "widget": "text",
            "group": "General",
        },
        {
            "key": "TEMPLATE_ENABLED",
            "type": "bool",
            "default": True,
            "description": "Toggle an example flag.",
            "widget": "toggle",
            "group": "General",
        },
    ]

    async def register(self) -> PluginMetadata:
        return PluginMetadata(
            name="template",
            version="0.1.0",
            description="A starter Minder plugin — replace this.",
            author="you",
            capabilities=["collect"],
        )

    async def collect_data(self) -> dict:
        # TODO: fetch/produce your data here. This runs on the registry's hourly
        # loop and on a manual /collect. For HTTP, add ``httpx`` to your deps:
        #
        #   import httpx
        #   async with httpx.AsyncClient(timeout=10) as client:
        #       resp = await client.get("https://example.com/api")
        #       data = resp.json()
        #
        self._last = {"greeting": getattr(self, "template_greeting", "hello")}
        return self._last

    # ── OR make it a "Talent": an AI tool the LLM can call ────────────────────
    # A plugin doesn't have to collect data — it can expose a capability the model
    # calls by name (function-calling). That's a "Talent", the unit the
    # marketplace sells. To turn this into one, uncomment the block below (and set
    # DISPLAY["category"] = "ai-tool"), then delete collect_data if you don't need
    # a stored series:
    #
    #     ACTIONS = frozenset({"greet"})
    #     READ_ONLY_ACTIONS = frozenset({"greet"})  # reachable via GET, unauth
    #     AI_TOOLS = [
    #         {
    #             "name": "greet",
    #             "description": "Greet someone by name.",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {"name": {"type": "string"}},
    #                 "required": ["name"],
    #             },
    #             "action": "greet",   # must name a method below (in ACTIONS)
    #             "method": "GET",
    #         },
    #     ]
    #
    #     async def greet(self, name: str) -> dict:
    #         return {"message": f"Hello, {name}!"}

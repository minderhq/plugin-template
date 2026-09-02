"""Contract tests for the plugin — powered by the SDK's test harness.

``check_plugin`` returns an empty list when the plugin honours the contract;
``run_lifecycle`` drives register → collect_data → … the way the registry does.
"""

import asyncio
import sys
from pathlib import Path

from minder_plugin_sdk import PluginMetadata, check_plugin, run_lifecycle

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from plugin import TemplatePlugin  # noqa: E402


def test_plugin_honours_the_contract():
    assert check_plugin(TemplatePlugin()) == []


def test_lifecycle_runs():
    out = asyncio.run(run_lifecycle(TemplatePlugin()))
    assert isinstance(out["metadata"], PluginMetadata)
    assert out["health_check"]["healthy"] is True
    assert "greeting" in out["collect_data"]

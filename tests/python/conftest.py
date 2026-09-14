"""Shared fixtures for the Python test suite.

Tests that need an external tool (zola, majordomus, an authenticated gh) skip when the tool is
missing locally. CI sets CAAS_REQUIRE_TOOLS=1 so that a missing tool fails instead of skipping,
which keeps every command registry entry genuinely verified.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def require_tool(name, probe=None):
    available = shutil.which(name) is not None
    if available and probe:
        available = subprocess.run(probe, cwd=ROOT, capture_output=True).returncode == 0
    if available:
        return
    message = f"{name} is not available"
    if os.environ.get("CAAS_REQUIRE_TOOLS") == "1":
        pytest.fail(message)
    pytest.skip(message)


def run(args, cwd=ROOT, env=None, timeout=600, check=False):
    merged = {**os.environ, **(env or {})}
    result = subprocess.run(args, cwd=cwd, env=merged, capture_output=True, text=True, timeout=timeout)
    if check and result.returncode != 0:
        raise AssertionError(f"{args} exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


@pytest.fixture
def root():
    return ROOT


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path

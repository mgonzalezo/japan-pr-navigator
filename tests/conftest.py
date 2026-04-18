import shutil
from pathlib import Path

import pytest

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


@pytest.fixture
def knowledge_dir() -> Path:
    """Return the path to the real knowledge directory."""
    return KNOWLEDGE_DIR


@pytest.fixture
def tmp_knowledge_dir(tmp_path: Path) -> Path:
    """Copy real knowledge files to a temp directory for isolated tests."""
    dest = tmp_path / "knowledge"
    shutil.copytree(KNOWLEDGE_DIR, dest)
    return dest


@pytest.fixture
def empty_knowledge_dir(tmp_path: Path) -> Path:
    """Return an empty temp directory (no YAML files)."""
    d = tmp_path / "empty_knowledge"
    d.mkdir()
    return d

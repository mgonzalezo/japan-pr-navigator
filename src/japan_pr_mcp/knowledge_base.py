"""Loads and indexes the YAML knowledge base."""

from __future__ import annotations

import copy
import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

KBEntry = dict[str, Any]


class KnowledgeBase:
    """Immutable, indexed access to the Japan PR knowledge YAML files."""

    def __init__(
        self,
        documents: list[KBEntry],
        phases: list[KBEntry],
        hsp_table: KBEntry,
        offices: list[KBEntry],
        tips: list[KBEntry],
        faq: list[KBEntry],
    ) -> None:
        self._documents = documents
        self._phases = phases
        self._hsp_table = hsp_table
        self._offices = offices
        self._tips = tips
        self._faq = faq

    @classmethod
    def load(cls, path: Path) -> KnowledgeBase:
        if not path.exists():
            raise FileNotFoundError(f"Knowledge directory not found: {path}")

        return cls(
            documents=_load_list(path / "documents.yaml", "documents"),
            phases=_load_list(path / "phases.yaml", "phases"),
            hsp_table=_load_dict(path / "hsp_points.yaml", "hsp_points"),
            offices=_load_list(path / "offices.yaml", "offices"),
            tips=_load_list(path / "tips.yaml", "tips"),
            faq=_load_list(path / "faq.yaml", "faq"),
        )

    def get_documents(self) -> list[KBEntry]:
        return copy.deepcopy(self._documents)

    def get_phases(self) -> list[KBEntry]:
        return copy.deepcopy(self._phases)

    def get_hsp_table(self) -> KBEntry:
        return copy.deepcopy(self._hsp_table)

    def get_offices(self) -> list[KBEntry]:
        return copy.deepcopy(self._offices)

    def get_tips(self) -> list[KBEntry]:
        return copy.deepcopy(self._tips)

    def get_faq(self) -> list[KBEntry]:
        return copy.deepcopy(self._faq)

    def get_document_by_id(self, doc_id: int) -> KBEntry | None:
        for doc in self._documents:
            if doc["id"] == doc_id:
                return copy.deepcopy(doc)
        return None

    def get_phase_by_number(self, phase: int) -> KBEntry | None:
        for p in self._phases:
            if p["phase"] == phase:
                return copy.deepcopy(p)
        return None

    def get_offices_by_prefecture(self, prefecture: str) -> list[KBEntry]:
        needle = prefecture.lower()
        return copy.deepcopy(
            [o for o in self._offices if o["prefecture"].lower() == needle]
        )

    def get_tips_by_category(self, category: str) -> list[KBEntry]:
        return copy.deepcopy(
            [t for t in self._tips if t["category"] == category]
        )

    def search_faq(self, query: str) -> list[KBEntry]:
        needle = query.lower()
        results: list[KBEntry] = []
        for entry in self._faq:
            parts = [entry['question'], entry['answer'], ' '.join(entry.get('tags', []))]
            searchable = ' '.join(parts).lower()
            if needle in searchable:
                results.append(copy.deepcopy(entry))
        return results


def _load_list(file: Path, key: str) -> list[KBEntry]:
    data = _safe_load_yaml(file)
    if isinstance(data, dict) and key in data:
        val = data[key]
        return val if isinstance(val, list) else []
    return []


def _load_dict(file: Path, key: str) -> KBEntry:
    data = _safe_load_yaml(file)
    if isinstance(data, dict) and key in data:
        val = data[key]
        return val if isinstance(val, dict) else {}
    return {}


def _safe_load_yaml(file: Path) -> Any:
    if not file.exists():
        return None
    try:
        with file.open() as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        logger.warning("Failed to parse YAML: %s", file)
        return None

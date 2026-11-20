"""Verify that coupled CodeQL actions stay on one immutable release."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

CODEQL_REFERENCE = re.compile(
    r"(?m)(?:^\s*(?:-\s*)?|\{\s*|,\s*)['\"]?uses['\"]?\s*:\s*['\"]?"
    r"github/codeql-action/([^@\s'\"]+)@([^\s'\"}#,]+)"
)


class CodeQLPinTests(unittest.TestCase):
    """Reject independent component updates and mutable CodeQL references."""

    def test_one_immutable_release(self) -> None:
        """Require init, analyze, and any other CodeQL actions to share a commit."""
        directory = Path(__file__).resolve().parents[1] / ".github/workflows"
        files = [*directory.glob("*.yaml"), *directory.glob("*.yml")]
        references = CODEQL_REFERENCE.findall("\n".join(path.read_text() for path in files))
        self.assertTrue({"init", "analyze"} <= {name for name, _ in references})
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", ref) for _, ref in references))
        self.assertEqual(len({ref for _, ref in references}), 1)

    def test_flow_mapping_reference_is_detected(self) -> None:
        """Include CodeQL references written in YAML flow mappings."""
        self.assertEqual(
            CODEQL_REFERENCE.findall("- {uses: github/codeql-action/upload-sarif@v4}"),
            [("upload-sarif", "v4")],
        )

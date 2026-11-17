"""Check that extra CMake arguments cannot expand target-controlled filenames."""

from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


class ExtraOptionsTests(unittest.TestCase):
    """Use a mock CMake function instead of executing build configuration."""

    def test_filename_expansion_is_disabled(self) -> None:
        """Keep whitespace-separated option semantics without shell glob expansion."""
        action = (Path(__file__).parents[1] / "action.yaml").read_text()
        script = textwrap.dedent(
            action.split("        # Add extra options\n")[1].split(
                '        echo "Source directory:'
            )[0]
        )
        helpers = 'CMAKE_ARGS=(); cmake() { printf "<%s>\\n" "$@"; };\n'
        with tempfile.TemporaryDirectory(prefix="cmake-options-test-") as tmp:
            (Path(tmp) / "-DNAME=unexpected").write_text("data\n")
            for value, succeeds in [("-DNAME=* -DOTHER=1", True), ("-DX=1\n-DY=2", False)]:
                result = subprocess.run(
                    ["bash", "-e", "-c", helpers + script],
                    cwd=tmp,
                    capture_output=True,
                    text=True,
                    env={"PATH": os.environ["PATH"], "EXTRA_OPTIONS": value},
                )
                self.assertEqual(result.returncode == 0, succeeds, result.stderr)
                if succeeds:
                    self.assertIn("<-DNAME=*>", result.stdout)
                    self.assertNotIn("unexpected", result.stdout)


if __name__ == "__main__":
    unittest.main()

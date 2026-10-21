
import re
import subprocess
import sys


class CodeQualityChecker:
    def check(self, filepath):
        issues = []

        result = subprocess.run(
            [sys.executable, "-m", "flake8", filepath],
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines():
            match = re.match(
                r"^(.+):(\d+):(\d+):\s*(.*)$",
                line
            )

            if not match:
                continue

            issues.append({
                "type": "Lint Issue",
                "message": match.group(4),
                "lineno": int(match.group(2)),
                "col_offset": int(match.group(3))
            })

        return issues

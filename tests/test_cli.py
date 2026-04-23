import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from cli_assistant.cli import run


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.storage = str(Path(self.tmpdir.name) / "tasks.json")

    def tearDown(self):
        self.tmpdir.cleanup()

    def _run(self, args):
        out = StringIO()
        with redirect_stdout(out):
            code = run(["--storage", self.storage, *args])
        return code, out.getvalue()

    def test_cli_workflow(self):
        code, output = self._run(["add", "Task from CLI", "--priority", "medium"])
        self.assertEqual(code, 0)
        self.assertIn("Created task 1", output)

        code, output = self._run(["list", "--all"])
        self.assertEqual(code, 0)
        self.assertIn("Task from CLI", output)

        code, output = self._run(["complete", "1"])
        self.assertEqual(code, 0)
        self.assertIn("Completed task 1", output)

        code, output = self._run(["stats"])
        self.assertEqual(code, 0)
        self.assertIn("Total: 1", output)
        self.assertIn("Completed: 1", output)


if __name__ == "__main__":
    unittest.main()

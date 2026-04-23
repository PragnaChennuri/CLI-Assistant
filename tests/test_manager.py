import tempfile
import unittest
from pathlib import Path

from cli_assistant.manager import TaskManager
from cli_assistant.storage import JsonTaskStorage


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.tmpdir.name) / "tasks.json"
        self.manager = TaskManager(JsonTaskStorage(self.storage_path))

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_update_complete_delete_task(self):
        task = self.manager.add_task("Write tests", priority="high", due_date="2026-05-01")
        self.assertEqual(task.id, 1)
        self.assertEqual(len(self.manager.list_tasks()), 1)

        updated = self.manager.update_task(task.id, title="Write focused tests", description="for manager")
        self.assertEqual(updated.title, "Write focused tests")
        self.assertEqual(updated.description, "for manager")

        completed = self.manager.complete_task(task.id)
        self.assertTrue(completed.completed)
        self.assertIsNotNone(completed.completed_at)

        self.manager.delete_task(task.id)
        self.assertEqual(self.manager.list_tasks(), [])

    def test_persists_to_local_storage(self):
        self.manager.add_task("Persist me")

        reloaded = TaskManager(JsonTaskStorage(self.storage_path))
        tasks = reloaded.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Persist me")

    def test_stats_and_status_filter(self):
        one = self.manager.add_task("Pending")
        self.manager.add_task("Done")
        self.manager.complete_task(2)

        pending = self.manager.list_tasks(status="pending")
        completed = self.manager.list_tasks(status="completed")
        stats = self.manager.stats()

        self.assertEqual([t.id for t in pending], [one.id])
        self.assertEqual([t.id for t in completed], [2])
        self.assertEqual(stats, {"total": 2, "completed": 1, "pending": 1})


if __name__ == "__main__":
    unittest.main()

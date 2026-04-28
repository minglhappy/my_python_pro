"""任务管理器的测试用例"""

import pytest
from task_manager import Task, TaskManager


class TestTask:
    """测试Task类"""

    def test_create_task(self) -> None:
        task = Task("测试任务", "描述", 3)
        assert task.title == "测试任务"
        assert task.completed is False

    def test_mark_complete(self) -> None:
        task = Task("测试任务")
        task.mark_complete()
        assert task.completed is True

    def test_mark_incomplete(self) -> None:
        task = Task("测试任务")
        task.mark_complete()
        task.mark_incomplete()
        assert task.completed is False


class TestTaskManager:
    """测试TaskManager类"""

    def setup_method(self) -> None:
        self.manager = TaskManager()

    def test_add_task(self) -> None:
        task = self.manager.add_task("新任务")
        assert len(self.manager.tasks) == 1
        assert task.title == "新任务"

    def test_remove_task(self) -> None:
        self.manager.add_task("任务1")
        self.manager.add_task("任务2")
        assert self.manager.remove_task(0) is True
        assert len(self.manager.tasks) == 1

    def test_remove_invalid_index(self) -> None:
        assert self.manager.remove_task(99) is False

    def test_complete_task(self) -> None:
        self.manager.add_task("任务")
        self.manager.complete_task(0)
        assert self.manager.tasks[0].completed is True

    def test_get_stats(self) -> None:
        self.manager.add_task("任务1")
        self.manager.add_task("任务2")
        self.manager.complete_task(0)
        stats = self.manager.get_stats()
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["pending"] == 1

    def test_invalid_priority(self) -> None:
        with pytest.raises(ValueError):
            self.manager.add_task("任务", priority=6)

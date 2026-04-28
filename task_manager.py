"""
Git练习项目 - 一个简单的任务管理器
用于管理日常任务，支持添加、删除、查看和标记完成状态
"""

import sys
import json
import os
from datetime import datetime
from typing import Optional, Any


# 修复Windows控制台中文输出乱码问题
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


class Task:
    """表示一个任务"""

    def __init__(self, title: str, description: str = "", priority: int = 1) -> None:
        self.title = title
        self.description = description
        self.priority = priority  # 1-5，5为最高优先级
        self.completed = False
        self.created_at = datetime.now()

    def mark_complete(self) -> None:
        """标记任务为已完成"""
        self.completed = True

    def mark_incomplete(self) -> None:
        """标记任务为未完成"""
        self.completed = False

    def to_dict(self) -> dict[str, Any]:
        """将任务转换为字典以便JSON序列化"""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Task':
        """从字典反序列化创建任务对象"""
        task = cls(data["title"], data.get("description", ""), data.get("priority", 1))
        task.completed = data.get("completed", False)
        if "created_at" in data:
            task.created_at = datetime.fromisoformat(data["created_at"])
        return task

    def __str__(self) -> str:
        status = "已完成" if self.completed else "未完成"
        return f"[{status}] {self.title} (优先级: {self.priority})"


class TaskManager:
    """任务管理器，负责管理所有任务"""

    def __init__(self, data_file: str = "tasks.json") -> None:
        self.tasks: list[Task] = []
        self.data_file = data_file
        self.load_from_file()

    def save_to_file(self) -> None:
        """将任务保存到JSON文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存任务失败: {e}")

    def load_from_file(self) -> None:
        """从JSON文件加载任务"""
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except Exception as e:
            print(f"加载任务失败: {e}")

    def add_task(self, title: str, description: str = "", priority: int = 1) -> Task:
        """添加新任务"""
        if priority < 1 or priority > 5:
            raise ValueError("优先级必须在1-5之间")
        task = Task(title, description, priority)
        self.tasks.append(task)
        self.save_to_file()
        return task

    def remove_task(self, index: int) -> bool:
        """根据索引删除任务"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_to_file()
            return True
        return False

    def get_task(self, index: int) -> Optional[Task]:
        """根据索引获取任务"""
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    def list_tasks(self, show_completed: bool = True) -> list[Task]:
        """列出所有任务"""
        if show_completed:
            return self.tasks
        return [t for t in self.tasks if not t.completed]

    def complete_task(self, index: int) -> bool:
        """完成指定索引的任务"""
        task = self.get_task(index)
        if task:
            task.mark_complete()
            self.save_to_file()
            return True
        return False

    def get_stats(self) -> dict:
        """获取任务统计信息"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        return {"total": total, "completed": completed, "pending": total - completed}


def main() -> None:
    """主函数，演示任务管理器的基本功能"""
    manager = TaskManager("demo_tasks.json")

    # 如果没有任务，则添加一些示例任务
    if not manager.list_tasks():
        print("=== 初始化并添加示例任务 ===")
        manager.add_task("学习Git基础", "了解commit、push、pull等命令", 5)
        manager.add_task("练习分支操作", "创建和合并分支", 4)
        manager.add_task("学习Git进阶", "rebase、cherry-pick等操作", 3)
    else:
        print("=== 从文件中加载了已存在的任务 ===")

    # 列出所有任务
    print("\n=== 当前所有任务 ===")
    for i, task in enumerate(manager.list_tasks()):
        print(f"{i}: {task}")

    # 如果第一个任务没完成，就完成它演示一下
    first_task = manager.get_task(0)
    if first_task and not first_task.completed:
        manager.complete_task(0)
        print("\n=== 完成第一个任务后 ===")
        for i, task in enumerate(manager.list_tasks()):
            print(f"{i}: {task}")

    # 显示统计信息
    stats = manager.get_stats()
    print(f"\n=== 统计信息 ===")
    print(f"总计: {stats['total']}, 已完成: {stats['completed']}, 未完成: {stats['pending']}")


if __name__ == "__main__":
    main()

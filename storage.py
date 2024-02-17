from dataclasses import dataclass

from .models import List, Task


@dataclass
class Database:
    lists: dict[int, List] = {}
    tasks: dict[int, Task] = {}

    def get_lists(self) -> list[List]:
        return list(self.lists.values())

    def get_list(self, list_id: int) -> List:
        for list in self.lists:
            if list.id == list_id:
                return list
        # raise not found

    def get_tasks(self, list_id: int) -> list[Task]:
        return [task for task in self.tasks.values() if task.list_id == list_id]

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        # raise not found

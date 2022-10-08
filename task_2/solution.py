import json
import os
from datetime import date
import time
from typing import List, Dict


class Model:
    def __init__(self, file_name):
        self.file_name = file_name
        self.activeTasks = []
        self.completedTasks = {}

    def load_tasks(self) -> None:
        with open(self.file_name, encoding="utf-8") as file:
            data = json.load(file)
        self.activeTasks = data["activeTasks"]
        self.completedTasks = data["completedTasks"]

    def get_activeTasks(self) -> List:
        return self.activeTasks

    def get_completedTasks(self) -> Dict:
        return self.completedTasks

    def add_task(self, task_name: str) -> List:
        self.activeTasks.append(task_name)
        return self.activeTasks

    def add_tasks(self, tasks: List[str]) -> List[str]:
        for task_name in tasks:
            self.add_task(task_name)
        return self.activeTasks

    def remove_task(self, task_id: int) -> str:
        return self.activeTasks.pop(task_id)

    def remove_tasks(self, tasks: List[int]) -> List[str]:
        return [self.activeTasks.pop(task_id) for task_id in tasks]

    def mark_as_done(self, task_id: int) -> str:
        task = self.remove_task(task_id=task_id)

        today_date = date.today().strftime("%d/%m/%Y")

        self.completedTasks.update({
            today_date: self.completedTasks.get(today_date, []) + [task]
        })
        return task

    def save(self) -> None:
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump({
                "activeTasks": self.activeTasks,
                "completedTasks": self.completedTasks
            }, file)


class View:
    @classmethod
    def clean_screen(cls):
        os.system('clear')

    def tasks_view(self, tasks: List[str]):
        for tk, task in enumerate(tasks):
            print(f"{tk}| {task}")

    def menu_view(self):
        msg = """
            Hello this is TODO app with a command line interface.
            
            To start working with that you should tell me number of action.
            1) Add an item
            2) Remove an item
            3) Mark an item as done
            4) List items
        """
        print(msg)

    def add_tasks_view(self):
        msg = """
        To add new tasks just type them and press enter. 
        Every new line == new task. 
        To exit typing mode just leave empty line.
        """
        print(msg)



def controller():
    ...


if __name__ == "__main__":
    controller()

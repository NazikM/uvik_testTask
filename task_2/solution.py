import json
import os
from datetime import date
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

    def add_tasks(self, tasks: List[str]) -> List[str]:
        for task_name in tasks:
            self.activeTasks.append(task_name)
        return self.activeTasks

    def remove_tasks(self, tasks: List[int]) -> List[str]:
        return [self.activeTasks.pop(task_id) for task_id in tasks]

    def mark_as_done(self, task_id: int) -> str:
        tasks = self.remove_tasks(tasks=[task_id])

        today_date = date.today().strftime("%d/%m/%Y")

        self.completedTasks.update({
            today_date: self.completedTasks.get(today_date, []) + tasks
        })
        return tasks[0]

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

    def print_tasks(self, active: List[str], completed: Dict[str, List[str]]):
        print("YOUR TODO LIST")
        print("To be done:")
        for tk, task in enumerate(active):
            print(f"{tk}| {task}")
        print("Completed:")
        for _, tasks in completed:
            for tk, task in enumerate(active):
                print(f"{tk}| {task}")
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


class Controller:
    @staticmethod
    def multiline_input() -> List[str]:
        res = []
        while temp := input("::"):
            res.append(temp)
        return res

    @staticmethod
    def controller():
        model = Model("storage.json")
        view = View()
        model.load_tasks()
        view.clean_screen()
        while True:
            view.menu_view()
            choice = input("::")
            match choice:
                case "1":
                    view.add_tasks_view()
                    data = Controller.multiline_input()
                    model.add_tasks(data)
                case "2":
                    ...
                case "3":
                    ...
                case "4":
                    view.print_tasks(active=model.get_activeTasks(),
                                     completed=model.get_completedTasks())


if __name__ == "__main__":
    Controller.controller()

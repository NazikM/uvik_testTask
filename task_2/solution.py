import json
from datetime import date

class Model:
    def __init__(self, file_name):
        self.file_name = file_name
        self.activeTasks = []
        self.completedTasks = {}

    def load_tasks(self):
        with open(self.file_name, encoding="utf-8") as file:
            data = json.load(file)
        self.activeTasks = data["activeTasks"]
        self.completedTasks = data["completedTasks"]

    def get_activeTasks(self):
        return self.activeTasks

    def get_completedTasks(self):
        return self.completedTasks

    def add_task(self, task_name):
        self.activeTasks.append(task_name)
        return self.activeTasks

    def remove_task(self, task_id: int):
        return self.activeTasks.pop(task_id)

    def mark_as_done(self, task_id: int):
        task = self.remove_task(task_id=task_id)

        today_date = date.today().strftime("%d/%m/%Y")

        self.completedTasks.update({
            today_date: self.completedTasks.get(today_date, []) + [task]
        })



class View:
    ...


def controller():
    ...


if __name__ == "__main__":
    controller()

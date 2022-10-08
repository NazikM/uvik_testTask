import json


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



class View:
    ...


def controller():
    ...


if __name__ == "__main__":
    controller()

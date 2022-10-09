import json
import time
from datetime import date
from typing import List, Dict
from colorama import Fore, Style


class Model:
    def __init__(self, file_name):
        self.file_name = file_name
        self._tasks = []
        self._lastId = None

    def load_tasks(self) -> None:
        with open(self.file_name, encoding="utf-8") as file:
            data = json.load(file)
        self._tasks = data["tasks"]
        self._lastId = data["lastId"]

    def get_tasks(self):
        return self._tasks

    def add_tasks(self, tasks: List[str]) -> List[str]:
        for task_name in tasks:
            self._lastId += 1
            self._tasks.append({
                "id": self._lastId,
                "task": task_name,
                "completed": False
            })
        return self._tasks

    def remove_tasks(self, tasks: List[str]) -> List[str]:
        response = []
        for task_id in tasks:
            try:
                task_id = int(task_id)
            except ValueError:
                response.append(f"Not correct format {task_id}")
                continue
            for i in range(len(self._tasks)):
                if self._tasks[i]['id'] == task_id:
                    response.append(self._tasks.pop(i))
                    break
            else:
                response.append(f"There is no task with id {task_id}")
        return response

    def mark_as_done(self, task_id: int) -> Dict:
        for task in self._tasks:
            if task['id'] == task_id:
                task.update({
                    'completed': True,
                    'date': date.today().strftime("%d/%m/%Y")
                })
                break
        else:
            return {}
        return task

    def show_stat(self):
        res = {}
        for task in self._tasks:
            if task['completed']:
                res.update({
                    task['date']: res.get(task['date'], 0) + 1
                })
        return res

    def save_to_file(self) -> None:
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump({
                'tasks': self._tasks,
                'lastId': self._lastId
            }, file, indent=4)


class View:

    @staticmethod
    def decorator_for_output(func):
        def wrapper(*args, **kwargs):
            print("----------------------------------------------------------------")
            return func(*args, **kwargs)
        return wrapper

    @decorator_for_output
    def print_tasks(self, tasks: List[Dict]):
        print("YOUR TODO LIST")
        if tasks:
            for task in tasks:
                print(
                    f"{task['id']}| {task['task']}{(Fore.GREEN + ' Done' + Style.RESET_ALL) if task['completed'] else ''}")
        else:
            print("There are no tasks!")

    @decorator_for_output
    def menu_view(self):
        msg = "Hello this is TODO app with a command line interface.\n\n" \
              "To start working with that you should tell me number of action.\n" \
              "1) Add an item\n" \
              "2) Remove an item\n" \
              "3) Mark an item as done\n" \
              "4) List items\n" \
              "5) Show stat\n"
        print(msg)

    @decorator_for_output
    def add_tasks_view(self):
        msg = "To add new tasks just type their ids.\n" \
              "Every new line == new task.\n" \
              "To exit typing mode just leave empty line."
        print(msg)

    @decorator_for_output
    def remove_tasks_view(self):
        msg = "To remove tasks just type their ids.\n" \
              "Every new line == new task.\n" \
              "To exit typing mode just leave empty line."
        print(msg)

    @decorator_for_output
    def mark_as_done_view(self):
        print("Type 1 id of item that should be marked as done.")

    @decorator_for_output
    def stat_view(self, data):
        if data:
            for k, v in data.items():
                print(f"{k}: you've completed {v} tasks!")
        else:
            print("You haven't completed task yet")

    @decorator_for_output
    def not_correct_data_passed(self, data):
        print(f"Not correct data passed {data}")


class Controller:
    @staticmethod
    def multiline_input() -> List[str]:
        res = []
        while temp := input("::"):
            res.append(temp)
        return res

    @staticmethod
    def str_to_int(data):
        try:
            return int(data)
        except ValueError:
            return data

    @staticmethod
    def controller():
        model = Model("storage.json")
        view = View()
        model.load_tasks()
        while True:
            view.menu_view()
            choice = input("::")
            match choice:
                case "1":
                    view.add_tasks_view()
                    data = Controller.multiline_input()
                    model.add_tasks(data)
                case "2":
                    view.remove_tasks_view()
                    data = Controller.multiline_input()
                    res = model.remove_tasks(data)
                    print(res)
                case "3":
                    view.mark_as_done_view()
                    task_id_input = Controller.str_to_int(input("::"))
                    if task_id_input is not None:
                        res = model.mark_as_done(task_id_input)
                        print(res)
                    else:
                        view.not_correct_data_passed(task_id_input)
                case "4":
                    view.print_tasks(tasks=model.get_tasks())
                case "5":
                    stat = model.show_stat()
                    view.stat_view(stat)
            model.save_to_file()
            time.sleep(1)


if __name__ == "__main__":
    Controller.controller()

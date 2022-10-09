import json
import os
from datetime import date
from typing import List, Dict
from colorama import Fore
from colorama import Style


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

    # def get_activeTasks(self) -> List:
    #     for task in self.tasks:
    #         if not task["completed"]:
    #             yield task

    # def get_completedTasks(self) -> Dict:
    #     for task in self.tasks:
    #         if task["completed"]:
    #             yield task

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
            for i in range(len(self._tasks)):
                if self._tasks[i]['id'] == int(task_id):
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

    def save(self) -> None:
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump({
                'tasks': self._tasks
            }, file)


class View:
    @classmethod
    def clean_screen(cls):
        os.system('clear')

    def print_tasks(self, tasks: List[Dict]):
        print("YOUR TODO LIST")
        if tasks:
            for task in tasks:
                print(f"{task['id']}| {task['task']}{(Fore.GREEN+' Done'+Style.RESET_ALL)if task['completed'] else ''}")
        else:
            print("There are no tasks!")

    def menu_view(self):
        msg = """
        Hello this is TODO app with a command line interface.
            
        To start working with that you should tell me number of action.
        1) Add an item
        2) Remove an item
        3) Mark an item as done
        4) List items
        5) Show stat
        """
        print(msg)

    def add_tasks_view(self):
        msg = """
        To add new tasks just type their ids.
        Every new line == new task. 
        To exit typing mode just leave empty line.
        """
        print(msg)
    
    def remove_tasks_view(self):
        msg = """
        To remove tasks just type their ids. 
        Every new line == new task. 
        To exit typing mode just leave empty line.
        """
        print(msg)

    def mark_as_done_view(self):
        msg = """
        Type 1 id of item that should be marked as done.
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
                    view.remove_tasks_view()
                    data = Controller.multiline_input()
                    res = model.remove_tasks(data)
                    print(res)
                case "3":
                    view.mark_as_done_view()
                    task_id_input = int(input("::"))
                    res = model.mark_as_done(task_id_input)
                    print(res)
                case "4":
                    view.print_tasks(tasks=model.get_tasks())
                case "5":
                    ...


if __name__ == "__main__":
    Controller.controller()

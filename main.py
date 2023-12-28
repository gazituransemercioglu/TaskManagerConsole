#author: gazi turan semercioglu - 20190808012
#auhtor: Selin Yıldız - 20200808608


from abc import ABC, abstractmethod
from enum import Enum


# State Pattern
class TaskState(Enum):
    TODO = "Todo"
    DONE = "Done"
    WAIT = "Wait"


class TaskContext:
    def __init__(self, state):
        self._state = state

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state


# Factory Method Pattern
class TaskFactory(ABC):
    @abstractmethod
    def create_task(self, assignee, assigned_to, date, name):
        pass


class CodeTaskFactory(TaskFactory):
    def create_task(self, assignee, assigned_to, date, name, repo_link):
        return CodeTask(assignee, assigned_to, date, name, repo_link)


class SocialTaskFactory(TaskFactory):
    def create_task(self, assignee, assigned_to, date, name, design_link):
        return SocialTask(assignee, assigned_to, date, name, design_link)


class BusinessTaskFactory(TaskFactory):
    def create_task(self, assignee, assigned_to, date, name):
        return BusinessTask(assignee, assigned_to, date, name)


class Task(ABC):
    def __init__(self, assignee, assigned_to, date, name):
        self.assignee = assignee
        self.assigned_to = assigned_to
        self.date = date
        self.name = name
        self.context = TaskContext(TaskState.WAIT)

    @abstractmethod
    def display_info(self):
        pass


class CodeTask(Task):
    def __init__(self, assignee, assigned_to, date, name, repo_link):
        super().__init__(assignee, assigned_to, date, name)
        self.repo_link = repo_link

    def display_info(self):
        print(f"Code Task: {self.name}, Assignee: {self.assignee}, Repo Link: {self.repo_link}, State: {self.context.get_state().value}")


class SocialTask(Task):
    def __init__(self, assignee, assigned_to, date, name, design_link):
        super().__init__(assignee, assigned_to, date, name)
        self.design_link = design_link

    def display_info(self):
        print(f"Social Task: {self.name}, Assignee: {self.assignee}, Design Link: {self.design_link}, State: {self.context.get_state().value}")


class BusinessTask(Task):
    def display_info(self):
        print(f"Business Task: {self.name}, Assignee: {self.assignee}, State: {self.context.get_state().value}")


# Command Pattern
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Command Pattern
class CreateTaskCommand(Command):
    def __init__(self, factory, assignee, assigned_to, date, name, board_name, *extra_args):
        self.factory = factory
        self.extra_args = extra_args
        self.task = None
        self.assignee = assignee
        self.assigned_to = assigned_to
        self.date = date
        self.name = name
        self.board_name = board_name

    def execute(self):
        self.task = self.factory.create_task(self.assignee, self.assigned_to, self.date, self.name, *self.extra_args)
        return self.task


# Client
# TaskManager sınıfı
class TaskManager:
    def __init__(self):
        self.user = None
        self.groups = []
        self.boards = []
        self.tasks = []
        self.current_board = None

    def create_user(self, name):
        self.user = User(name)

    def create_group(self, name):
        new_group = Group(name)
        self.groups.append(new_group)
        if self.user:
            self.user.groups.append(new_group)
        return new_group

    def login_user(self, name):
        user_found = False
        for group in self.groups:
            for user in group.users:
                if user.name == name:
                    self.user = user
                    user_found = True
                    break
            if user_found:
                break

        if not user_found:
            print(f"User '{name}' not found.")

    def go_group(self, group_name):
        for group in self.groups:
            if group.name == group_name:
                self.current_group = group
                return True
        return False

    def create_board(self, name):
        if self.user and self.current_group:
            new_board = Board(name)
            self.current_group.boards.append(new_board)
            self.user.boards.append(new_board)
            self.current_board = new_board
            return new_board
        else:
            print("User or group not available. Create user and group first.")

    def go_board(self, board_name):
        if self.user and self.current_group:
            for board in self.current_group.boards:
                if board.name == board_name:
                    self.current_board = board
                    return True
        return False

    def create_task(self, task_type, name, *extra_args):
        if self.user and self.current_group and self.current_board:
            factory = None
            if task_type == "code":
                factory = CodeTaskFactory()
            elif task_type == "social":
                factory = SocialTaskFactory()
            elif task_type == "business":
                factory = BusinessTaskFactory()

            if factory:
                create_task_command = CreateTaskCommand(factory, self.user.name, self.current_board.name, "2023-01-01",
                                                        name, self.current_board.name,
                                                        *extra_args)  # board_name +
                created_task = create_task_command.execute()
                self.tasks.append(created_task)
                print(f"{task_type.capitalize()} task '{name}' created in board '{self.current_board.name}'.")
        else:
            print("User, group, or board not available. Create user, group, and board first.")

    def list_groups(self):
        if self.user and self.user.groups:
            print(f"Groups for user '{self.user.name}':")
            for group in self.user.groups:
                print(group.name)
        else:
            print("No groups found.")

    def list_boards(self):
        if self.user and self.user.boards:
            print(f"Boards for user '{self.user.name}':")
            for board in self.user.boards:
                print(board.name)
        else:
            print("No boards found.")

    def list_tasks(self):
        if self.user:
            print(f"Tasks for user '{self.user.name}':")
            for task in self.tasks:
                task.display_info()
        else:
            print("User not logged in.")

    def list_boards_in_current_group(self):  # Eklendi
        if self.user and self.current_group:
            print(f"Boards in group '{self.current_group.name}':")
            for board in self.current_group.boards:
                print(board.name)
        else:
            print("User or group not available. Create user and group first.")

    def list_tasks_in_current_board(self):  # Eklendi
        if self.user and self.current_board:
            print(f"Tasks in board '{self.current_board.name}':")
            for task in self.tasks:
                if self.current_board.name == task.board_name:
                    task.display_info()
        else:
            print("User or board not available. Create user and board first.")

    def read(self):
        if not self.user or not self.current_board:
            print("User not logged in or no board selected.")
            return

        print(f"Tasks in board '{self.current_board.name}':")
        for task in self.tasks:
            if self.current_board.name == task.assigned_to:
                task.display_info()


# Group, Board, User classes are simple classes representing the entities in the system.
class Group:
    def __init__(self, name):
        self.name = name
        self.boards = []


class Board:
    def __init__(self, name):
        self.name = name


class User:
    def __init__(self, name):
        self.name = name
        self.groups = []
        self.boards = []


class ConsoleInterface:
    def __init__(self):
        self.task_manager = TaskManager()
        self.commands = {
            "create_user": self.create_user,
            "login_user": self.login_user,
            "create_group": self.create_group,
            "go_group": self.go_group,
            "create_board": self.create_board,
            "go_board": self.go_board,
            "create_task": self.create_task,
            "list_groups": self.list_groups,
            "list_boards": self.list_boards,
            "list_tasks": self.list_tasks,
            "list_boards_in_current_group": self.list_boards_in_current_group,
            "list_tasks_in_current_board": self.list_tasks_in_current_board,
            "exit": self.exit_console,
        }

    def list_boards_in_current_group(self):
        self.task_manager.list_boards_in_current_group()

    def list_tasks_in_current_board(self):
        self.task_manager.list_tasks_in_current_board()

    def create_user(self, name):
        self.task_manager.create_user(name)
        print(f"User '{name}' created.")

    def login_user(self, name):
        self.task_manager.login_user(name)
        print(f"User '{name}' logged in.")

    def create_group(self, name):
        self.task_manager.create_group(name)
        print(f"Group '{name}' created.")

    def go_group(self, group_name):
        if self.task_manager.go_group(group_name):
            print(f"Entered group '{group_name}'.")
        else:
            print(f"Group '{group_name}' not found.")

    def create_board(self, name):
        self.task_manager.create_board(name)
        print(f"Board '{name}' created.")

    def go_board(self, board_name):
        if self.task_manager.go_board(board_name):
            print(f"Entered board '{board_name}'.")
        else:
            print(f"Board '{board_name}' not found.")

    def create_task(self, task_type, name, *extra_args):
        self.task_manager.create_task(task_type, name, *extra_args)

    def list_groups(self):
        self.task_manager.list_groups()

    def list_boards(self):
        self.task_manager.list_boards()

    def list_tasks(self):
        self.task_manager.list_tasks()

    def list_boards_in_current_group(self):  # Eklendi
        if self.task_manager.user and self.task_manager.current_group:
            print(f"Boards in group '{self.task_manager.current_group.name}':")
            for board in self.task_manager.current_group.boards:
                print(board.name)
        else:
            print("User or group not available. Create user and group first.")

    def list_tasks_in_current_board(self):  # Eklendi
        if self.task_manager.user and self.task_manager.current_board:
            print(f"Tasks in board '{self.task_manager.current_board.name}':")
            for task in self.task_manager.tasks:
                if self.task_manager.current_board.name == task.board_name:
                    task.display_info()
        else:
            print("User or board not available. Create user and board first.")

    def exit_console(self):
        print("Exiting console.")
        exit()

    def print_error(self, message):
        print(f"Error: {message}")

    def get_command(self):
        return input("Enter a command: ")

    def start_console(self):
        print("Welcome to Task Manager Console!")
        while True:
            command_input = self.get_command()
            command_parts = command_input.split()
            command_name = command_parts[0] if command_parts else None

            if command_name in self.commands:
                self.commands[command_name](*command_parts[1:])
            else:
                self.print_error("Invalid command. Please try again.")

    def run(self):
        self.start_console()


def main():
    console_interface = ConsoleInterface()

    # Test commands
    test_commands = [
        "create_user JohnDoe",
        "create_group Development",
        "go_group Development",
        "create_board Sprint1",
        "create_task code Task1 https://github.com/repo1",
        "create_task social Task2 https://designs.com/design1",
        "create_task business Task3",
        "list_groups",
        "list_boards",
        "list_tasks",
        "go_board Sprint1",

        "exit"
    ]

    for command_input in test_commands:
        command_parts = command_input.split()
        command_name = command_parts[0] if command_parts else None

        if command_name in console_interface.commands:
            console_interface.commands[command_name](*command_parts[1:])
        else:
            console_interface.print_error("Invalid command. Please try again.")

if __name__ == "__main__":
    #main()
    console_interface = ConsoleInterface()
    console_interface.run()

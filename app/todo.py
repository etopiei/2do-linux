import db
import time


class ToDo:

    """
    The ToDo class is the top level class which is used by the app. It handles accessing database methods
    Storing data in data structures and should provide the necessary methods to the user to be able
    to manipulate data and the UI to make the app work.
    """

    def __init__(self):
        self.main_lists = MainList()
        self.tasks = TaskList()

    def get_tasks_from_database(self):
        """
        This will use db methods to return data, this method will wrap the data
        in a Task Object and append it to the data structures of this class.
        """
        database_main_lists = db.get_main_lists()
        for x in database_main_lists:
            if x["title"] is not None and x["uid"] is not None:
                self.main_lists.append(
                    TaskObject(
                        x["title"],
                        x["uid"],
                        None,
                        colour=x["color"],
                        special=x["special"],
                    )
                )

        task_list = db.get_tasks()
        for x in task_list:
            task_colour = self.main_lists.find_colour_uid(x["parent_uid"])

            new_task = TaskObject(
                x["title"],
                x["uid"],
                x["parent_uid"],
                x["duetime"],
                x["startdate"],
                x["completed"],
                x["notes"],
                colour=task_colour,
            )

            self.tasks.append(new_task)

    def get_main_lists(self):
        return self.main_lists

    def get_tasks(self):
        return self.tasks.copy_task_list()

    def get_tasks_of_parent(self, parent_uid):
        return self.tasks.get_tasks_of_parent(parent_uid)


class TaskObject:

    """
    This class stores objects of types Task, they could be either a main list, a project or an individual task.
    This is the underlying structure for TaskList and MainList and is what the UI will mostly access.
    """

    def __init__(
        self,
        title,
        uid,
        parent_uid,
        duetime=time.time(),
        starttime=time.time(),
        completed=False,
        notes=None,
        colour=None,
        special=None,
    ):

        self.title = title
        self.uid = uid
        self.parent_uid = parent_uid
        self.duetime = duetime
        self.starttime = starttime
        self.completed = completed
        self.notes = notes
        self.colour = colour
        self.special = special

    def __str__(self):
        return_string = "{Title: " + str(self.title) + " UID: " + str(self.uid)
        if self.parent_uid is not None:
            return_string += " Parent: " + self.parent_uid
        if self.completed:
            return_string += " Completed"
        else:
            return_string += " Not Completed"
        if self.notes != "":
            return_string += " Notes: " + self.notes

        return_string += "}"

        return return_string


class MainList:

    """
    This class is a simple list that stores the Parent Lists (Such as Today, All etc.)
    These are the 2Do lists usually in the sidebar it stores objects of type task_object.
    """

    def __init__(self):
        self.lists = []

    def append(self, task_object):
        self.lists.append(task_object)
        return self

    def __str__(self):
        print(len(self.lists))
        total_string = ""
        for x in self.lists:
            total_string = total_string + str(x) + "\n"
        return total_string

    def __iter__(self):
        return iter(self.lists)

    def find_colour_uid(self, uid):
        for x in self.lists:
            if x.uid == uid:
                return x.colour


class TaskList:

    """
    This class stores all the tasks of the 2Do instance running. 
    It has methods to filter them and only get the tasks wanted.
    """

    def __init__(self):
        self.tasks = []

    def __len__(self):
        return len(self.tasks)

    def copy_task_list(self):
        """
        This is used to ensure that the original data from the database is still stored
        and the app UI can filter and sort on data without modifying the original data
        """
        copy = TaskList()
        for x in self.tasks:
            copy.append(x)
        return copy

    def append(self, task_object):
        self.tasks.append(task_object)

    def __str__(self):
        return_string = ""
        for x in self.tasks:
            if x is not None:
                return_string = return_string + str(x) + "\n"

        return return_string

    def __iter__(self):
        return iter(self.tasks)

    def toggle_completion_of_task_object(self, uid):

        for x in self.tasks:
            if x.uid == uid:
                x.completed = not x.completed
                return x.completed

    def get_tasks_of_parent(self, parent_uid):
        """
        Iterate over task list and if the task_object parent_uid is not none and equals parent_uid 
        add it to a return array, limit this to a set number of entries
        """
        in_parent = []
        for x in self.tasks:
            if x.parent_uid == parent_uid:
                in_parent.append(x)
        return in_parent

    def abstract_filter(self, condition_lambda):
        """
        This is an abstract function that iterates through a list of tasks and ensures that
        the conditions specified are met by any tasks that are returned.
        """
        filtered_task_list = []
        for x in self.tasks:
            if condition_lambda(x):
                filtered_task_list.append(x)
        self.tasks = filtered_task_list

    def abstract_sort(self, access_lambda, asc=False):
        """
        This is an abstract function that sorts the list of tasks by a particular key
        specified by the access lambda. Such as duedate, alphabetical etc.
        """
        self.tasks.sort(key=access_lambda, reverse=asc)

    def filter_tasks_by_completed(self, completed=False):
        """
        Filter by whether it has been completed or not: based on the completed argument
        """
        self.abstract_filter(lambda x: x.completed == completed)

    def filter_tasks_by_datetime(self, datetime, after=True):
        """
        This method should iterate through the task list given and only return those who are
        either after or before the specified date, the default is after
        """
        if after:
            self.abstract_filter(lambda x: x.duetime > datetime)
        else:
            self.abstract_filter(lambda x: x.duetime < datetime)

    def filter_tasks_by_parent_uid(self, uid):
        """
        This method should only allow tasks whose parent uid is the same as the argument passed to this function
        This function should be modified to go a few levels deep with parents
        """
        self.abstract_filter(lambda x: str(x.parent_uid) == str(uid))

    def sort_tasks_by_due_date(self, asc=False):
        """
        This method sorts by task due date using the abstract sort function.
        """
        self.abstract_sort(lambda x: x.duetime, asc)

    def search_by_keyword(self, keyword):
        """
        This method filters the task list by a keyword search (search on title)
        """
        self.abstract_filter(lambda x: keyword in x.title)

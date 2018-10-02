import db
import time

class ToDo:

    '''
    The ToDo class is the top level class which is used by the app. It handles accessing database methods
    Storing data in data structures and should provide the necessary methods to the user to be able
    to manipulate data and the UI to make the app work.
    '''

    def __init__(self):
        self.main_lists = MainList()
        self.tasks = TaskList()

    def get_tasks_from_database(self):
        '''
        This will use db methods to return data, this method will wrap the data
        in a Task Object and append it to the data structures of this class
        '''
        database_main_lists = db.get_main_lists()
        for x in database_main_lists:
            if x['title'] != None and x['uid'] != None:
                self.main_lists.append(TaskObject(x['title'], x['uid']))

        task_list = db.get_tasks()
        for x in task_list:
            self.tasks.append(TaskObject(x['title'], x['uid'], x['parent_uid'], x['duetime'], x['completed']))

    def get_main_lists(self):
        return self.main_lists

    def get_tasks(self):
        return self.tasks

    def get_tasks_of_parent(self, parent_uid):
        return self.tasks.get_tasks_of_parent(parent_uid)


class TaskObject:

    '''
    This class stores objects of types Task, they could be either a main list, a project or an individual task.
    This class needs to be fleshed out more to hold more data from the database
    This is the underlying structure for TaskList and MainList and is what the UI will mostly access.
    '''

    def __init__(self, title, uid, parent_uid=None, duetime=time.time(), completed=False):
        self.title = title
        self.uid = uid
        self.parent_uid = parent_uid
        self.duetime = duetime
        self.completed = completed

    def title(self):
        return self.title

    def uid(self):
        return self.uid

    def __str__(self):
        return "{Title: " + str(self.title) + " UID: " + str(self.uid) + "}"

class MainList:

    '''
    This class is a simple list that stores the Parent Lists (Such as Today, All etc.)
    These are the 2Do lists usually in the sidebar it stores objects of type task_object
    '''

    def __init__(self):
        self.lists = []

    def append(self, task_object):
        self.lists.append(task_object)

    def __str__(self):
        print(len(self.lists))
        totalString = ""
        for x in self.lists:
            totalString = totalString + str(x) + "\n"
        return totalString

    def __iter__(self):
        return iter(self.lists)


class TaskList:

    '''
    This class stores all the tasks of the 2Do instance running. 
    It has methods to filter them and only get the tasks wanted.
    '''

    def __init__(self):
        self.tasks = []

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

    def get_tasks_of_parent(self, parent_uid):
        '''
        Iterate over task list and if the task_object parent_uid is not none and equals parent_uid 
        add it to a return array, limit this to a set number of entries
        '''
        in_parent = []
        for x in self.tasks:
            if x.parent_uid == parent_uid:
                in_parent.append(x)
        return in_parent

    def abstract_filter(self, condition_lambda):
        '''
        This is an abstract function that iterates through a list of tasks and ensures that
        the conditions specified are met by any tasks that are returned.
        '''
        filtered_task_list = []
        for x in self.tasks:
            if condition_lambda(x):
                filtered_task_list.append(x)
        return filtered_task_list

    def filter_tasks_by_completed(self, completed=False):
        '''
        Filter by whether it has been completed or not: based on the completed argument
        '''
        return self.abstract_filter(lambda x: x.completed == completed)
                

    def filter_tasks_by_datetime(self, datetime, after=True):
        '''
        This method should iterate through the task list given and only return those who are
        either after or before the specified date, the default is after
        '''
        if after:
            return self.abstract_filter(lambda x: x.duetime > datetime)
        else:
            return self.abstract_filter(lambda x: x.duetime < datetime) 
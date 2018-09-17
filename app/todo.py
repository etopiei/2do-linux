import db

class ToDo:

    def __init__(self):
        self.main_lists = MainList()
        self.tasks = TaskList()

    def add_to_main_lists(self, uid, title):
        task_object = TaskObject(title, uid)
        self.main_lists.append(task_object)

    def add_to_tasks(self, uid, title):
        self.tasks[uid] = title

    def get_tasks_from_database(self):
        '''
        This will use db methods to return data, this method will wrap the data
        in a Task Object and append it to the data structures of this class
        '''
        database_main_lists = db.get_main_lists()
        for x in database_main_lists:
            if x['title'] != None and x['uid'] != None:
                task_object = TaskObject(x['title'], x['uid'])
                self.main_lists.append(task_object)

        task_list = db.get_tasks()
        for x in task_list:
            task_object = TaskObject(x['title'], x['uid'], x['parent_uid'])
            self.tasks.append(task_object)

    def get_main_lists(self):
        return self.main_lists

    def get_tasks(self):
        return self.tasks

    def get_tasks_of_parent(self, parent_uid):
        return self.tasks.get_tasks_of_parent(parent_uid)

class TaskObject:

    def __init__(self, title, uid, parent_uid=None):
        self.title = title
        self.uid = uid
        self.parent_uid = parent_uid

    def title(self):
        return self.title

    def uid(self):
        return self.uid

    def __str__(self):
        return "{Title: " + str(self.title) + " UID: " + str(self.uid) + "}"

class MainList:

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
        # Warning! This method will return all tasks held by the app, it is best to use the specific parent and the get_tasks_of_parents method
        # As this will return far too many tasks then should be rendered at once.
        return iter(self.tasks)

    def get_tasks_of_parent(self, parent_uid):
        # Iterate over task list and if the task_object parent_uid is not none and equals parent_uid 
        # add it to a return array, limit this to a set number of entries
        in_parent = []
        for x in self.tasks:
            if x.parent_uid == parent_uid:
                in_parent.append(x)
        return in_parent

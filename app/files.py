import os
import gzip
import biplist

class FileInterface:
    """
    This class will allow the todo object to interact seamlessly with files so that they can synced with Dropbox
    It's interface should be identical to the database methods so it can be a drop in replacement.

    One slight caveat, it won't update on the fly (methods called that change thing in the database won't happen)
    The client will have to explicitly save the app state.
    """

    def __init__(self, directories):
        self.unpacker = Unpacker(directories)
        self.repacker = Repacker(directories)

    def get_tasks(self):
        return self.unpacker.get_tasks()

    def get_main_lists(self):
        return self.unpacker.get_main_lists()

    def save_app_state(self, todo_instance):
        """
        This method should be used instead of commit_database_changes.
        """
        self.repacker.save_app_state(todo_instance)

class Unpacker:
    """
    This class is designed to take a file that is saved by 2Do to Dropbox
    and unpack it into a usable form which the 2Do class can utilise. 
    It will try and mirror methods and behaviour in db.py 
    (i.e. reading from files should be a drop in replacement to reading from the saved .sql backup)
    """

    def __init__(self, directories):
        self.directories = directories

    @staticmethod
    def get_key(keyname, data):
        print(keyname, len(data['$objects']), data)
        """
        This method will get the data associated with the key given
        Note: The key mightn't exist in the data, and if that is the case return None
        It will search through, find the key, then go to the data position.
        """
        for x in range(2, len(data['$objects']) - 1):
            if data['$objects'][x] == keyname:
                halfway = (len(data['$objects']) - 1) // 2
                print(halfway + x - 1)
                keys_data = data['$objects'][halfway + x - 1]
                return keys_data

        return None

    def get_single_task(self, filename):
        """
        This method will read in a task from a file and extract the relevant information,
        It will also store the filename of the task, so that changes can be saved to the file
        """
        with gzip.open(filename, "rb") as f:
            file_content = f.read()
            with open("temp_file.plist", "wb") as g:
                g.write(file_content)
                
        task_data = biplist.readPlist("temp_file.plist")
        os.remove("temp_file.plist")
           
        return {
            "title": self.get_key("title", task_data),
            "uid": self.get_key("uid", task_data),
            "parent_uid": self.get_key("caluid", task_data),
            "duetime": self.get_key("duetime", task_data),
            "completed": self.get_key("completed", task_data),
            "notes": self.get_key("notes", task_data),
            "startdate": self.get_key("startdate", task_data),
        }

    def get_tasks(self):
        """
        This method will return data compatible with the ToDo Object (see todo.py).
        This data should be identical to data returned in db.py's get_tasks method. 
        It will iterate through the directory given to the Unpacker class and get the data from the files
        """
        tasks = []
        for subdir, dirs, files in os.walk(self.directories[0]):
            for file in files:
                tasks.append(self.get_single_task(os.path.join(subdir, file))) 

        return tasks

    def get_main_lists(self):
        """
        This method should return data comaptible with the ToDo Object (see todo.py).
        The data returned should be identical to the data returned in db.py's get_task method.
        """
        print("Getting main lists")

class Repacker:

    def __init__(self, filenames):
        self.filenames = filenames

    def save_app_state(self, todo_object):
        """
        Take the current todo_object and pack it into files that can be synced to Dropbox.
        """
        print("Saving app state")

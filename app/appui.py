from appJar import gui
import todo

class MainUI:

    def __init__(self):
        # do any setup required by the app here
        self.app = gui("2Do Client", "600x600")
        self.app.setIcon("icon.gif")
        self.app.setExpand("both")
        self.app.setSticky("news")

    def main_setup(self, todo_object):
        # here take the data from the todo object and set up a UI
        # use frames to add labels to the list objects setup in the app init method
        current_list = None
        self.app.startFrame("Lists", row=0, column=0)
        main_lists = todo_object.get_main_lists()
        for x in main_lists:
            if x.title == "Music":
                current_list = x.uid
            self.app.label(x.title)
        self.app.stopFrame()

        self.app.startFrame("Tasks", row=0, column=1)
        for x in todo_object.get_tasks_of_parent(current_list):
            self.app.label(x.title)
        self.app.stopFrame()

    def start(self):
        # now start the app loop and spawn a window
        self.app.go()

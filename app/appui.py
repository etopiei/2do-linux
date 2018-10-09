from appJar import gui
import todo


class MainUI:

    def __init__(self):
        # do any setup required by the app here
        self.app = gui("2Do Client", "600x600")
        self.app.setIcon("icon.gif")
        self.app.setExpand("both")
        self.app.setSticky("news")
        self.current_list = None
        self.current_list_title = None
        self.main_list = None
        self.task_list = None
    
    def main_setup(self, todo_object):
        # here take the data from the todo object and set up a UI
        # use frames to add labels to the list objects setup in the app init method

        self.main_list = todo_object.get_main_lists()
        self.task_list = todo_object.get_tasks()
        self.draw()

    def draw(self):

        self.app.startFrame("Lists", row=0, column=0)

        for x in self.main_list:
            if self.current_list == None:
                self.current_list = x.uid
                self.current_list_title = x.title
            if self.current_list == x.uid:
                self.drawListMenuItem(x, True)
            else:
                self.drawListMenuItem(x, False)
        self.app.stopFrame()

        self.app.startFrame("Tasks", row=0, column=1)
        self.app.startScrollPane("Pane")

        # Make copy for draw filtering and sorting
        task_list = self.task_list.copy_task_list()

        if self.current_list_title != "All":
            task_list.filter_tasks_by_parent_uid(self.current_list) # Get tasks only from one list
        task_list.filter_tasks_by_completed(False) # Get incomplete tasks
        task_list.sort_tasks_by_due_date() # Sort them chronilogically

        for x in task_list:
            self.drawTaskObject(x)

        self.app.stopScrollPane()
        self.app.stopFrame()

    def drawTaskObject(self, task_object):
        self.app.addNamedCheckBox(task_object.title, str(task_object) + "task")
        self.app.addHorizontalSeparator()
        if task_object.notes != '':
            self.app.addLabel(str(task_object) + "note", task_object.notes)

    def drawListMenuItem(self, main_list_item, isSelected):
        self.app.button(main_list_item.title, value=self.handleMenuClick)
        if isSelected:
            self.app.setButtonBg(main_list_item.title, "red")

    def handleMenuClick(self, value):
         # print("Menu Click: " + str(value))
        for x in self.main_list:
            if x.title == str(value):
                self.current_list = x.uid
                self.current_list_title = x.title
        self.redraw()

    def redraw(self):
        self.app.removeAllWidgets() # see if this can be written to only remove widgets in the right pane.
        self.draw()

    def start(self):
        # now start the app loop and spawn a window
        self.app.go()

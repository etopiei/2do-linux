from appJar import gui
import todo, db, helpers
from helpers import Colour

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
        self.redraws = 0
    
    def main_setup(self, todo_object):
        # here take the data from the todo object and set up a UI
        # use frames to add labels to the list objects setup in the app init method

        self.main_list = todo_object.get_main_lists()
        self.task_list = todo_object.get_tasks()
        self.draw()

    def drawRightSide(self):
        
        self.app.startFrame("Tasks", row=0, column=1)
        self.app.startScrollPane("Pane" + str(self.redraws))

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

        self.redraws += 1

    def draw(self):

        self.app.startFrame("Lists", row=0, column=0)

        for x in self.main_list:
            if self.current_list == None:
                self.current_list = x.uid
                self.current_list_title = x.title
            if self.current_list == x.uid:
                self.drawListMenuItem(x, Colour(1, 0, 0))
            else:
                self.drawListMenuItem(x, x.colour)
        self.app.stopFrame()

        self.drawRightSide()

    def drawTaskObject(self, task_object):

        row = self.app.getRow()
        self.app.addNamedCheckBox(task_object.title, str(task_object) + "task" + str(self.redraws), row, 0)

        if task_object.duetime != 6406192800.0:
            self.app.addLabel(str(task_object) + "time" + str(self.redraws), helpers.time_to_string(task_object.duetime), row, 1)
            self.app.setLabelFg(str(task_object) + "time" + str(self.redraws), "red")
        elif task_object.starttime != 6406192800.0:
            self.app.addLabel(str(task_object) + "time" + str(self.redraws), helpers.time_to_string(task_object.starttime), row, 1)
            self.app.setLabelFg(str(task_object) + "time" + str(self.redraws), "green")

        self.app.setCheckBoxBg(str(task_object) + "task" + str(self.redraws), task_object.colour.convertRGBToHexString())
        self.app.setCheckBoxChangeFunction(str(task_object) + "task" + str(self.redraws), self.handleItemClick)

        if task_object.notes != '':
            self.app.addLabel(str(task_object) + "note" + str(self.redraws), task_object.notes)
            self.app.setLabelAlign(str(task_object) + "note" + str(self.redraws), "left")
            self.app.setLabelBg(str(task_object) + "note" + str(self.redraws), task_object.colour.convertRGBToHexString())

        self.app.addHorizontalSeparator()

    def drawListMenuItem(self, main_list_item, colour="#FFFFFF"):
        self.app.button(main_list_item.title, value=self.handleMenuClick)
        self.app.setButtonBg(main_list_item.title, colour.convertRGBToHexString())
        self.app.setButtonFg(main_list_item.title, colour.getDarkerShade().convertRGBToHexString())

    def handleMenuClick(self, value):
        for x in self.main_list:
            if x.title == str(value):
                self.current_list = x.uid
                self.current_list_title = x.title
        self.redraw()

    def getUIDFromString(self, task_object_string):
        return task_object_string.split('UID: ')[1].split(" ")[0]

    def handleItemClick(self, value):
        '''
        The value passed to this is the TaskObject that was clicked
        '''
        uid = self.getUIDFromString(value)
        newValue = self.task_list.toggleCompletionOfTaskObject(uid)
        db.toggleItemCompletionInDatabase(uid, newValue)
        self.redraw()

    def redraw(self):
        self.app.removeFrame("Tasks") # see if this can be written to only remove widgets in the right pane.
        self.drawRightSide()

    def start(self):
        # now start the app loop and spawn a window
        self.app.go()

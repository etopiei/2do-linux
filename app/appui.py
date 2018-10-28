from appJar import gui
import db
import helpers
import time
from helpers import Colour


class MainUI:
    def __init__(self):
        # do any setup required by the app here
        self.app = gui("2Do Client", "600x600")
        self.app.setIcon("icon.gif")
        self.app.setExpand("both")
        self.app.setSticky("news")

        self.full_list = None
        self.current_list = None
        self.current_show_hide = None
        self.next_show_hide = None

        self.current_list_title = None
        self.main_list = None
        self.task_list = None
        self.redraws = 0
        self.searchKeyword = ""

    def main_setup(self, todo_object):
        # here take the data from the todo object and set up a UI
        # use frames to add labels to the list objects setup in the app init method

        self.main_list = todo_object.get_main_lists()
        self.full_list = todo_object.get_tasks()
        self.draw()

    def search(self, button_name):
        if button_name == "Search":
            self.searchKeyword = self.app.getEntry("Search Term")
            self.redraw()
        else:
            self.searchKeyword = ""
            self.redraw()

    def filter_and_sort_tasks(self):
        # Make copy for draw filtering and sorting
        self.current_list = self.full_list.copy_task_list()

        bad_lists = ["All", "Done", "Today"]

        if self.current_list_title not in bad_lists:
            self.current_list.filter_tasks_by_parent_uid(
                self.current_list
            )  # Get tasks only from one list

        # filter tasks if there is a search term
        if self.searchKeyword != "":
            self.current_list.search_by_keyword(self.searchKeyword)

        if self.current_list_title == "Done":
            self.current_list.filter_tasks_by_completed(True)  # get all completed tasks
        else:
            self.current_list.filter_tasks_by_completed(False)  # Get incomplete tasks

        if self.current_list_title == "Today":
            start_str = time.strftime("%m/%d/%Y") + " 00:00:00"
            today = int(time.mktime(time.strptime(start_str, "%m/%d/%Y %H:%M:%S")))
            self.current_list.filter_tasks_by_datetime(today, True)

        self.current_list.sort_tasks_by_due_date(True)  # Sort them chronilogically

    def init_right_side(self):
        """
        This should only be called the first time the app is opened. It will render all tasks in a list
        Once this is done, the only adjustment should be hiding and showing items from this list
        :return: None
        """
        self.app.startFrame("Tasks", row=0, column=1)
        self.app.startScrollPane("Pane")

        # draw search bar
        self.app.addLabelEntry("Search Term")
        self.app.setEntry("Search Term", self.searchKeyword, False)
        self.app.addButtons(["Search", "Clear"], self.search)

        self.filter_and_sort_tasks()

        self.current_show_hide = {}
        for x in self.full_list:
            if x in self.current_list:
                self.current_show_hide[x.uid] = 1
            else:
                self.current_show_hide[x.uid] = 0

        for x in self.current_list:
            self.draw_task_object(x)

        self.app.stopScrollPane()
        self.app.stopFrame()

    def draw_right_side(self):

        self.filter_and_sort_tasks()

        # Here construct what to show/hide now that all filtering and sorting is done
        # compare full_list to current_list
        self.next_show_hide = {}
        for x in self.full_list:
            if x in self.current_list:
                self.next_show_hide[x.uid] = 1
            else:
                self.next_show_hide[x.uid] = 0
        # now compare next_show_hide to current_show_hide and work out what needs to change in the interface
        # This will ensure minimal UI changes and speed up the redraw
        diff_show_hide = self.make_diff()
        self.iterate_through_diff(diff_show_hide)
        self.current_show_hide = self.next_show_hide

    def make_diff(self):
        """
        This will construct a diff between the widgets being currently shown/hidden
        And what needs to be shown/hidden now
        :return: A list of UID's of task_object that need to be either hidden or shown.
        These will be in the form [UID, 0] OR [UID, 1]
        (1 indicating widget should be shown)
        """
        diff = []
        for x in self.full_list:
            if self.current_show_hide[x.uid] == 1 and self.next_show_hide[x.uid] == 0:
                diff.append([x.uid, 0])
            elif self.current_show_hide[x.uid] == 0 and self.next_show_hide[x.uid] == 1:
                diff.append([x.uid, 1])
            else:
                print("Keep Widget the Same")
        return diff

    def iterate_through_diff(self, diff):
        """
        This will iterate through a diff object from the make_diff method of this class and set the widgets to be either
        shown or hidden based on this.
        :return: None
        """
        self.app.openScrollPane("Pane")
        for x in diff:
            if x[1] == 1:
                self.app.showFrame(x[0])
            else:
                self.app.hideFrame(x[0])
        self.app.stopScrollPane()

    def draw(self):

        self.app.startFrame("Lists", row=0, column=0)

        for x in self.main_list:
            if self.current_list is None:
                self.current_list = x.uid
                self.current_list_title = x.title
            if self.current_list == x.uid:
                self.draw_list_menu_item(x, Colour(1, 0, 0))
            else:
                self.draw_list_menu_item(x, x.colour)
        self.app.stopFrame()

        self.init_right_side()

    def draw_task_object(self, task_object):

        self.app.startFrame(task_object.uid)

        row = self.app.getRow()
        truncated_title = task_object.title[:40]
        truncated = task_object.title != truncated_title
        if truncated:
            truncated_title += "..."
        self.app.addNamedCheckBox(
            truncated_title, str(task_object) + "task" + str(self.redraws), row, 0
        )

        unique_name = str(task_object) + "time" + str(self.redraws)

        if task_object.duetime != float(0):
            self.app.addLabel(
                unique_name, helpers.time_to_string(task_object.duetime), row, 1
            )
            self.app.setLabelFg(unique_name, "red")
        elif task_object.starttime != float(0):
            self.app.addLabel(
                unique_name, helpers.time_to_string(task_object.starttime), row, 1
            )
            self.app.setLabelFg(unique_name, "green")

        self.app.setCheckBoxChangeFunction(
            str(task_object) + "task" + str(self.redraws), self.handle_item_click
        )

        if task_object.notes != "":
            self.app.addLabel(
                str(task_object) + "note" + str(self.redraws), task_object.notes[:40]
            )
            self.app.setLabelAlign(
                str(task_object) + "note" + str(self.redraws), "left"
            )

        self.app.addHorizontalSeparator()

        self.app.stopFrame()

    def draw_list_menu_item(
        self, main_list_item, colour=Colour.from_hex_string("#FFFFFF")
    ):
        self.app.button(main_list_item.title, value=self.handle_menu_click)
        self.app.setButtonBg(main_list_item.title, colour.convert_rgb_to_hex_string())
        self.app.setButtonFg(
            main_list_item.title, colour.get_darker_shade().convert_rgb_to_hex_string()
        )

    def handle_menu_click(self, value):
        for x in self.main_list:
            if x.title == str(value):
                self.current_list = x.uid
                self.current_list_title = x.title
        self.redraw()

    def draw_sub_window_to_display_task(self):
        self.app.startSubWindow("single_task_view", modal=True)
        self.app.addLabel("TaskView")
        self.app.addButton("Change/Set Date")
        self.app.addButton("Set/Edit Notes")
        self.app.stopSubWindow()

    @staticmethod
    def get_uid_from_string(task_object_string):
        return task_object_string.split("UID: ")[1].split(" ")[0]

    def handle_item_click(self, value):
        """
        The value passed to this is the TaskObject that was clicked.
        """
        uid = self.get_uid_from_string(value)
        new_value = self.task_list.toggleCompletionOfTaskObject(uid)
        db.toggle_item_completion_in_database(uid, new_value)
        self.redraw()

    def redraw(self):
        self.draw_right_side()
        self.redraws += 1

    def start(self):
        # now start the app loop and spawn a window
        self.app.go()

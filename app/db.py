import sqlite3
from helpers import Colour

conn = sqlite3.connect('test.db')
c = conn.cursor()

def get_main_lists():
    '''
    This method should return from the database a list of main parent lists. 
    i.e. the lists in the sidebar.
    It should return an array of dictionary type objects structured as followed:
    {title: "list_title", "uid": "437942"}
    '''

    main_lists = []
    for row in c.execute('SELECT title, uid, parentuid, parentname, redcolor, greencolor, bluecolor FROM calendars'):
        special = False
        colour = Colour(row[4], row[5], row[6])
        if row[2] != '2DoCalGroupSmart':
            if row[3] != 'LISTS':
                special = True
            main_lists.append({'title': row[0], 'uid': row[1], 'color': colour, 'special': special})
    return main_lists

def get_tasks():
    '''
    This method will get tasks from the database including the parent info (this will be used later)
    It will return an array of tasks with the following structure:
    {title: "task_title", "uid" "943294", "parent_uid": "43892"}
    '''

    tasks = []
    for row in c.execute('SELECT title, uid, calendaruid, duedate, iscompleted, notes FROM tasks'):
        completed = True
        if row[4] == 0:
            completed = False

        tasks.append({'title': row[0], 'uid': row[1], 'parent_uid': row[2], 'duetime': row[3], 'completed': completed, 'notes': row[5]})

    return tasks


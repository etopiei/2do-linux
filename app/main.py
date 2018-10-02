import todo, appui

if __name__ == "__main__":
    
    app = appui.MainUI()

    todo_instance = todo.ToDo() # initalise
    todo_instance.get_tasks_from_database() # get data

    app.main_setup(todo_instance) # get app ready
    app.start() # leggo

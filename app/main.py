import todo, appui

if __name__ == "__main__":
    
    app = appui.MainUI()

    todo_instance = todo.ToDo()
    todo_instance.get_tasks_from_database()

    app.main_setup(todo_instance)
    app.start()

import todo
import appui
import db

if __name__ == "__main__":

    app = appui.MainUI()

    todo_instance = todo.ToDo()  # initialise
    todo_instance.get_tasks_from_database()  # get data

    app.main_setup(todo_instance)  # get app ready
    app.start()  # leggo
    db.close_connection()  # once app is done close connection to db

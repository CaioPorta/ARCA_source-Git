import src.app.core.DBManager as DBManager


def db():
    db = DBManager.ConnectToDB()
    return db

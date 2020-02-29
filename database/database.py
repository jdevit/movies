import sqlite3

class Database(object):

    instance = None

    @staticmethod
    def getInstance():
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance

    def __init__(self):
        super().__init__()

        # self.database_path = os.path.join("database/", 'database.sql')
        # self.connection = sqlite3.connect(self.database_path)

    def create_table(self, query):
        try:
            c = self.connection.cursor()
            c.execute(query)
        except Exception as e:
            return False
        return True

    def insert_data(self, query):
        try:
            c = self.connection.cursor()
            c.execute(query)
        except Exception as e:
            print(e)
            return False
        self.save()  # Saves database after insertion
        return True

    ## Saves changes made to database #(and closes connection)
    def save(self):
        try:
            self.connection.commit()
            # self.connection.close()
        except Exception as e:
            return False
        return True
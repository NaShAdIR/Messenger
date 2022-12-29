import sqlite3

class Data_base_control:
    def __init__(self, data_base):
        """
        При создании экземпляра класса,
        программа автоматически подключается
        к базе данных указанной в аргументе!
        """
        self.connection = sqlite3.connect(data_base)
        self.cursor = self.connection.cursor()

    def __repr__(self):
        data = self.cursor.execute("SELECT * FROM Users").fetchall()
        string = '\n'.join(str(user) for user in data)
        self.connection.close()

        return string


print(Data_base_control('datebase.db'))


input()
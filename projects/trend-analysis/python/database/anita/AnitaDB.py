from database.db.MySqlDB import MySqlDB
from database.db.structure.DBType import DBType

name = "anita"


class AnitaDB:
    def __init__(self, anonymous=False):
        self.database_name = name
        if anonymous:
            self.mysql_db = MySqlDB()
        else:
            self.mysql_db = MySqlDB(self.database_name)

    @property
    def database_name(self):
        return self._database_name

    @database_name.setter
    def database_name(self, value):
        self._database_name = value

    @property
    def mysql_db(self):
        return self._mysql_db

    @mysql_db.setter
    def mysql_db(self, value):
        self._mysql_db = value

    def exist(self):
        query = "SHOW DATABASES"

        fields, databases = self.mysql_db.search(query)
        for database in databases:
            if self.database_name == database[0]:
                return True

        return False
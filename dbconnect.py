import sqlalchemy
from sqlalchemy import text
import queries

HOST = "reddwarf.cs.rit.edu"
USER = "p320_13"
PASS = "aiyohleiCahc2xahtee1"
PORT = "5432"
LANG = "postgresql"
DATABASE = "%s://%s:%s@%s:%s/%s" % (LANG, USER, PASS, HOST, PORT, USER)

class Connection:
    def __init__(self, db_name):
        self.__engine = sqlalchemy.create_engine(db_name)
        self.__connection = self.__engine.connect()

    def execute_query(self, query, **kwargs):
        statement = text(query)
        try:
            ret = self.__connection.execute(statement, kwargs)
        except:
            ret = None

        return ret

if __name__ == "__main__":
    connection = Connection(DATABASE)
    # res = connection.execute_query(queries.select_users)
    # print(res)
    # for thing in res:
    #     print(thing)

    res = connection.execute_query(queries.select_users_kwargs, uid='1')
    for thing in res:
        print(thing)
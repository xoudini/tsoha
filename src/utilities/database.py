import psycopg2 as pg
from psycopg2.extras import RealDictCursor, RealDictRow

from typing import List, Dict, Tuple

class DatabaseManager:

    def __init__(self, database: str, user: str = None, password: str = None, host: str = None, port: int = None):
        paramlist: List[str] = []

        if database is not None:
            paramlist.append("dbname=" + database)
        
        if user is not None:
            paramlist.append("user=" + user)
        
        if password is not None:
            paramlist.append("password=" + password)
        
        if host is not None:
            paramlist.append("host=" + host)
        
        if port is not None:
            paramlist.append("port=" + str(port))
        
        self.dsn: str = " ".join(paramlist)
    
    def test_connection(self) -> str:
        try:
            with pg.connect(dsn=self.dsn) as connection:
                return "Database connection established!"
        except Exception as e:
            return "Exception: {0}".format(e)

    def execute_query(self, sql: str, mapping: Dict[str, str] = None) -> List[Dict]:
        try:
            with pg.connect(dsn=self.dsn) as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    try:
                        if mapping is None:
                            cursor.execute(sql)
                        else:
                            cursor.execute(sql, mapping)

                        rows = cursor.fetchall()

                        return rows

                    except Exception as e:
                        # TODO: Rethrow.
                        print(e)
        
        except Exception as e:
            # TODO: Rethrow.
            print(e)
    
    def execute_update(self, sql: str, mapping: Dict[str, str] = None):
        try:
            with pg.connect(dsn=self.dsn) as connection:
                with connection.cursor() as cursor:
                    try:
                        if mapping is None:
                            cursor.execute(sql)
                        else:
                            cursor.execute(sql, mapping)
                    
                    except Exception as e:
                        # TODO: Rethrow.
                        print(e)

        except Exception as e:
            # TODO: Rethrow.
            print(e)

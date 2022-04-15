from json import loads, dumps
import sqlite3

class Sql:
    @staticmethod
    def execute(query):
        result: tuple = None
        connection: 'Подключение' = sqlite3.connect(f'db/cache.db')
        cur: 'Курсор' = connection.cursor()
    
        try:
            cur.execute(query)
            result = cur.fetchall()

            connection.commit()
            connection.close()
        except Exception as e:
            print( f'Some error: {type(e)}, {query}' )
        
        finally:
            if result:
                return result
            return None
    
    @staticmethod
    def setUpUser(user_id: int) -> None:
        
        def isExist(user_id: int) -> bool:
            if Sql.execute(f''' SELECT count(user) FROM Cache WHERE user='{user_id}' ''')[0][0]:
                return True
            return False
        
        if not(isExist(user_id)):
            Sql.execute(f"insert into Cache (user, c1, c2, c3) VALUES ('{user_id}', 0, 0, 0)")
    
    @staticmethod
    def setUp() -> None:
        
        def isExists() -> bool:
            if Sql.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Cache' ''')[0][0]:
                return True
            return False
        
        if not(isExists()):
            Sql.execute(''' CREATE TABLE Cache (user, c1, c2, c3) ''')
    
    @staticmethod
    def updateCache(user: int, slot: str, value: str) -> None:
        Sql.execute(f''' UPDATE Cache set {slot}='{value}' where user='{user}' ''')
    
    @staticmethod
    def getCache(user):
        return Sql.execute(f''' SELECT * from Cache where user="{user}" ''')
import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'DB')

class DBhandler:
    def __init__(self):
        pass
    def addUser(self,nazwa_uzytkownika, preferencje): 
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()

            insert_query = '''
            INSERT INTO Użytkownik (nazwa_uzytkownika, preferencje)
            VALUES (?, ?);
            '''
            
            cursor.execute(insert_query, (nazwa_uzytkownika, preferencje))
            connection.commit()
            print("Record inserted successfully!")
    
    def updateUser(self,new_name, old_name): 
            with sqlite3.connect(DB_PATH) as connection:
                cursor = connection.cursor()
    
                update_query = '''
                UPDATE Użytkownik 
                SET nazwa_uzytkownika = ?
                WHERE nazwa_uzytkownika = ?
                '''
              
                cursor.execute(update_query, (new_name, old_name))
                connection.commit()
                if cursor.rowcount > 0:
                 print(f"Sukces! Zaktualizowano wierszy: {cursor.rowcount}")
                else:
                    print(f"UWAGA: Nie znaleziono w bazie użytkownika o nazwie '{old_name}'!")
    def deleteUser(self,name): 
                with sqlite3.connect(DB_PATH) as connection:
                    cursor = connection.cursor()
        
                    delete_query = '''
                   DELETE FROM Użytkownik 
                  
                    WHERE nazwa_uzytkownika = ?
                    '''
                  
                    cursor.execute(delete_query, (name,))
                    connection.commit()
                    print(f"Deleted user record ")
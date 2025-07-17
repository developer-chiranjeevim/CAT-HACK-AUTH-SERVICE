from dotenv import load_dotenv
import os
import psycopg2
import bcrypt
from datetime import datetime



load_dotenv()
class Database:
    def hash_password(self, plain_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def __init__(self):
        self.database_connection = psycopg2.connect(
            host = os.getenv("DATABASE_HOST"),
            port = os.getenv("DATABASE_PORT"),
            password = os.getenv("DATABASE_PASSWORD"),
            database = os.getenv("DATABASE_NAME"),
            user= os.getenv("DATABASE_USER"),
        )

    def create_user(self, operator_id, operator_name, password ,mobile_number):
        hashed_password = self.hash_password(password)
        current_date = datetime.now()
        try:
            db_cursor = self.database_connection.cursor()
            db_cursor.execute('''INSERT INTO operator(operator_id, operator_name, password, working_hours ,last_break_time, mobile_number) VALUES(%s, %s, %s, %s, %s, %s);''' ,(operator_id, operator_name, hashed_password, 0, current_date,mobile_number))
            self.database_connection.commit()
            db_cursor.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def fetch_user(self, operator_id, password):
        try:
            db_cursor = self.database_connection.cursor()
            db_cursor.execute(
                '''SELECT password FROM operator WHERE operator_id = %s''',
                (operator_id,)
            )
            response = db_cursor.fetchone()
            print("Fetched Password Hash:", response)

            if response:
                stored_hashed_password = response[0]
                if self.verify_password(password, stored_hashed_password):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error fetching user:", e)
            return False


    

    
if __name__ == "__main__":
    #driver code
    db = Database()
    db.fetch_user("developer@gmail.com", "chiranthen54321")
    pass
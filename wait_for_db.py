import time
import pymysql
from sqlalchemy import create_engine

def wait_for_db(host, user, password, db_name):
    while True:
        try:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.close()
            print("MySQL is up - executing command")
            break
        except pymysql.MySQLError as e:
            print("MySQL is unavailable - sleeping")
            time.sleep(1)

if __name__ == "__main__":
    import sys
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    db_name = sys.argv[4]
    command = sys.argv[5:]
    wait_for_db(host, user, password, db_name)
    import subprocess
    subprocess.run(command)

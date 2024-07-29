import sys
import time
import pymysql
import subprocess

def wait_for_db(host, user, password, db):
    while True:
        try:
            connection = pymysql.connect(host=host, user=user, password=password, database=db)
            connection.close()
            break
        except pymysql.MySQLError as e:
            print("MySQL is unavailable - sleeping")
            time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Not enough arguments provided to wait_for_db.py")
        sys.exit(1)

    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    db_name = sys.argv[4]
    command = sys.argv[5:]

    wait_for_db(host, user, password, db_name)
    subprocess.run(command)

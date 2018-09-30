from datetime import datetime
import pymysql

connection = pymysql.connect(host='localhost', user='root', password='1234', db='flask_bbs', charset='utf8')
with connection.cursor() as cursor:
    sql = "INSERT INTO board(id,name,create_time) VALUES ('{}','{}','{}')"
    cursor.execute(sql.format(2, 'flask', datetime.now()))
    connection.commit()

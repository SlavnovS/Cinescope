import psycopg2
from psycopg2 import extras


try:
    connect_bd = psycopg2.connect(dbname = "db_movies",
                              user = "postgres",
                              password = "AmwFrtnR2",
                              host = "80.90.191.123",
                              port="31200")


    cursor = connect_bd.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT COUNT(%(id)s), %(price)s FROM movies WHERE price < %(price)s "
                   "GROUP BY price", {"price": "325", "id": "id"})
    record = cursor.fetchall()
    print(record)
    a = cursor.get_dsn_parameters()
    print(a)

except Exception as e:
    print(e)
finally:
    if cursor:
        cursor.close()

    if connect_bd:
        connect_bd.close()
        print("соединение закрыто")

'''Simple mysql wrapper'''


import config
import MySQLdb

cursor = MySQLdb.connect(**config.DB).cursor()

def sql(query, *args):
    cursor.execute(query, args)
    return cursor

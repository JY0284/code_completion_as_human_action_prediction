def db_connect(name):
    return None


# in project 'Data Manager'
# in file 'data_utils.py'

def save_data(output_file):
    # read and save data to a given file
    database = db_connect('raw_db')   # 1
    target_rows = database.execute(QUERY_SQL_CMD).get() # 2,3,4
    database.disconnect() # 5

    target_file = open(output_file, 'w') # 6
    target_file.write(target_rows) # 7
    target_file.close() # 8


"""
save data:
database : being db connect, 'dummy_db'
database : execute, 'dummy_sql_command'
database : get, @
target data ~ database : 这里是database最新的encoding结果 // database.execute('dummy_sql_command').get()
database : disconnect, @
target file : being open, 'tmp.txt' 'w'
target file : write, $target_data
target file : close, @
"""

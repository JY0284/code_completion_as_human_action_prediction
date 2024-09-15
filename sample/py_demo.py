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
# Project name and file name will be the part of the context information when modeling to action sequence, ignore in the following demo for simplicity.
save data:
database ~ db connect, 'raw_db'
database : execute, 'QUERY_SQL_CMD'
database : get, @
target rows ~ database // database.execute('dummy_sql_command').get()
database : disconnect, @
target file ~ open, 'tmp.txt' 'w'
target file : write, target rows
target file : close, @
"""

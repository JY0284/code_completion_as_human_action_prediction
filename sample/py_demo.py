def db_connect(name):
    return None


# without method parameters
# noinspection PyNoneFunctionAssignment,PyUnresolvedReferences
def save_data():
    # read and save data to a file, then close all
    database = db_connect('dummy_db')
    target_data = database.execute('dummy_sql_command').get()
    database.disconnect()

    target_file = open('tmp.txt', 'w')
    target_file.write(target_data)
    target_file.close()


"""
save data:
database :? db connect
database : execute
database : get
database : disconnect

// target_data = database.execute('dummy_sql_command').get()
target data ~ database : disconnect  

target file :? open
target file : write
target file : close
"""

import json
import os
import sys
src_path = os.path.curdir + "/backend/src"
print(src_path)
sys.path.insert(0, src_path)
from config.settings import Settings
import database.dao_helper_functions as ibm_db_interface
from database import db
# Test Data will be inserted in the order it appears in the test dataset
# ENSURE THE ORDER IS CORRECT (pay attention to foreign key, etc.)

#TESTS_DATA is structured like DICT{TABLE: [ROW, ROW, ...]}
TEST_DATA = json.load(open("backend/tests/test_data/test_set_1.json", "r"))
assert(isinstance(TEST_DATA, dict))
# DB_NAME: str = "DBGOLDFI"
creds: dict = json.load(open(Settings.db_config_file()))
DB_NAME: str = creds["db_name"]

connection = ibm_db_interface.get_pooled_connection(db._conn_str)
cursor = connection.cursor()

for table, rows in TEST_DATA.items():
    for row in rows:
        assert(isinstance(row, dict))
        columns = list(row.keys())
        row_data = list(row.values())
        insert_string= f"INSERT INTO {DB_NAME}.{table} ({", ".join(columns)}) VALUES ("
        insert_string += "?, " * len(row_data) 
        insert_string = insert_string[0:-2] + ")" # Replace last "," with ")"
        print(insert_string)
        print(row_data)
        cursor.execute(insert_string, row_data)

connection.commit()
connection.close()
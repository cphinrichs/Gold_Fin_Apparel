
#import ibm_db_dbi
import json
import os
from logger import log
from logger.logger_object import Level
from config.settings import Settings
from pathlib import Path

# clidriver_path = Path(__file__).parent.parent.parent.parent
# os.add_dll_directory(f"{clidriver_path}/bin")
# clidriver_path = f"{clidriver_path}/bin/amd64.VC12.CRT"

# os.environ["PATH"] = clidriver_path + ";" + os.environ.get("PATH", "")

project_root = Path(__file__).parent.parent.parent.parent
venv_path = project_root / ".venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

os.add_dll_directory(str(clidriver_bin))
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db
import ibm_db_dbi

class _Db2DAO:
    def __init__(self):
        try:
            config_path = Settings.db_config_file()
            with open(config_path, "r") as file:
                self.creds = json.load(file)
        
            self.conn_str = (
                f"DATABASE={self.creds["database"]};"
                f"HOSTNAME={self.creds["host"]};"
                f"PORT={self.creds["port"]};"
                f"PROTOCOL={self.creds["protocol"]};"
                f"AUTHENTICATION=SERVER;"
                f"UID={self.creds["username"]};"
                f"PWD={self.creds["password"]};"
            )

            self.conn = ibm_db_dbi.Connection(ibm_db.connect(self.conn_str, "", ""))
            self.cursor = self.conn.cursor()
            
            log.log(Level.INFO, "Successfully connected to Db2.")

            # test_dictionary = {}
            # test_dictionary["ascending"] = True
            # self.select_inventory(test_dictionary)
        except Exception as e:
            log.log(Level.CRITICAL, e.args[0])

    def create_order(self, order_data: dict):
        pass

    def select_inventory(self, search_fields: dict) -> list[tuple]:
        try:
            
            log.log(Level.DEBUG, "Preparing SQL query to display inventory...")
            sql = """
            SELECT * FROM USER13.Inventory
            """
            params = []


            for field in ["Size", "Style", "Material", "Color"]:
                if field in search_fields:
                    sql += f"WHERE {field} LIKE %?%"
                    params.append(search_fields[field])

            sql += "ORDER BY Price "
            if "ascending" in search_fields and search_fields["ascending"]:
                sql += "ASC;"
            else:
                sql += "DESC;"
            
            log.log(Level.DEBUG, "Executing query...")
            self.cursor.execute(sql, params)
            query_results = self.cursor.fetchall()

            return query_results
        except Exception as e:
            log.log(Level.ERROR, "Error occured during inventory query: " + e.args[0])
            raise Exception(e.args[0])


    def select_designs(self, search_fields: dict):
        pass
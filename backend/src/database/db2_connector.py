
#import ibm_db_dbi
import json
import os
from logger import log
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

class _Db2DAO:
    def __init__(self):
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

        self.conn = ibm_db.connect(self.conn_str, "", "")
        log.log("INFO", "Successfully connected to Db2")

    def create_order(self, order_data: dict):
        pass

    def select_inventory(self, search_fields: dict):
        try:
            sql = """
            SELECT * FROM Inventory
            """
            params = []

            for field in ["Size", "Style", "Material", "Color"]:
                if field in search_fields:
                    sql += f"WHERE {field} LIKE %?%"
                    params.append(search_fields[field])

            sql += "ORDER BY Price "
            if "ascending" in search_fields & search_fields["ascending"]:
                sql += "ASC;"
            else:
                sql += "DESC;"
            
            if len(params) >= 1:
                stmt_insert = ibm_db.prepare(self.conn, sql)
                query_results = ibm_db.execute_many(stmt_insert, params)
            else:
                query_results = ibm_db.exec_immediate(self.conn, sql)

            return True, query_results
        except:
            return False, "Unknown error occurred"


    def select_designs(self, search_fields: dict):
        pass
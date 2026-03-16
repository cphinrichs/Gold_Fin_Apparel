
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
venv_path = project_root / "venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

os.add_dll_directory(str(clidriver_bin))
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db
import ibm_db_dbi

class _Db2DAO:
    def __init__(self):
        self.creds = None
        self.conn = None
        self.cursor = None
        
        try:
            config_path = Settings.db_config_file()
            with open(config_path, "r") as file:
                self.creds = json.load(file)
        
            self.conn_str = (
                f"DATABASE={self.creds['db_instance']};"
                f"HOSTNAME={self.creds['host']};"
                f"PORT={self.creds['port']};"
                f"PROTOCOL={self.creds['protocol']};"
                f"AUTHENTICATION=SERVER;"
                f"UID={self.creds['username']};"
                f"PWD={self.creds['password']};"
            )

            self.conn = ibm_db_dbi.Connection(ibm_db.connect(self.conn_str, "", ""))
            self.cursor = self.conn.cursor()
            
            log.log(Level.INFO, "Successfully connected to Db2.")

            # test_dictionary = {}
            # test_dictionary["ascending"] = True
            # self.select_inventory(test_dictionary)
        except Exception as e:
            log.log(Level.CRITICAL, f"Failed to initialize DB2 connection: {e}")
            raise

    def create_order(self, order_data: dict):
        # TODO: check if customer is in database already, and if not, add them
        # TODO: add the order to the database
        # TODO: for each order item in the request, add it to the database
        
        
        
        pass

    def select_inventory(self, search_fields: dict) -> list[tuple]:
        try:
            
            log.log(Level.DEBUG, "Preparing SQL query to display inventory...")
            sql = f"""
            SELECT 
                I.PRODUCT_ID,
                SZ.NAME AS SIZE,
                ST.NAME AS STYLE,
                M.NAME AS MATERIAL,
                I.COLOR,
                I.STOCK
            FROM {self.creds["db_name"]}.INVENTORY I
            LEFT JOIN {self.creds["db_name"]}.SIZES SZ
                ON I.SIZE_ID = SZ.ID
            LEFT JOIN {self.creds["db_name"]}.STYLES ST
                ON I.STYLE_ID = ST.ID
            LEFT JOIN {self.creds["db_name"]}.MATERIALS M
                ON I.MATERIAL_ID = M.ID
            """
            params = []

            for field in ["Size", "Style", "Material", "Color"]:
                if field in search_fields:
                    if len(params) == 0:
                        sql += f" WHERE "
                    else:
                        sql += f" AND "
                    
                    if field == "Size":
                        sql += "SZ.NAME = ?"
                    elif field == "Style":
                        sql += "ST.NAME = ?"
                    elif field == "Material":
                        sql += "M.NAME = ?"
                    elif field == "Color":
                        sql += "I.COLOR = ?"
                    
                    params.append(search_fields[field])

            sql += " ORDER BY I.STOCK "
            if "Ascending" in search_fields and search_fields["Ascending"].lower() == "true":
                sql += "ASC;"
            else:
                sql += "DESC;"

            print(sql)
            
            log.log(Level.DEBUG, "Executing query...")
            self.cursor.execute(sql, params)
            query_results = self.cursor.fetchall()

            return query_results
        except Exception as e:
            log.log(Level.ERROR, "Error occured during inventory query: " + e.args[0])
            raise Exception(e.args[0])

    def select_designs(self, search_fields: dict) -> list[tuple]:
        try:
            
            log.log(Level.DEBUG, "Preparing SQL query to display designs...")
            
            sql = f"""
            SELECT * FROM {self.creds["db_name"]}.DESIGNS
            """
            params = []

            if "Min_Price" in search_fields and not "Max_Price" in search_fields:
                sql += f" WHERE Price >= ?"
                params.append(search_fields["Min_Price"])
            elif "Max_Price" in search_fields and not "Min_Price" in search_fields:
                sql += f" WHERE Price <= ?"
                params.append(search_fields["Max_Price"])
            elif "Min_Price" in search_fields and "Max_Price" in search_fields:
                sql += f" WHERE Price BETWEEN ? AND ?"
                params.append(search_fields["Min_Price"])
                params.append(search_fields["Max_Price"])

            if "Name" in search_fields:
                if len(params) == 0:
                    sql += " WHERE Name LIKE %?%"
                else:
                    sql += " AND Name LIKE %?%"
                params.append(search_fields["Name"])

            if "Sort_By_Price" in search_fields and search_fields["Sort_By_Price"].lower() == "true":
                sql += " ORDER BY Price "
            else:
                sql += " ORDER BY Name "
            if "Ascending" in search_fields and search_fields["Ascending"].lower() == "true":
                sql += "ASC;"
            else:
                sql += "DESC;"

            
            
            log.log(Level.DEBUG, "Executing query...")
            self.cursor.execute(sql, params)
            query_results = self.cursor.fetchall()

            return query_results
        except Exception as e:
            log.log(Level.ERROR, "Error occured during designs query: " + e.args[0])
            raise Exception(e.args[0])
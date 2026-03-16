
#import ibm_db_dbi
import json
import os
from logger import log
from logger.logger_object import Level
from config.settings import Settings
from pathlib import Path
from order_validation.order_validator import Order
import datetime

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

            conn = ibm_db_dbi.Connection(ibm_db.connect(self._conn_str, "", ""))
            conn.close()
            
            log.log(Level.INFO, "Successfully connected to Db2.")
            print("test")
            # test_dictionary["ascending"] = True

            # test_dictionary = {
            #     "Customer": "Kara Lynch",
            #     "Items": [
            #         {
            #             "Product_Id": 1,
            #             "Design_Id": 1,
            #             "Quantity": 3
            #         }
            #     ]
            # }
            # self.create_order(Order(test_dictionary))
        except Exception as e:
            log.log(Level.CRITICAL, f"Failed to initialize DB2 connection: {e}")
            raise

    def get_pooled_connection(self) -> ibm_db_dbi.Connection:
        """Gets a connection with ibm_db_dbi"""
        new_connection = ibm_db.pconnect(self._conn_str,"","")
        assert(isinstance(new_connection, ibm_db.IBM_DBConnection))
        return ibm_db_dbi.Connection(new_connection)

    def create_order(self, order_data: Order):
        log.log(Level.DEBUG, "Successfully connected to Db2.")
        customer_check_sql = f"""
        SELECT * FROM {self.creds["db_name"]}.Customers
        WHERE Name = ?;
        """
        conn = self.get_pooled_connection()
        cursor = conn.cursor()


        cursor.execute(customer_check_sql, [order_data.get_customer()["Name"]])
        customer_query_results = cursor.fetchall()

        print(customer_query_results)

        if len(customer_query_results) == 0:
            cust_id = self.add_customer(conn, order_data.get_customer())
        else:
            cust_id = customer_query_results[0][0]

        add_order_sql = f"""
        SELECT ID
        FROM FINAL TABLE
        (INSERT INTO {self.creds["db_name"]}.Orders (Customer_ID, Total_Price, Order_Date)
        VALUES (?, ?, ?));
        """
        
        order_price = self.get_order_price(order_data)

        current_time = datetime.datetime.today().strftime("%Y-%m-%d")

        order_params = [cust_id, order_price, current_time]

        cursor.execute(add_order_sql, order_params)
        order_id = cursor.fetchall()[0][0]
        
        order_items_sql = f"""
        INSERT INTO {self.creds["db_name"]}.Order_Items (Order_ID, Product_Id, Quantity, Design_Id, Price)
        VALUES(?, ?, ?, ?, ?)"""

        order_items = order_data.get_items()

        for item in order_items:
            order_items_params = [order_id, item["Product_Id"], item["Quantity"], item["Design_Id"], self.get_item_price(item)]
            cursor.execute(order_items_sql, order_items_params)

        conn.close()
        
        
    def add_customer(self, conn: ibm_db_dbi.Connection, cust_data: dict) -> int:
        sql = f"""
        SELECT ID
        FROM FINAL TABLE
        (INSERT INTO {self.creds["db_name"]}.Customers (Name, Address)
        VALUES(?, ?));
        """
        cursor = conn.cursor()

        log.log(Level.DEBUG, "Executing add customer query...")
        cursor.execute(sql, [cust_data["Name"], cust_data["Address"]])
        query_results = cursor.fetchall()[0][0]
        # print(query_results)
        
        if isinstance(query_results, int):
            return query_results
        
        
        return 0
    
    def get_order_price(self, order_data: Order) -> float:
        return 0.0
    
    def get_item_price(self, item_data: dict) -> float:
        return 0.0
        

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

            conn = self.get_pooled_connection()
            cursor = conn.cursor()
            log.log(Level.DEBUG, "Executing query...")
            cursor.execute(sql, params)
            query_results = cursor.fetchall()

            conn.close()
            return query_results
        
            #TODO: refactor to include left joins and price calc
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

            
            
            conn = self.get_pooled_connection()
            cursor = conn.cursor()

            log.log(Level.DEBUG, "Executing query...")
            cursor.execute(sql, params)
            query_results = cursor.fetchall()

            conn.close()
            return query_results
        except Exception as e:
            log.log(Level.ERROR, "Error occured during designs query: " + str(e.args))
            raise Exception(e.args[0])
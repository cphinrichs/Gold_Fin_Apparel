
#import ibm_db_dbi
import json
import os
from logger import log
from logger.logger_object import Level
from config.settings import Settings
from pathlib import Path
from order_validation.order_validator import Order
import datetime
import dao_helper_functions as helper

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
        # self.creds = None
        self.conn = None
        self.cursor = None
        
        try:
            config_path = Settings.db_config_file()
            with open(config_path, "r") as file:
                self.creds = json.load(file)
        
            self._conn_str = (
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
            raise Exception

    def create_order(self, order_data: Order):
        log.log(Level.DEBUG, "Initializing SQL query to check if the customer exists...")
        customer_check_sql = f"""
        SELECT * FROM {self.creds["db_name"]}.CUSTOMERS
        WHERE NAME = ?;
        """
        conn = helper.get_pooled_connection(self._conn_str)
        cursor = conn.cursor()


        cursor.execute(customer_check_sql, [order_data.get_customer()["Name"]])
        customer_query_results = cursor.fetchall()

        print(customer_query_results)

        if len(customer_query_results) == 0:
            cust_id = self.add_customer_and_return_id(conn, order_data.get_customer())
        else:
            cust_id = customer_query_results[0][0]

        add_order_sql = f"""
        SELECT ID
        FROM FINAL TABLE
        (INSERT INTO {self.creds["db_name"]}.ORDERS (CUSTOMER_ID, TOTAL, ORDER_DATE)
        VALUES (?, ?, ?));
        """
        
        order_price = helper.get_order_price(order_data)

        current_time = datetime.datetime.today().strftime("%Y-%m-%d")

        order_params = [cust_id, order_price, current_time]

        cursor.execute(add_order_sql, order_params)
        order_id = cursor.fetchall()[0][0]
        
        order_items_sql = f"""
        INSERT INTO {self.creds["db_name"]}.ORDER_ITEMS (ORDER_ID, PRODUCT_ID, QUANTITY, DESIGN_ID, PRICE)
        VALUES(?, ?, ?, ?, ?)"""

        order_items = order_data.get_items()

        for item in order_items:
            order_items_params = [order_id, item["Product_Id"], item["Quantity"], item["Design_Id"], helper.get_item_price(item)]
            cursor.execute(order_items_sql, order_items_params)

        conn.close()
    
    def lookup_inventory_by_id(self, conn: ibm_db_dbi.Connection, id_list: list[int]) -> list[dict]:
        # this method is only meant for use by other parts of the DAO
        # which is why it takes a connection as input

        if len(id_list) == 0:
            log.log(Level.ERROR, "Aborting inventory lookup by id. No ids were given -- this likely means an empty order was made.")
            return [{}]
        
        sql = f"""
        SELECT 
            INVENTORY.PRODUCT_ID,
            SIZES.NAME AS SIZE,
            STYLES.NAME AS STYLE,
            MATERIAL.NAME AS MATERIAL,
            INVENTORY.COLOR,
            INVENTORY.STOCK,
            SIZES.PRICE_FACTOR AS SIZE_FACTOR,
            STYLES.PRICE AS STYLE_PRICE,
            MATERIAL.PRICE AS MATERIAL_PRICE,
        FROM {self.creds["db_name"]}.INVENTORY
        LEFT JOIN {self.creds["db_name"]}.SIZES
            ON INVENTORY.SIZE_ID = SIZES.ID
        LEFT JOIN {self.creds["db_name"]}.STYLES
            ON INVENTORY.STYLE_ID = STYLES.ID
        LEFT JOIN {self.creds["db_name"]}.MATERIALS
            ON INVENTORY.MATERIAL_ID = MATERIALS.ID
        WHERE INVENTORY.PRODUCT_ID IN (
        """

        params = []
        
        for id in id_list:
            sql += "?"
            if len(params) < len(id_list) - 1:
                sql += ", "
            elif len(params) == len(id_list) - 1:
                sql += ");"
            params.append(id)
        
        cursor = conn.cursor()
        cursor.execute(sql, params)
        query_results = cursor.fetchall()

        inventory_list = []
        for row in query_results:
            inventory_list.append(helper.convert_inventory_data(row))
        
        return inventory_list
    
    def lookup_design_prices_by_id(self, conn: ibm_db_dbi.Connection, id_list: list[int]) -> list[dict]:
        # this method is only meant for use by other parts of the DAO
        # which is why it takes a connection as input
        sql = f"""
        SELECT ID, PRICE
        FROM {self.creds["db_name"]}.DESIGNS
        WHERE ID IN (
        """

        if len(id_list) == 0:
            log.log(Level.ERROR, "Aborting inventory lookup by id. No ids were given -- this likely means an empty order was made.")
            return [{}]

        params = []
        
        for id in id_list:
            sql += "?"
            if len(params) < len(id_list) - 1:
                sql += ", "
            elif len(params) == len(id_list) - 1:
                sql += ");"
            params.append(id)
        
        cursor = conn.cursor()
        cursor.execute(sql, params)
        query_results = cursor.fetchall()
        
        inventory_list = []
        for row in query_results:
            inventory_list.append(helper.convert_inventory_data(row))
        
        return inventory_list
    
    
        
        
    def add_customer_and_return_id(self, conn: ibm_db_dbi.Connection, cust_data: dict) -> int:
        sql = f"""
        SELECT ID
        FROM FINAL TABLE
        (INSERT INTO {self.creds["db_name"]}.CUSTOMERS (NAME, ADDRESS)
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
        

    def select_inventory(self, search_fields: dict) -> list[dict]:
        try:
            
            log.log(Level.DEBUG, "Preparing SQL query to display inventory...")
            sql = f"""
            SELECT 
                INVENTORY.PRODUCT_ID,
                SIZES.NAME AS SIZE,
                STYLES.NAME AS STYLE,
                MATERIAL.NAME AS MATERIAL,
                INVENTORY.COLOR,
                INVENTORY.STOCK,
                SIZES.PRICE_FACTOR AS SIZE_FACTOR,
                STYLES.PRICE AS STYLE_PRICE,
                MATERIAL.PRICE AS MATERIAL_PRICE
            FROM {self.creds["db_name"]}.INVENTORY
            LEFT JOIN {self.creds["db_name"]}.SIZES
                ON INVENTORY.SIZE_ID = SIZES.ID
            LEFT JOIN {self.creds["db_name"]}.STYLES
                ON INVENTORY.STYLE_ID = STYLES.ID
            LEFT JOIN {self.creds["db_name"]}.MATERIALS
                ON INVENTORY.MATERIAL_ID = MATERIALS.ID
            """
            params = []

            for field in ["Size", "Style", "Material", "Color"]:
                if field in search_fields:
                    if len(params) == 0:
                        sql += f" WHERE "
                    else:
                        sql += f" AND "

                    if field == "Color":
                        sql += "INVENTORY.COLOR = ?"
                    else:
                        sql += f"{field}S.NAME = ?"
                    
                    params.append(search_fields[field])

            sql += " ORDER BY INVENTORY.STOCK "
            if "Ascending" in search_fields and search_fields["Ascending"].lower() == "true":
                sql += "ASC;"
            else:
                sql += "DESC;"

            print(sql)

            conn = helper.get_pooled_connection(self._conn_str)
            cursor = conn.cursor()
            log.log(Level.DEBUG, "Executing query...")
            cursor.execute(sql, params)
            query_results = cursor.fetchall()

            conn.close()

            

            inventory_list = []
            for row in query_results:
                inventory_list.append(helper.convert_inventory_data(row))
            
            return inventory_list
        
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
                sql += f" WHERE PRICE >= ?"
                params.append(search_fields["Min_Price"])
            elif "Max_Price" in search_fields and not "Min_Price" in search_fields:
                sql += f" WHERE PRICE <= ?"
                params.append(search_fields["Max_Price"])
            elif "Min_Price" in search_fields and "Max_Price" in search_fields:
                sql += f" WHERE PRICE BETWEEN ? AND ?"
                params.append(search_fields["Min_Price"])
                params.append(search_fields["Max_Price"])

            if "Name" in search_fields:
                if len(params) == 0:
                    sql += " WHERE NAME LIKE %?%"
                else:
                    sql += " AND NAME LIKE %?%"
                params.append(search_fields["Name"])

            if "Sort_By_Price" in search_fields and search_fields["Sort_By_Price"].lower() == "true":
                sql += " ORDER BY PRICE "
            else:
                sql += " ORDER BY NAME "
            if "Ascending" in search_fields and search_fields["Ascending"].lower() == "true":
                sql += "ASC;"
            else:
                sql += "DESC;"

            
            
            conn = helper.get_pooled_connection(self._conn_str)
            cursor = conn.cursor()

            log.log(Level.DEBUG, "Executing query...")
            cursor.execute(sql, params)
            query_results = cursor.fetchall()
            conn.close()
            
            


            return query_results
        except Exception as e:
            log.log(Level.ERROR, "Error occured during designs query: " + str(e.args))
            raise Exception(e.args[0])
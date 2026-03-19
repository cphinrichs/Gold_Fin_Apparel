
#import ibm_db_dbi
import json
import os
from logger import log
from logger.logger_object import Level
from config.settings import Settings
from pathlib import Path
from order_validation.order_validator import Order
import datetime
from database import dao_helper_functions as helper

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

        except Exception as e:
            log.log(Level.CRITICAL, f"Failed to initialize DB2 connection: {e}")
            raise Exception

    def create_order(self, order_data: Order):
        #step 0: ensure that there are items attached to the order
        order_items = order_data.get_items()
        if len(order_items) == 0:
            log.log(Level.ERROR, "Aborting order. No items were included.")
            raise IndexError
        
        #step 1: validate that we have everything in stock. and if we do, get its pricing data
        log.log(Level.DEBUG, "Checking price information and ensuring all items are in stock...")
        order_items = order_data.get_items()

        conn = helper.get_pooled_connection(self._conn_str)
        
        product_data, design_data = self.validate_and_lookup_item_prices(conn, order_data)

        #step 2: calculate the prices for the order and for each item
        log.log(Level.DEBUG, "Calculating all item prices...")
        order_price, order_items = helper.get_order_price(product_data, design_data, order_items)

        
        

        #step 3: check if the customer exists in the database
        #if they do, get their ID number. if they don't, add them and get the new ID
        log.log(Level.DEBUG, "Initializing SQL query to check if the customer exists...")
        customer_check_sql = f"""
        SELECT * FROM {self.creds["db_name"]}.CUSTOMERS
        WHERE NAME = ?;
        """
        cursor = conn.cursor()


        cursor.execute(customer_check_sql, [order_data.get_customer()["Name"]])
        customer_query_results = cursor.fetchall()

        # print(customer_query_results)

        if len(customer_query_results) == 0:
            log.log(Level.DEBUG, "Customer not found. Adding to database...")
            cust_id = self.add_customer_and_return_id(conn, order_data.get_customer())
        else:
            log.log(Level.DEBUG, "Customer found and ID retrieved.")
            cust_id = customer_query_results[0][0]
        
        #step 4: add the order to the table using the customer's ID and the order data
        #then get the order ID for the next step
        log.log(Level.DEBUG, "Preparing SQL query to add order...")
        add_order_sql = f"""
        SELECT ID
        FROM FINAL TABLE
        (INSERT INTO {self.creds["db_name"]}.ORDERS (CUSTOMER_ID, TOTAL_PRICE, ORDER_DATE)
        VALUES (?, ?, ?));
        """

        current_time = datetime.datetime.today().strftime("%Y-%m-%d")


        order_params = [cust_id, order_price, current_time]

        log.log(Level.DEBUG, "Adding order...")
        cursor.execute(add_order_sql, order_params)
        order_id = cursor.fetchall()[0][0]

        #step 5: add each of the order items to the table
        log.log(Level.DEBUG, "Order added. Preparing SQL queries to add order items...")        
        order_items_sql = f"""
        INSERT INTO {self.creds["db_name"]}.ORDER_ITEMS (ORDER_ID, PRODUCT_ID, QUANTITY, DESIGN_ID, PRICE)
        VALUES(?, ?, ?, ?, ?)"""
        
        log.log(Level.DEBUG, "Adding order items...")   
        for item in order_items:
            order_items_params = [order_id, item["Product_Id"], item["Quantity"], item["Design_Id"], item["Unit_Price"]]
            cursor.execute(order_items_sql, order_items_params)

        #step 6: for each order item, decrement the inventory table by its quantity
        log.log(Level.DEBUG, "Order items added. Preparing SQL inventory stock counts...")   
        decrement_items_sql = f"""
        UPDATE {self.creds["db_name"]}.INVENTORY
        SET STOCK = STOCK - ?
        WHERE PRODUCT_ID = ?
        """

        for item in order_items:
            decrement_items_params = [item["Quantity"], item["Product_Id"]]
            cursor.execute(decrement_items_sql, decrement_items_params)

        conn.commit()
        conn.close()
    
    def validate_and_lookup_item_prices (self, conn: ibm_db_dbi.Connection, order_data: Order) -> tuple[dict[int, dict[str, int | float]], dict[int, float]]:
        order_items = order_data.get_items()
        
        product_ids = set()
        design_ids = set()
        for item in order_items:
            product_ids.add(item["Product_Id"])
            design_ids.add(item["Design_Id"])
        
        product_lookup_sql = f"""
        SELECT 
            INV.PRODUCT_ID,
            INV.STOCK,
            SZ.PRICE_FACTOR AS SIZE_FACTOR,
            ST.PRICE AS STYLE_PRICE,
            MAT.PRICE AS MATERIAL_PRICE
        FROM {self.creds["db_name"]}.INVENTORY AS INV
        LEFT JOIN {self.creds["db_name"]}.SIZES AS SZ
            ON INV.SIZE_ID = SZ.ID
        LEFT JOIN {self.creds["db_name"]}.STYLES AS ST
            ON INV.STYLE_ID = ST.ID
        LEFT JOIN {self.creds["db_name"]}.MATERIALS AS MAT
            ON INV.MATERIAL_ID = MAT.ID
        WHERE INV.PRODUCT_ID IN (
        """

        product_lookup_params = []
        
        for id in product_ids:
            product_lookup_sql += "?"
            if len(product_lookup_params) < len(product_ids) - 1:
                product_lookup_sql += ", "
            elif len(product_lookup_params) == len(product_ids) - 1:
                product_lookup_sql += ");"
            product_lookup_params.append(id)
        
        cursor = conn.cursor()
        cursor.execute(product_lookup_sql, product_lookup_params)
        product_results = cursor.fetchall()

        inventory_dict = {}
        for row in product_results:
            inventory_dict[row[0]] = helper.convert_inventory_price_data(row)
        item = {}

        try:
            for item in order_items:
                assert item["Quantity"] <= inventory_dict[item["Product_Id"]]["Stock"]
        except AssertionError:
            log.log(Level.ERROR, "Aborting order. Insufficient stock for item of id " + item["Product_Id"])
            raise Exception
        
        design_lookup_sql = f"""
        SELECT ID, PRICE 
        FROM {self.creds["db_name"]}.DESIGNS
        WHERE ID IN (
        """

        design_lookup_params = []
        
        for id in design_ids:
            design_lookup_sql += "?"
            if len(design_lookup_params) < len(design_ids) - 1:
                design_lookup_sql += ", "
            elif len(design_lookup_params) == len(design_ids) - 1:
                design_lookup_sql += ");"
            design_lookup_params.append(id)

        # print(design_lookup_sql)
        
        cursor.execute(design_lookup_sql, design_lookup_params)
        design_results = cursor.fetchall()

        design_dict = {}

        for row in design_results:
            # print(row)
            design_dict[row[0]] = row[1]

        return inventory_dict, design_dict
        
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
            INV.PRODUCT_ID,
            SZ.NAME AS SIZE,
            ST.NAME AS STYLE,
            MAT.NAME AS MATERIAL,
            INV.COLOR AS COLOR,
            INV.STOCK,
            SZ.PRICE_FACTOR AS SIZE_FACTOR,
            ST.PRICE AS STYLE_PRICE,
            MAT.PRICE AS MATERIAL_PRICE
            FROM {self.creds["db_name"]}.INVENTORY AS INV
            LEFT JOIN {self.creds["db_name"]}.SIZES AS SZ
                ON INV.SIZE_ID = SZ.ID
            LEFT JOIN {self.creds["db_name"]}.STYLES AS ST
                ON INV.STYLE_ID = ST.ID
            LEFT JOIN {self.creds["db_name"]}.MATERIALS AS MAT
                ON INV.MATERIAL_ID = MAT.ID
            """
            params = []

            field_dict = {
                "Size": "SZ.NAME",
                "Style": "ST.NAME",
                "Material": "MAT.NAME",
                "Color": "INV.COLOR"
            }

            for field in ["Size", "Style", "Material", "Color"]:
                if field in search_fields:
                    if len(params) == 0:
                        sql += f" WHERE "
                    else:
                        sql += f" AND "

                    sql += f"{field_dict[field]} = ?"
                    params.append(search_fields[field])

            sql += f"\nORDER BY {self.creds["db_name"]}.INVENTORY.STOCK "
            if "Ascending" in search_fields and search_fields["Ascending"].lower() == "true":
                sql += "ASC;"
            else:
                sql += "DESC;"

            # print(sql)

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

            
            log.log(Level.DEBUG, "SQL assembled. Connecting to database...")
            
            conn = helper.get_pooled_connection(self._conn_str)
            cursor = conn.cursor()

            log.log(Level.DEBUG, "Executing query...")
            cursor.execute(sql, params)
            query_results = cursor.fetchall()
            conn.close()
            
            


            log.log(Level.DEBUG, "Query successful. Returning results...")
            return query_results
        except Exception as e:
            log.log(Level.ERROR, "Error occured during designs query: " + str(e.args))
            raise Exception(e.args[0])
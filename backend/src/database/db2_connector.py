
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
        #step 0: ensure that there are items attached to the order
        order_items = order_data.get_items()
        if len(order_items) == 0:
            log.log(Level.ERROR, "Aborting order. No items were included.")
            raise IndexError
        
        #step 1: validate that we have everything in stock. and if we do, get its pricing data
        log.log(Level.DEBUG, "Checking price information and ensuring all items are in stock...")
        order_items = order_data.get_items()

        conn = helper.get_pooled_connection(self._conn_str)
        
        price_data = self.validate_and_lookup_item_prices(conn, order_data)

        #step 2: calculate the prices for the order and for each item

        order_price, order_items = helper.get_order_price(price_data, order_items)

        
        

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

        print(customer_query_results)

        if len(customer_query_results) == 0:
            cust_id = self.add_customer_and_return_id(conn, order_data.get_customer())
        else:
            cust_id = customer_query_results[0][0]
        
        #step 4: add the order to the table using the customer's ID and the order data
        #then get the order ID for the next step
        add_order_sql = f"""
        SELECT ID
        FROM FINAL TABLE
        (INSERT INTO {self.creds["db_name"]}.ORDERS (CUSTOMER_ID, TOTAL, ORDER_DATE)
        VALUES (?, ?, ?));
        """

        current_time = datetime.datetime.today().strftime("%Y-%m-%d")


        order_params = [cust_id, order_price, current_time]

        cursor.execute(add_order_sql, order_params)
        order_id = cursor.fetchall()[0][0]

        #step 5: add each of the order items to the table

        
        order_items_sql = f"""
        INSERT INTO {self.creds["db_name"]}.ORDER_ITEMS (ORDER_ID, PRODUCT_ID, QUANTITY, DESIGN_ID, PRICE)
        VALUES(?, ?, ?, ?, ?)"""

        for item in order_items:
            order_items_params = [order_id, item["Product_Id"], item["Quantity"], item["Design_Id"], helper.get_item_price(item)]
            cursor.execute(order_items_sql, order_items_params)

        #step 6: for each order item, decrement the inventory table by its quantity

        conn.close()
    
    def validate_and_lookup_item_prices (self, conn: ibm_db_dbi.Connection, order_data: Order) -> dict[int, dict[str, int | float]]:
        order_items = order_data.get_items()
        
        product_ids, design_ids = set()
        for item in order_items:
            product_ids.add(item["Product_Id"])
            design_ids.add(item["Design_Id"])
        
        product_lookup_sql = f"""
        SELECT 
            INVENTORY.PRODUCT_ID,
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
        
        for id in product_ids:
            product_lookup_sql += "?"
            if len(params) < len(product_ids) - 1:
                product_lookup_sql += ", "
            elif len(params) == len(product_ids) - 1:
                product_lookup_sql += ");"
            params.append(id)
        
        cursor = conn.cursor()
        cursor.execute(product_lookup_sql, params)
        query_results = cursor.fetchall()

        inventory_dict = {}
        for row in query_results:
            inventory_dict[row[0]] = helper.convert_inventory_price_data(row)
        item = {}

        try:
            for item in order_items:
                assert item["Quantity"] <= inventory_dict[item["Product_Id"]]["Stock"]
        except AssertionError:
            log.log(Level.ERROR, "Aborting order. Insufficient stock for item of id " + item["Product_Id"])
            raise Exception

        return inventory_dict
        
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
                {self.creds["db_name"]}.INVENTORY.PRODUCT_ID,
                {self.creds["db_name"]}.SIZES.NAME AS SIZE,
                {self.creds["db_name"]}.STYLES.NAME AS STYLE,
                {self.creds["db_name"]}.MATERIALS.NAME AS MATERIAL,
                {self.creds["db_name"]}.INVENTORY.COLOR,
                {self.creds["db_name"]}.INVENTORY.STOCK,
                {self.creds["db_name"]}.SIZES.PRICE_FACTOR AS SIZE_FACTOR,
                {self.creds["db_name"]}.STYLES.PRICE AS STYLE_PRICE,
                {self.creds["db_name"]}.MATERIALS.PRICE AS MATERIAL_PRICE
            FROM {self.creds["db_name"]}.INVENTORY
            LEFT JOIN {self.creds["db_name"]}.SIZES
                ON {self.creds["db_name"]}.INVENTORY.SIZE_ID = {self.creds["db_name"]}.SIZES.ID
            LEFT JOIN {self.creds["db_name"]}.STYLES
                ON {self.creds["db_name"]}.INVENTORY.STYLE_ID = {self.creds["db_name"]}.STYLES.ID
            LEFT JOIN {self.creds["db_name"]}.MATERIALS
                ON {self.creds["db_name"]}.INVENTORY.MATERIAL_ID = {self.creds["db_name"]}.MATERIALS.ID
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

            sql += f" ORDER BY {self.creds["db_name"]}.INVENTORY.STOCK "
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
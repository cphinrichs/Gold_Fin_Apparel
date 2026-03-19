import sys
import os
import json

src_path = os.path.curdir + "/backend/src"
print(src_path)
sys.path.insert(0, src_path)

from config.settings import Settings
import database.dao_helper_functions as ibm_db_interface
from database import db


creds: dict = json.load(open(Settings.db_config_file()))
DB_NAME: str = creds["db_name"]

# TABLESPACES: {TABLENAMES: (DDL, UNIQUE INDEXED KEY, LIST OF INDEXED KEYS)} 
TABLESPACES_AND_TABLES: dict[str, dict[str, tuple[str, str, list[str]]]] = {
    # Do not include semicolons in ddl
    "TSSTYLES": {"STYLES": (f"""
            ID INT UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
            NAME VARCHAR(50) NOT NULL UNIQUE,
            PRICE DECIMAL(10,2) WITH DEFAULT NULL,
            CONSTRAINT PK_STYLES
                PRIMARY KEY (ID)
                            """, "ID ASC", ["NAME ASC", "PRICE ASC"])},
    "TSMATERS": {"MATERIALS": (f"""
            ID INT UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
            NAME VARCHAR(20) NOT NULL UNIQUE,
            PRICE DECIMAL(10,2) WITH DEFAULT NULL,
            CONSTRAINT PK_MATERIALS
                PRIMARY KEY (ID)
                            """, "ID ASC", ["NAME ASC", "PRICE ASC"])},
    "TSSIZES": {"SIZES": (f"""
            ID INT UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
            NAME CHAR(2) NOT NULL UNIQUE,
            PRICE_FACTOR FLOAT NOT NULL,
            CONSTRAINT PK_SIZES
                PRIMARY KEY (ID)
                """, "ID ASC", ["NAME ASC", "PRICE_FACTOR ASC"])},
    "TSDSIGNS": {"DESIGNS": (f"""
            ID INT UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
            NAME VARCHAR(50) NOT NULL,
            PRICE DECIMAL(10,2) WITH DEFAULT NULL,
            CONSTRAINT PK_DESIGNS
                PRIMARY KEY (ID)
                """ , "ID ASC", ["NAME ASC", "PRICE ASC"])},
    "TSINVENT": {"INVENTORY": (f"""
            PRODUCT_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            COLOR CHAR(6) NOT NULL,
            MATERIAL_ID INTEGER NOT NULL,
            STYLE_ID INTEGER NOT NULL,
            SIZE_ID INTEGER NOT NULL,
            STOCK INT NOT NULL,
            CONSTRAINT FK_MATERIAL
                FOREIGN KEY (MATERIAL_ID)
                REFERENCES {DB_NAME}.MATERIALS (ID)
                ON DELETE RESTRICT,
            CONSTRAINT FK_STYLE
                FOREIGN KEY (STYLE_ID)
                REFERENCES {DB_NAME}.STYLES (ID)
                ON DELETE RESTRICT,
            CONSTRAINT FK_SIZE
                FOREIGN KEY (SIZE_ID)
                REFERENCES {DB_NAME}.SIZES (ID)
                ON DELETE RESTRICT
                """, "PRODUCT_ID ASC", ["STOCK"])},
    "TSCSTMRS": {"CUSTOMERS": (f"""
                ID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                NAME VARCHAR(50) NOT NULL,
                ADDRESS VARCHAR(100) NOT NULL
                """, "ID ASC", ["NAME ASC"])},
    "TSORDERS": {"ORDERS": (f"""
                    ID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    TOTAL_PRICE DECIMAL(12,2) WITH DEFAULT 0.00,
                    ORDER_DATE DATE NOT NULL,
                    CUSTOMER_ID INTEGER NOT NULL,
                    CONSTRAINT FK_CUSTOMER
                        FOREIGN KEY (CUSTOMER_ID)
                        REFERENCES {DB_NAME}.CUSTOMERS (ID)
                        ON DELETE RESTRICT
                    """, "ID ASC", ["TOTAL_PRICE ASC", "ORDER_DATE ASC", "CUSTOMER_ID ASC"])},
    "TSOITEMS": {"ORDER_ITEMS": (f"""
                ORDER_ID INTEGER NOT NULL,
                PRODUCT_ID INTEGER NOT NULL,
                DESIGN_ID INTEGER NOT NULL,
                PRICE DECIMAL(10,2) WITH DEFAULT NULL,
                QUANTITY INTEGER NOT NULL DEFAULT 1,
                GOLD_TRIM SMALLINT NOT NULL WITH DEFAULT 0,
                CONSTRAINT FK_OI_ORDER
                    FOREIGN KEY (ORDER_ID)
                    REFERENCES {DB_NAME}.ORDERS (ID)
                    ON DELETE RESTRICT,
                CONSTRAINT FK_OI_PRODUCT
                    FOREIGN KEY (PRODUCT_ID)
                    REFERENCES {DB_NAME}.INVENTORY (PRODUCT_ID)
                    ON DELETE RESTRICT,
                CONSTRAINT FK_OI_DESIGN
                    FOREIGN KEY (DESIGN_ID)
                    REFERENCES {DB_NAME}.DESIGNS (ID)
                    ON DELETE RESTRICT,
                CONSTRAINT PK_ORDER_ITEMS
                    PRIMARY KEY (ORDER_ID, PRODUCT_ID, DESIGN_ID, GOLD_TRIM)
                """, "ORDER_ID ASC, PRODUCT_ID ASC, DESIGN_ID ASC, GOLD_TRIM", ["PRICE ASC", "QUANTITY ASC"])},
}

connection = ibm_db_interface.get_pooled_connection(db._conn_str)
cursor = connection.cursor()
cursor.execute(f""" 
    SELECT NAME 
    FROM SYSIBM.SYSTABLESPACE
    WHERE DBNAME = '{DB_NAME}' 
    ORDER BY NAME""")
tablespaces_to_drop = [row[0] for row in cursor.fetchall()]

for tablespace in tablespaces_to_drop:
   cursor.execute(f"DROP TABLESPACE {DB_NAME}.{tablespace}")
   print(f"Dropped tablespace: {DB_NAME}.{tablespace}")
connection.commit()
for tablespace, table in TABLESPACES_AND_TABLES.items():
    print(f"Creating TS {tablespace}")
    cursor.execute(f"""CREATE TABLESPACE {tablespace}
    IN {DB_NAME}
    SEGSIZE 4
    BUFFERPOOL BP0;
               """)
    
    for table_name, (table_ddl, unique_key, indexed_columns) in table.items():
        print(f"Creating table {table_name}")
        ddl_string = f"""CREATE TABLE {DB_NAME}.{table_name}
                ({table_ddl}) in {DB_NAME}.{tablespace};
            """
        try:
            cursor.execute(ddl_string)
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")
            print(f"DDL: {ddl_string}")
            exit()
        cursor.execute(f"""
            CREATE UNIQUE INDEX {DB_NAME}.IX_{table_name}_PK
            ON {DB_NAME}.{table_name} ({unique_key})
        """)
        print(f"Creating index for {table_name}")
        cursor.execute(f""" 
            CREATE INDEX {DB_NAME}.IX_{table_name}
            ON {DB_NAME}.{table_name} ({", ".join(indexed_columns)})
        """)

connection.commit()
connection.close()
print("All operations completed successfully.")
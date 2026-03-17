import os
from logger import log
from logger.logger_object import Level
from pathlib import Path
from config.settings import Settings
from order_validation.order_validator import Order
import json

project_root = Path(__file__).parent.parent.parent.parent
venv_path = project_root / ".venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

os.add_dll_directory(str(clidriver_bin))
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db
import ibm_db_dbi

config_path = Settings.db_config_file()
with open(config_path, "r") as file:
    backend_settings = json.load(file)

# This file defines a series of helper functions used by the DAO that aren't directly
# related to looking up stuff in the database, such as for opening a new connection or
# processing data.



def get_pooled_connection(conn_str) -> ibm_db_dbi.Connection:
    """Gets a connection with ibm_db_dbi"""
    new_connection = ibm_db.pconnect(conn_str,"","")
    assert(isinstance(new_connection, ibm_db.IBM_DBConnection))
    return ibm_db_dbi.Connection(new_connection)
    
def get_order_price(order_price_data: dict[int, dict[str, int | float]], order_items: list[dict]) -> tuple[float, list[dict]]:
    
    return (0.0, [{}])

def get_item_price(item_data: dict) -> float:
    running_total = item_data["Style_Price"] * item_data["Size_Factor"]
    running_total += item_data["Material_Price"] + item_data["Design_Price"]
    if "Gold_Trim" in item_data and item_data["Gold_Trim"]:
        running_total += backend_settings["Gold_Trim_Price"]

    return running_total


    
def convert_inventory_data(row: tuple) -> dict:
    price_info = {
        "Size_Factor": float(row[6]),
        "Style_Price": float(row[7]),
        "Material_Price": float(row[8]),
        "Design_Price": 0.0,
        "Gold_Trim": 0
    }
    item_price = get_item_price(price_info)
    return {
        "Product_Id": row[0],
        "Size": row[1],
        "Style": row[2],
        "Material": row[3],
        "Color": row[4],
        "Stock": row[5],
        "Price": item_price
    }

def convert_inventory_price_data(row: tuple) -> dict[str, int | float]:
    # INVENTORY.PRODUCT_ID,
    # INVENTORY.STOCK,
    # SIZES.PRICE_FACTOR AS SIZE_FACTOR,
    # STYLES.PRICE AS STYLE_PRICE,
    # MATERIAL.PRICE AS MATERIAL_PRICE,
    price_data = {}
    
    price_data["Stock"] = row[1]
    price_data["Size_Factor"] = row[1]
    price_data["Style_Price"] = row[2],
    price_data["Material_Price"] = row[3]
    
    return price_data

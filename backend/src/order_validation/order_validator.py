from logger import log
from logger.logger_object import Level

class Order:
    def __init__(self, order_data: dict[str, str | list[dict]]) -> None:
        log.log(Level.DEBUG, "Initializing order object.")

        for key in order_data:
            if key not in ["Customer", "Items"]:
                log.log(Level.ERROR, "Aborting order. The following data is an invalid field: " + str(key))
                raise Exception
            
        log.log(Level.DEBUG, "No invalid fields found.")

        field = ""
        # print(type(order_data["Items"]))
        # print(type(order_data["Items"][0]))
        try:
            field = "Customer"
            assert type(order_data["Customer"]) == dict
            field = "Items"
            assert type(order_data["Items"]) == list            
        except KeyError as e:
            log.log(Level.ERROR, "Aborting order. The following data was not found in request: " + str(e.args))
            raise Exception
        except AssertionError as e:
            log.log(Level.ERROR, "Aborting order. The following data is formatted improperly: " + field)
            raise Exception
        except Exception as e:
            log.log(Level.ERROR, "Aborting order. The following error occurred: " + str(e.args))
            raise Exception
        
        log.log(Level.DEBUG, "All object types are correct.")
        
        self._customer: dict = order_data["Customer"]
        self._items: list[dict] = order_data["Items"]

        log.log(Level.DEBUG, "Order initialized successfully.")

    def validate(self) -> None:
        self.validate_cust()
        self.validate_items()

    def validate_items(self) -> None:
        log.log(Level.DEBUG, "Validating items field for order object.")

        item = {}
        try:
            for item in self._items:
                assert type(item) == dict
        except AssertionError:
            log.log(Level.ERROR, f"Aborting order. The item in index {self._items.index(item)} is formatted incorrectly.")
            raise Exception

        field = ""
        try:
            for item in self._items:
                for field in ["Quantity", "Product_Id", "Design_Id"]:
                    assert type(item[field]) == int
        except AssertionError:
            log.log(Level.ERROR, f"Aborting order. The following data is of the wrong type: index {self._items.index(item)}, field {field}")
            raise Exception
        
        log.log(Level.DEBUG, "Order items validated successfully.")

    def validate_cust(self) -> None:
        log.log(Level.DEBUG, "Validating customer field for order object.")

        key = ""
        try:
            for key in self._customer.keys():
                assert type(key) == str
            for key in self._customer:
                assert type(key) == str
        except AssertionError:
            log.log(Level.ERROR, f"Aborting order. The customer field {key} is not a string.")
            raise Exception

        log.log(Level.DEBUG, "Customer data validated successfully.")
    
    def get_customer(self) -> dict:
        return self._customer
    
    def get_items(self) -> list[dict[str, int]]:
        return self._items
        
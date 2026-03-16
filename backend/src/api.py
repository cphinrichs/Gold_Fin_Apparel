from flask import Flask, request, abort, jsonify
from logger import log
from logger.logger_object import Level
from database import db
from order_validation.order_validator import Order
# from src.validation import *

import json
# import requests

log.log(Level.INFO, "REST API started.")\
# db = LicenseDAO()

app = Flask(__name__)

@app.get("/hello_world")
def hello():
    log.log(Level.INFO, "Hello!")
    print("Hello!")
    return f'<p>Hello!</p>'

@app.get("/inventory")
def getInventory():
    log.log(Level.DEBUG, "Request to get inventory received. Processing...")
    query_fields = dict(request.headers)
    # query_fields = {"Size": "M "}
    log.log(Level.DEBUG, "Request processed. Querying database...")
    query_results = db.select_inventory(query_fields)
    
    log.log(Level.DEBUG, "Database queried successfully. Returning results...")
    return query_results


@app.get("/designs")
def getDesigns():
    log.log(Level.DEBUG, "Request to get designs received. Processing...")
    query_fields = dict(request.headers)
    # query_fields = {"Size": "M"}
    log.log(Level.DEBUG, "Request processed. Querying database...")
    query_results = db.select_designs(query_fields)
    
    log.log(Level.DEBUG, "Database queried successfully. Returning results...")
    return query_results

@app.post("/order")
def postOrder():
    query_fields = request.json
    print(type(query_fields))
    print(query_fields)
    # TODO: validate the request and return a 400 status code if it's not valid
    try:
        order_data = Order(query_fields)
        order_data.validate()
    except Exception as e:
        log.log(Level.ERROR, "Aborting order. Validation failed for reason: " + str(e.args))
        abort(401)

    # TODO: call the DAO using the request object
    

    # TODO: return a 200 status code if successful

    db.create_order(order_data)
    return "<p>Order posted</p>"

if __name__ == '__main__':
    app.run(debug=True)
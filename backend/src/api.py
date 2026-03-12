from flask import Flask, request, abort, jsonify
from logger import log
from logger.logger_object import Level
from database import db
# from src.request.user_request import *
# from src.validation import *

import json
# import requests

log.log(Level.INFO, "REST API started.")\
# db = LicenseDAO()

app = Flask(__name__)

@app.get("/hello_world/")
def hello():
    return f'<p>Hello!</p>'

@app.get("/inventory")
def getInventory():
    log.log(Level.DEBUG, "Request to get inventory received. Processing...")
    query_fields = dict(request.headers)
    log.log(Level.DEBUG, "Request processed. Querying database...")
    query_results = db.select_inventory(query_fields)
    
    log.log(Level.DEBUG, "Database queried successfully. Returning results...")
    return query_results


@app.get("/designs")
def getDesigns():
    abort(418)

@app.post("/order")
def postOrder():
    abort(418)
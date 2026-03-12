from flask import Flask, request, abort, jsonify
from logger import log
from database import db
# from src.request.user_request import *
# from src.validation import *

import json
# import requests

log.log("INFO", "REST API started.")\
# db = LicenseDAO()

app = Flask(__name__)

@app.get("/hello_world/")
def hello():
    return f'<p>Hello!</p>'

@app.get("/inventory")
def getInventory():
    query_fields = request.json
    query_results = db.select_inventory(query_fields)
    return query_results


@app.get("/designs")
def getDesigns():
    abort(418)

@app.post("/order")
def postOrder():
    abort(418)
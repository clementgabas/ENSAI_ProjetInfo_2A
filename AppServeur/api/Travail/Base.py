import os
import traceback
import csv
import random
import json
import hashlib

from api.codeList import _codes

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flask_restplus import Api, Resource
from flask_restplus import abort
from flask_caching import Cache
from loguru import logger
from requests import codes as http_codes
from api.commons import configuration


import sqlite3
import requests
from datetime import datetime



def make_reponse(p_object=None, status_code=http_codes.OK):
    if p_object is None and status_code == http_codes.NOT_FOUND:
        p_object = {
            "status": {
                "status_content": [
                    {"code": "404 - Not Found", "message": "Resource not found"}
                ]
            }
        }

    json_response = jsonify(p_object)
    json_response.status_code = status_code
    json_response.content_type = "application/json;charset=utf-8"
    json_response.headers["Cache-Control"] = "max-age=3600"
    return json_response




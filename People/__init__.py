#!/usr/bin/env python3
import traceback
import sys
import logging
import json
import pymongo as mongo
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return get(req)

def get(req: func.HttpRequest) -> func.HttpResponse:
    age_param = 40 if req.params.get('age') is None else int(req.params.get('age'))

    try:
        connection_string = f"mongodb+srv://{os.environ['user']}:{os.environ['passwd']}@{os.environ['uri']}"    
        people = get_people_from_mongo(connection_string, age = {'$gte': age_param }, name = {'$eq': 'Jesse Jordan'})
        result = parse_mongodb_results(people)
        success = func.HttpResponse(result, mimetype='application/json')    
        return success
    except Exception as e: 
        logging.error(type(e))
        return func.HttpResponse(str(e), status_code=(404 if isinstance(e, ValueError) else 400))

def get_people_from_mongo(connection_string: str, **kwargs):
    try:
        client = connect_to_mongodb(connection_string)
        coll = get_person_collection(client)
        pipeline = [
            {'$match': kwargs},
            {'$project': {'_id': 0, 'name': 1, 'age': 1}} 
        ]

        return coll.aggregate(pipeline)
    except:
        logging.error(traceback.format_exc())
        raise ConnectionError('Could not get data from Mongodb')

def connect_to_mongodb(connection_string: str) -> mongo.MongoClient:
    logging.debug('connecting to mongodb: {}'.format(connection_string))
    return mongo.MongoClient(connection_string)

def get_person_collection(client: mongo.MongoClient) -> mongo.collection:
    db = client.m121
    return db['people']

def parse_mongodb_results(people: mongo.CursorType) -> str:
    try: 
        result = tuple(people)
    except: 
        logging.error(traceback.format_exc())
        raise ValueError('No results found matching the criteria')
    else:
        if len(result) == 0: raise ValueError('No results found matching the criteria')

    return json.dumps(result)
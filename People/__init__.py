#!/usr/bin/env python3

import logging
import pymongo as mongo
import json
import os
import azure.functions as func

def get_people_from_mongo_by_age(connection_string: str, age: int):
    client = connect_to_mongodb(connection_string)
    coll = get_person_collection(client)
    return coll.find({'age': {'$gte': age }}, {'_id': 0, 'name': 1, 'age': 1})

def connect_to_mongodb(connection_string: str) -> mongo.MongoClient:
    logging.debug('connecting to mongodb: {}'.format(connection_string))
    return mongo.MongoClient(connection_string)


def get_person_collection(client: mongo.MongoClient) -> mongo.collection:
    db = client.m121
    return db['people']

def parse_mongodb_results(people: mongo.cursor):
    result = []
    for doc in people:
        result.append(doc)
    return result

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_string = f"mongodb+srv://{os.environ['user']}:{os.environ['passwd']}@{os.environ['uri']}"
    people = get_people_from_mongo_by_age(connection_string, 20)
    result = parse_mongodb_results(people)
    return func.HttpResponse(json.dumps(result), mimetype='application/json')
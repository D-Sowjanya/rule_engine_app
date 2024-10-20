# database.py
from pymongo import MongoClient
from bson import ObjectId

class MongoDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.rules_collection = self.db['rules']

    def insert_rule(self, rule_string, ast):
        rule_doc = {
            "rule_string": rule_string,
            "ast": ast
        }
        result = self.rules_collection.insert_one(rule_doc)
        return str(result.inserted_id)

    def get_rule(self, rule_id):
        return self.rules_collection.find_one({"_id": ObjectId(rule_id)})

    def update_rule(self, rule_id, rule_string, ast):
        self.rules_collection.update_one(
            {"_id": ObjectId(rule_id)},
            {"$set": {"rule_string": rule_string, "ast": ast}}
        )

    def delete_rule(self, rule_id):
        self.rules_collection.delete_one({"_id": ObjectId(rule_id)})

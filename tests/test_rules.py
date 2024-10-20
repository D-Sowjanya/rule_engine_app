# tests/test_rules.py (updated)
import unittest
from rules import create_rule, evaluate_rule
from database import MongoDB

class TestRuleEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mongodb = MongoDB(uri="mongodb://localhost:27017/", db_name="rule_engine_db")

    def test_create_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        rule_id = self.mongodb.insert_rule(rule_string, ast.__dict__)
        self.assertIsNotNone(rule_id)

    def test_evaluate_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        rule_id = self.mongodb.insert_rule(rule_string, ast.__dict__)
        user_data = {"age": 35, "department": "Sales"}
        result = evaluate_rule(ast, user_data)
        self.assertTrue(result)

    def test_update_rule(self):
        rule_string = "age < 40 AND department = 'Sales'"
        ast = create_rule(rule_string)
        rule_id = self.mongodb.insert_rule(rule_string, ast.__dict__)
        updated_string = "age < 45 AND department = 'Marketing'"
        updated_ast = create_rule(updated_string)
        self.mongodb.update_rule(rule_id, updated_string, updated_ast.__dict__)

        # Verify update
        updated_rule = self.mongodb.get_rule(rule_id)
        self.assertEqual(updated_rule['rule_string'], updated_string)

    def test_delete_rule(self):
        rule_string = "age > 25 AND department = 'Sales'"
        ast = create_rule(rule_string)
        rule_id = self.mongodb.insert_rule(rule_string, ast.__dict__)
        self.mongodb.delete_rule(rule_id)

        # Verify deletion
        deleted_rule = self.mongodb.get_rule(rule_id)
        self.assertIsNone(deleted_rule)

if __name__ == '__main__':
    unittest.main()

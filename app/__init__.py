# app/__init__.py

__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "A simple rule engine that uses an Abstract Syntax Tree (AST) for evaluating user eligibility based on defined rules."

# Import key components for easier access
from .models import Node
from .rules import create_rule, evaluate_rule, combine_rules
from pymongo import MongoDB

# Optionally, you could define a simple initializer or helper function
def initialize_db(uri="mongodb://localhost:27017/", db_name="rule_engine_db"):
    """Initialize the database connection."""
    return MongoDB(uri, db_name)

# You can also add other initial setup code here if needed

# rules.py
import re
from models import Node

# A basic function to parse conditions like "age > 30"
def parse_condition(condition):
    match = re.match(r"(\w+)\s*(>=|<=|>|<|=)\s*(\w+)", condition.strip())
    if match:
        attr, operator, value = match.groups()
        if value.isdigit():
            value = int(value)  # convert value to an integer if applicable
        return Node("operand", (attr, operator, value))
    return None

def create_rule(rule_string):
    # Parse the rule string and create the corresponding AST.
    rule_string = rule_string.strip()
    if "AND" in rule_string:
        left_part, right_part = rule_string.split("AND", 1)
        left_node = create_rule(left_part)
        right_node = create_rule(right_part)
        return Node("operator", "AND", left=left_node, right=right_node)
    elif "OR" in rule_string:
        left_part, right_part = rule_string.split("OR", 1)
        left_node = create_rule(left_part)
        right_node = create_rule(right_part)
        return Node("operator", "OR", left=left_node, right=right_node)
    else:
        # It's a condition
        return parse_condition(rule_string)

# Example
rule_string = "age > 30 AND department = 'Sales'"
ast_root = create_rule(rule_string)
print(ast_root)




def evaluate_rule(ast_node, data):
    """
    Evaluate the rule AST against the provided user data.
    ast_node: Root node of the AST.
    data: Dictionary containing user attributes like {"age": 35, "department": "Sales"}
    """
    if ast_node.node_type == "operand":
        attr, operator, value = ast_node.value
        user_value = data.get(attr)

        if operator == '>':
            return user_value > value
        elif operator == '<':
            return user_value < value
        elif operator == '=':
            return user_value == value
        elif operator == '>=':
            return user_value >= value
        elif operator == '<=':
            return user_value <= value
        else:
            return False

    elif ast_node.node_type == "operator":
        if ast_node.value == "AND":
            return evaluate_rule(ast_node.left, data) and evaluate_rule(ast_node.right, data)
        elif ast_node.value == "OR":
            return evaluate_rule(ast_node.left, data) or evaluate_rule(ast_node.right, data)

    return False

# Example evaluation
user_data = {"age": 35, "department": "Sales"}
result = evaluate_rule(ast_root, user_data)
print(result)  # True or False




def combine_rules(rule_strings, combine_type="AND"):
    """
    Combine multiple rule strings into a single AST.
    combine_type: 'AND' or 'OR' to combine the rules.
    """
    combined_ast = None

    for rule_string in rule_strings:
        rule_ast = create_rule(rule_string)
        if not combined_ast:
            combined_ast = rule_ast
        else:
            combined_ast = Node("operator", combine_type, left=combined_ast, right=rule_ast)

    return combined_ast

# Example
rule1 = "age > 30 AND department = 'Sales'"
rule2 = "salary > 50000 OR experience > 5"
combined_ast = combine_rules([rule1, rule2], combine_type="AND")
print(combined_ast)





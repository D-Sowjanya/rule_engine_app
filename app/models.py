# models.py

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        """
        Represents an AST Node.
        node_type: "operator" for AND/OR, "operand" for conditions
        value: For operands, store a tuple of (attribute, operator, value)
               For operators, store the operation like "AND", "OR"
        left: Reference to the left child node
        right: Reference to the right child node
        """
        self.node_type = node_type  # 'operator' or 'operand'
        self.value = value          # Condition or operator
        self.left = left            # Left child (for operator nodes)
        self.right = right          # Right child (for operator nodes)

    def __repr__(self):
        return f"Node({self.node_type}, {self.value})"

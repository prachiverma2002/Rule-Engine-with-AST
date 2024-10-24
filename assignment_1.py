class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # 'operator' for AND/OR, 'operand' for conditions
        self.value = value     # Only relevant for 'operand' nodes (e.g., 'age > 30')
        self.left = left       # Left child (for operators)
        self.right = right     # Right child (for operators)

    def __repr__(self):
        if self.type == "operand":
            return f"Operand({self.value})"
        elif self.type == "operator":
            return f"Operator({self.value}) with left: {self.left} and right: {self.right}"


def create_rule(rule_string):
    # For simplicity, we'll split the rule by AND/OR and create a basic AST
    # The function assumes conditions are in the form (age > 30 AND salary > 50000)
    
    tokens = rule_string.split()  # Simple tokenization (would need a real parser for complex rules)
    
    if "AND" in tokens:
        and_index = tokens.index("AND")
        left_part = " ".join(tokens[:and_index])
        right_part = " ".join(tokens[and_index+1:])
        
        left_node = Node(node_type="operand", value=left_part)
        right_node = Node(node_type="operand", value=right_part)
        
        return Node(node_type="operator", value="AND", left=left_node, right=right_node)
    
    elif "OR" in tokens:
        or_index = tokens.index("OR")
        left_part = " ".join(tokens[:or_index])
        right_part = " ".join(tokens[or_index+1:])
        
        left_node = Node(node_type="operand", value=left_part)
        right_node = Node(node_type="operand", value=right_part)
        
        return Node(node_type="operator", value="OR", left=left_node, right=right_node)
    
    else:
        return Node(node_type="operand", value=rule_string)


def combine_rules(rules, operator="AND"):
    combined_ast = None
    
    for rule_string in rules:
        rule_ast = create_rule(rule_string)
        
        if combined_ast is None:
            combined_ast = rule_ast
        else:
            combined_ast = Node(node_type="operator", value=operator, left=combined_ast, right=rule_ast)
    
    return combined_ast

def evaluate_rule(node, data):
    if node.type == "operand":
        # Extract condition, e.g., 'age > 30' or 'department == "Sales"'
        condition = node.value.strip()
        key, operator, value = condition.split()[:3]
        
        if key not in data:
            return False
        
        # Handle different operators
        if operator == '>':
            return data[key] > float(value)
        elif operator == '<':
            return data[key] < float(value)
        elif operator == '==':
            return str(data[key]) == value.strip("'")
    
    elif node.type == "operator":
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)
        
        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result
    
    return False

rule1 = "age > 30 AND department == 'Sales'"
rule2 = "salary > 50000 OR experience > 5"

ast_rule1 = create_rule(rule1)
ast_rule2 = create_rule(rule2)

print("AST for Rule 1:", ast_rule1)
print("AST for Rule 2:", ast_rule2)

data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
print("Evaluation of Rule 1:", evaluate_rule(ast_rule1, data))  # True
print("Evaluation of Rule 2:", evaluate_rule(ast_rule2, data))  # True

combined_ast = combine_rules([rule1, rule2], operator="AND")
print("Combined AST:", combined_ast)
print("Evaluation of Combined Rule:", evaluate_rule(combined_ast, data))  # True

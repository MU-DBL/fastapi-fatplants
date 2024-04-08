import re

def is_sql_injection(input_value):
    # Regular expression pattern to detect common SQL injection characters or patterns
    # edit if any of the symbol is required in input
    sql_injection_pattern = r'[-;\'"()/\|{}=+*[\]<>?`~&^%$#@!,\s]'
    
    if re.search(sql_injection_pattern, input_value):
        return True  # SQL injection detected
    else:
        return False  # No SQL injection detected
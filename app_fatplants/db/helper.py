import re

def is_sql_injection(input_value, search=False):
    # Regular expression pattern to detect common SQL injection characters or patterns
    # edit if any of the symbol is required in input
    if search:
        sql_injection_pattern = r'[\'"\|{}=+*[\]<>?`~^%$#@!]' #Allow some characters for searching
    else:
        sql_injection_pattern = r'[;\'"()\|{}=+*[\]<>?`~&^%$#@!]'
    if re.search(sql_injection_pattern, input_value):
        return True  # SQL injection detected
    else:
        return False  # No SQL injection detected

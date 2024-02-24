import cgi 
import main
import json

print("Content-type: application/json; charset=utf-8\n")

# print(main.get_categories())



print(f'{{"categories": {json.dumps(main.get_categories())}}}')



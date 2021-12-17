import ast
from astpp import *
import call_extractor

code_f = open('sample/py_demo.py', 'r')
content = code_f.read()
tree = ast.parse(content)

extractor = call_extractor.CallExtractor()
ans = []
extractor.extract_from_file(code_f.name, ans)

print(ans)
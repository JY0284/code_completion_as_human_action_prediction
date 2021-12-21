import ast
from astpp import *
import call_extractor

code_f = open('sample/astpp.py', 'r', encoding='utf-8')
content = code_f.read()
tree = ast.parse(content)

extractor = call_extractor.CallExtractor()
ans = []
extractor.extract_from_file(code_f.name, ans)

print(ans)


# 1.ctx
pass

# 2.actor

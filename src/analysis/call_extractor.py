import ast
from _ast import AST, Assign, Call
from typing import Any
from spiral import ronin
import copy

MAX_ASSIGN_LEFT_VALUE = 3

class CallExtractor(ast.NodeVisitor):

    def __init__(self):
        self.ans = []
        self.ctx = []

    def visit_and_save(self, node: AST, ans) -> Any:
        self.ans = ans
        return super().visit(node)

    def extract_from_file(self, file_name, ans, max_lines=-1):
        code_file = None
        try:
            code_file = open(file_name, 'r', encoding='utf-8')
            content = code_file.readlines()
            code_file.close()
            if max_lines > 0 and len(content) > max_lines:
                return False
        except BaseException as e:
            # print("error while opening:" + str(e))
            return False

        ast_obj = None
        try:
            ast_obj = ast.parse(''.join(content))
        except BaseException as e:
            # print('error while parsing:' + str(e))
            return False
        if ast_obj is not None:
            self.visit_and_save(ast_obj, ans)
        
        return True

    def visit_Assign(self, node: Assign) -> Any:
        self.generic_visit(node)
        res = [copy.copy(self.ctx), 'Assign']
        for target in node.targets[:MAX_ASSIGN_LEFT_VALUE]:
            res.append(target.id)
        self.ans.append(res)

    def get_call_stk(self, node):
        prt_stk = []
        cur = node.func
        while isinstance(cur, ast.Attribute) \
                and not isinstance(cur.value, ast.Call):
            prt_stk.append(cur.attr)
            cur = cur.value
        if hasattr(cur, 'id'):
            prt_stk.append(cur.id)
        elif hasattr(cur, 'attr'):
            prt_stk.append(cur.attr)
        return prt_stk

    def get_actor(self, node:Call):
        # case1: db.execute().get()
        if isinstance(node.func.value, ast.Call):
            prt_stk = self.get_call_stk(node.func.value)
            return '.'.join(prt_stk[::-1])
        # case2: ''.join()
        elif isinstance(node.func.value, ast.Constant):
            return '$Const$'
        else:
            return ''

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Attribute):
            actor = self.get_actor(node)
            res = None
            # case2: ''.join()
            if isinstance(node.func.value, ast.Constant):
                prt_stk = node.func.attr
                res = [copy.copy(self.ctx), 'Call', actor, prt_stk]
            else:
                prt_stk = self.get_call_stk(node)
                if actor != '':
                    res = '.'.join(prt_stk[::-1])
                    res = [copy.copy(self.ctx), 'Call', actor, res]
                else:
                    res = '.'.join(prt_stk[:-1][::-1])
                    res = [copy.copy(self.ctx), 'Call', prt_stk[-1], res]
            self.ans.append(res)
        else:
            if hasattr(node.func, 'id'):
                self.ans.append([copy.copy(self.ctx), 'Call', '$', node.func.id])
            elif hasattr(node.func, 'attr'):
                self.ans.append([copy.copy(self.ctx), 'Call', '$', node.func.attr])


    def visit_Return(self, node):
        self.generic_visit(node)
        self.ans.append([copy.copy(self.ctx), 'Return'])

    def visit_FunctionDef(self, node):
        self.ans.append('*' * (len(self.ctx) + 1) + node.name)
        self.ctx.append(node.name)
        self.generic_visit(node)
        self.ans.append('#' * (len(self.ctx) + 1) + node.name)
        self.ctx.pop(-1)



def trim_by_method(seqs):
    res = seqs[1:]
    res = [[seq[0][1:]] + seq[1:] for seq in res]
    tmp = []
    for seq in res:
        tmp.append([call if call.find('.') == -1 else call[len(call) - call[::-1].find('.'):] for call in seq])
    
    return tmp

def extract_seq_by_method(origin_lst, threshold=2, trim=False):
    outside = []
    func_stk = []
    res_stk = []

    for e in origin_lst:
        if e.startswith('*') and e != '*#':
            func_stk.append([])
            func_stk[-1].append(e)
            continue

        if len(func_stk) > 0:
            if e.startswith('#'):
                if e[1:] == func_stk[-1][0][1:]:
                    res_stk.append(func_stk.pop())
                else:
#                     print(e)
                    raise BaseException('Error')
            else:
                func_stk[-1].append(e)
        else:
            outside.append(e)

    res_stk = [lst for lst in res_stk if len(lst) >= threshold]
    res_stk.insert(0, outside)

    return res_stk if not trim else trim_by_method(res_stk)


def split_and_make_sense(seq):
    tmp = [seq[0]]
    for call in seq[1:]:
        if call == '*#':
            tmp.append(['return'])
            continue
        
        splits = ronin.split(call)
        if len(splits) > 0:
            tmp.append([word.lower() if len(word) > 1 and word[0].isupper() and word[1].islower() else word for word in splits])
    
    return tmp


def split_seqs_by_method_to_one_long(seqs):
    res = []
    for lst in seqs:
        res += [ronin.split(lst)]
    res = [e for l in res for e in l if e != 'self']

    return res


def demo():
    # code_file = open('download_file.py', 'r')
    # code_file = open('image.py', 'r')
    # content = code_file.readlines()
    # code_file.close()
    # ast_obj = ast.parse(''.join(content))
    #
    res = []
    sv = CallExtractor()
    # sv.visit_and_save(ast_obj, res)
    sv.extract_from_file('../publish_docs.py', res)
    print(sv.ans)

# demo()

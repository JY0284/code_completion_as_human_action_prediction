import json
import pickle
from model import *


def get_py_name(fpath: str):
    # data / repo\\0101\\pipetools\\publish_docs.py
    return fpath[-fpath[::-1].index('\\'):]


def raw_quads_to_objects(raw_quads: dict):
    objs = []
    for f_name, content in raw_quads.items():
        ori_name = f_name
        f_name = get_py_name(f_name)[:-3]
        res_lst = extract_by_method(content)
        e = None
        for m_res in res_lst:
            try:
                for e in m_res:
                    e = e
                    obj = Quad()
                    objs.append(obj)
                    obj.ctx = [f_name] + e[0]
                    obj.type = e[1]
                    if obj.type in RETURN_TOKEN:
                        continue
                    if isinstance(e[2], list):
                    obj.actor = e[2]
                    else:
                        obj.actor = [e[2]]
                    if obj.type in ASSIGN_TOKEN:
                        continue
                    obj.call = e[3]
                    obj.paras = e[4]
            except BaseException as exp:
                print(e)
                print(exp)
                print(ori_name)
    return objs


# discard outside
def extract_by_method(content, threshold=2):
    outside = []
    func_stk = []
    res_stk = []
    for e in content:
        if isinstance(e, str) and e.startswith('*'):
            func_stk.append([])
            func_stk[-1].append(e)
            continue

        if len(func_stk) > 0:
            if isinstance(e, str) and e.startswith('#'):
                if e[e.count('#'):] == func_stk[-1][0][e.count('#'):]:
                    func_stk[-1].pop(0)
                    res_stk.append(func_stk.pop())
                else:
                    print(e)
                    raise BaseException('Error')
            else:
                func_stk[-1].append(e)
        else:
            outside.append(e)

    res_stk = [lst for lst in res_stk if len(lst) >= threshold]

    return res_stk

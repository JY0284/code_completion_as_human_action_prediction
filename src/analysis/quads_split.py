"""
This script will take care of quads objects 
and use ronin to split them with given limitations.
"""

import pickle
import argparse

from tqdm import tqdm
from spiral import ronin

import data_utils
from model import *
from joblib import Parallel, delayed


def add_method_key(qd):
    qd['key'] = qd['ctx'][-1]


def quad_obj_split(quad):
    # split to tokens
    # print(quad)
    add_method_key(quad)
    ctx = [token for sign in quad['ctx'] for token in ronin.split(sign)]
    quad['ctx'] = ctx[:STORAGE_MAX_CTX_LEN]
    if isinstance(quad['call'], list):
        # call is empty
        quad['call'] = []
    else:
        calls = ronin.split(quad['call'])
        quad['call'] = calls[:STORAGE_MAX_CALL_LEN]

    if not isinstance(quad['actor'], list):
        print(quad.__dict__)
        raise BaseException()

    actor_lst = quad['actor']
    if len(actor_lst) == 1:
        if actor_lst[0] in [CONST_TOKEN, SELF_TOKEN]:
            quad['actor'] = quad['actor']
        else:
            actors = ronin.split(actor_lst[0])
            quad['actor'] = actors[:STORAGE_MAX_ACTOR_LEN]
    else:
        quad['actor'] = [
            token for actor in actor_lst for token in ronin.split(actor)]

    if quad['type'] == CALL_TOKEN:
        paras = []
        for para in quad['paras']:
            if para in ['$Const$']:
                paras.append(para)
            else:
                paras += ronin.split(para)
        quad['paras'] = paras[:STORAGE_MAX_PARAS_LEN]
    else:
        quad['paras'] = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Split quads objects with ronin.')
    parser.add_argument('in_file', metavar='IN_FILE', type=str,
                        help='quads pickle file to split')
    parser.add_argument('out_file', metavar='OUT_FILE', type=str,
                        help='output file path')

    args = parser.parse_args()

    f = open(args.in_file, 'rb')
    quads = pickle.load(f)
    f.close()
    print(f"Processing files count: {len(quads.keys())}")
    quad_objs = data_utils.raw_quads_to_objects(quads)
    quads_dic = [e.__dict__ for e in quad_objs]

    Parallel(n_jobs=16, require='sharedmem')(delayed(quad_obj_split)(quad)
                                             for quad in tqdm(quads_dic))

    f = open(args.out_file, 'wb')
    pickle.dump(quads_dic, f)
    f.close()
    print(f"Data file has been written to {args.out_file}")

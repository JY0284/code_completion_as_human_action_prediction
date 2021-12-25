import ast
import json
import pickle
import tqdm
import call_extractor
import utils
from joblib import Parallel, delayed


def debug():
    code_f = open('data/repo\\0101\\pipetools\\setup.py', 'r', encoding='utf-8')
content = code_f.read()
tree = ast.parse(content)

extractor = call_extractor.CallExtractor()
ans = []
extractor.extract_from_file(code_f.name, ans)

print(ans)


def generate_quads(count_str: str, output_path):
    files = pickle.load(open('data/repo_files.pkl', 'rb'))
    print(len(files))

    res = {}
    wrong = {}
    extractor = call_extractor.CallExtractor()
    n_files_to_go = utils.convert_str_to_number(count_str)
    n = len(files)
    if n_files_to_go == -1:
        n_files_to_go = n
    n_files_to_go = min(n_files_to_go, n)

    def process(f_name):
        try:
            tmp_file = open(f_name, 'r', encoding='utf-8')
            lines = tmp_file.readlines()
            tmp_file.close()
            if len(lines) <= 500:
                ans = []
                extractor.extract_from_file(f_name, ans)
                res[f_name] = ans
        except BaseException as e:
            wrong[f_name] = e
        finally:
            return None

    Parallel(n_jobs=16, require='sharedmem') \
        (delayed(process)(files[i])
         for i in tqdm.tqdm(range(n_files_to_go)))

    print(f'#Error: {len(wrong)}')

    f = open(output_path + 'quads_' + count_str + '.pkl', 'wb')
    pickle.dump(res, f)
    f.close()

    f = open(output_path + 'quads_' + count_str + '.json', 'w')
    json.dump(res, f, indent=4)
    f.close()


# 2.actor

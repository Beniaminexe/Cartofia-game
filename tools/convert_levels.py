import os, json, pickle

ROOT = os.path.dirname(os.path.dirname(__file__))

for fname in os.listdir(ROOT):
    if fname.startswith('level') and fname.endswith('_data'):
        levelname = fname.split('_')[0]  # level1, level2
        p = os.path.join(ROOT, fname)
        try:
            with open(p, 'rb') as f:
                data = pickle.load(f)
            json_fname = os.path.join(ROOT, f'{levelname}.json')
            with open(json_fname, 'w', encoding='utf-8') as jf:
                json.dump(data, jf)
            print(f'Converted {fname} -> {levelname}.json')
        except Exception as e:
            print('Failed to convert', fname, e)

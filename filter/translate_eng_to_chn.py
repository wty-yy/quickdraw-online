import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
from translate import Translator
from tqdm import tqdm

# 将英文标签转化为中文标签，生成eng_to_chn.json文件
def load_eng_to_chn():
    path = Path.cwd().joinpath("eng_to_chn.json")
    if not path.exists():
        translator = Translator(from_lang="English", to_lang="Chinese")
        eng_to_chn = {}
        PATH_DATASET = Path(r"C:\Coding\demo\quick_draw\numpy_bitmap")  # 数据集路径
        dirs = list(PATH_DATASET.iterdir())
        flag = True
        for f in tqdm(dirs):
            label = f.name[:-4]
            # if label == 'roller coaster': flag = False
            if label == 'square': flag = False

            chn = None
            if label == 'rollerskates': label = 'roller skates'
            if label == 'squiggle': chn = '胡乱写的字，花体'
            # print(f, f.name, label)

            if flag: continue
            if chn is None:
                try:
                    chn = translator.translate(label)
                except:
                    break
            eng_to_chn[label] = chn
        with open(path, "w", encoding='utf-8') as file:
            json.dump(eng_to_chn, file, indent=4, ensure_ascii=False)
    with open(path, "r", encoding='utf-8') as file:
        eng_to_chn = json.load(file)
    return eng_to_chn

eng_to_chn = load_eng_to_chn()
print(eng_to_chn, len(eng_to_chn))

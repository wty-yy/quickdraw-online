import numpy as np
from pathlib import Path
import json

PATH_DATASET = Path.cwd().parent.joinpath("dataset_selected")  # 数据集路径

PATH_ARCHIVES = Path.cwd().parent.joinpath("archives")  # 文档存放路径
if not PATH_ARCHIVES.exists():
    raise BaseException(f"文件夹{PATH_ARCHIVES}不存在")

PATH_MODELS = Path.cwd().parent.joinpath("models")  # 模型存放路径
if not PATH_MODELS.exists():
    raise BaseException(f"文件夹{PATH_MODELS}不存在")

with open(PATH_ARCHIVES.joinpath("eng_to_chn.json"), "r", encoding="utf-8") as file:  # 标签英文转中文字典
    eng_to_chn = json.load(file)

with open(PATH_ARCHIVES.joinpath("target_labels.txt"), "r") as file:  # 读取筛选标签
    target_labels = file.read().split('\n')[:-1]
target_labels = np.array(target_labels)

show_row = 2
show_column = 5
show_total = show_row * show_column
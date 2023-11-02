from pathlib import Path
import json

PATH_DATASET = Path(r"C:\Coding\xjtu_quick_draw\dataset_selected")  # 数据集

PATH_ARCHIVES = Path(__file__).parent.parent.joinpath("archives")  # 文档存放路径
if not PATH_ARCHIVES.exists():
    raise BaseException(f"文件夹{PATH_ARCHIVES}不存在")

with open(PATH_ARCHIVES.joinpath("eng_to_chn.json"), "r", encoding="utf-8") as file:  # 标签英文转中文字典
    eng_to_chn = json.load(file)

with open(PATH_ARCHIVES.joinpath("target_labels.txt"), "r") as file:  # 读取筛选标签
    target_labels = file.read().split('\n')[:-1]

PATH_AUG = Path("./augmentations")  # 存储图像增强的采样图片
PATH_AUG.mkdir(parents=True, exist_ok=True)
import pickle
import numpy as np
from pathlib import Path
from random import choice
from PIL import Image
from constant import target_labels, target_counts, img_show_total
from constant import PATH_DATASET, PATH_LOGS, PATH_CACHE, PATH_SELECTED

PATH_SELECTED_COUNTS = PATH_LOGS.joinpath("selected_counts.pkl")

def load_file(path:Path):  # 用pickle读取path中文件
    assert(path.exists())
    with open(path, 'rb') as file:
        ret = pickle.load(file)
    return ret

def save_file(obj, path:Path):  # 用pickle保存obj数据到path中
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

class ImageBag:  # 用户与网页交互时显示的图片包
    # bag.label为当前图片包的标签
    # bag.paths为当前图片包中每个图片的路径
    def __init__(self):
        undone_labels = []  # 选出还未达到目标筛选数量的label并且在target_labels中
        for label, count in selected_counts.items():
            if label not in target_labels: continue
            if count < target_counts:
                undone_labels.append(label)
        if len(undone_labels) > 0:
            self.label = choice(undone_labels)  # 从中随机选出一个label作为当前的图像包标签
        else: self.label = -1; return
        # 读取图像
        imgs = np.load(PATH_DATASET.joinpath(f"{self.label}.npy"), encoding="latin1", allow_pickle=True)
        # 读取当前标签已使用过的索引
        self.path_label_used_idxs = PATH_LOGS.joinpath(f"{self.label}_used_idxs.pkl")
        used_idxs = load_file(self.path_label_used_idxs)  # set类型
        self.idxs = []  # 顺次选取img_show_total个未使用过的索引，准备显示到网页上
        for i in range(imgs.shape[0]):
            if i not in used_idxs:
                self.idxs.append(i)
                used_idxs.add(i)  # 将当前用过的索引加入used_idxs中，避免其他用户选到相同图片
            if len(self.idxs) == img_show_total: break
        save_file(used_idxs, self.path_label_used_idxs)
        imgs = imgs[self.idxs]  # 选出特定索引的图像

        self.paths = []  # 当前缓存中的图像路径
        for img, idx in zip(imgs, self.idxs):  # 加载到缓存中
            path = PATH_CACHE.joinpath(f"{self.label}/{idx}.png")
            Image.fromarray(img.reshape(28,28)).save(path)
            self.paths.append(path)

    def update(self, html_idxs):  # 根据用户网页上筛选的图片索引html_idxs，保存图片
        selected_counts[self.label] += len(html_idxs)
        save_file(selected_counts, PATH_SELECTED_COUNTS)
        for idx in html_idxs:  # 移动筛选出的图片
            path = self.paths[idx]
            path.replace(PATH_SELECTED.joinpath(f"{self.label}/" + path.name))
        self.__remove()

    def __remove(self):  # 删除图片包中的所有图片
        for path in self.paths:
            if path.exists(): path.unlink()

    def reset(self):  # 当用户未完成当前的图片包图像选择，则将当前锁定的索引重新解锁
        used_idxs = load_file(self.path_label_used_idxs)
        for idx in self.idxs:
            used_idxs.remove(idx)
        save_file(used_idxs, self.path_label_used_idxs)
        self.__remove()

# 下面分别检查./logs目录下
# "selected_counts.pkl"和每个label对应的f"{label}_used_idxs.pkl"是否存在
# 若不存在则进行创建，并读取selected_counts.pkl文件
selected_counts = {}  # 每个标签已筛选出的数目，用字典保存
# {'label1': num1, 'label2': num2, ...}
if not PATH_SELECTED_COUNTS.exists():
    for label in target_labels:
        selected_counts[label] = 0
    save_file(selected_counts, PATH_SELECTED_COUNTS)
else:
    selected_counts = load_file(PATH_SELECTED_COUNTS)

for label in target_labels:  # 每个标签已用过的图片索引，用set保存
    # label1_used_idxs.pkl用set存储label1中已用过的索引
    path = PATH_LOGS.joinpath(f"{label}_used_idxs.pkl")
    if not path.exists():
        save_file(set(), path)  # 初始化为空set

if __name__ == '__main__':
    bag = ImageBag()
    print(bag.label, bag.paths)
    input("继续？")
    bag.reset()

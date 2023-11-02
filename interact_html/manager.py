from PIL import Image, ImageOps
import base64
from io import BytesIO
import numpy as np
from pathlib import Path
from constant import target_labels, eng_to_chn, PATH_DATASET, show_total, show_column
import shutil
PATH_CACHE = Path("./static/cache")
PATH_CACHE.mkdir(parents=True, exist_ok=True)

def clean_cache(path):
    if not path.exists(): return
    if path.is_file():
        path.unlink()
    else:
        for file in path.iterdir():
            if file.is_file():
                file.unlink()
            else: clean_cache(file)
        path.rmdir()

class Manager:
    def __init__(self):
        self.count = 0
        self.users = []
    def add(self):
        self.users.append(User(self.count))
        self.count += 1
        return self.users[-1]
    def get_user(self, id):
        if id >= self.count: return False
        return self.users[id]

def convert_form_to_image(image_data):
    base64_data = image_data.split(',')[1]
    decoded_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(decoded_data))
    # 图片为RGBA格式，由于是黑白图片，只有第三个维度不为0
    # 0为透明，而255为不透明，所以后续也不用翻转值域
    image = np.array(image)[:,:,3]
    return image

class User:
    def __init__(self, id):
        self.id = id
        self.count = 0
        self.dir_path = PATH_CACHE.joinpath(f"{self.id:04}")
        self.dir_path.mkdir(parents=True, exist_ok=True)
        self.get_table()
        self.img = None
        self.img_path = None

    def get_paths(self):
        self.relative_paths = []
        dir_show_path = self.dir_path.joinpath("show")
        clean_cache(dir_show_path)
        dir_show_path.mkdir(parents=True, exist_ok=True)
        for label in self.show_labels:
            path = PATH_DATASET.joinpath(label)
            files = list(path.iterdir())
            file = np.random.choice(files)
            show_path = dir_show_path.joinpath(label+'_'+file.name).absolute()
            # print(file, show_path)
            relative_path = str(show_path)[str(show_path).find("static")-1:]
            # print(relative_path)
            self.relative_paths.append(relative_path)
            shutil.copy(file, show_path)
    
    def get_table(self):  # 更新为用户显示的图像索引及对应的缓存位置
        self.show_labels = np.random.choice(target_labels, show_total)
        self.get_paths()
        self.table, row = [], []
        for idx, (label, path) in enumerate(zip(self.show_labels, self.relative_paths)):
            row.append((label, eng_to_chn[label], path))
            if (idx + 1) % show_column == 0:
                self.table.append(row)
                row = []
    
    def get_relative_path(self):  # 获取相对于static/的路径
        s = str(self.img_path.absolute()).split('/')
        return '/'.join(s[-3:])

    def remove_img(self):
        if self.img_path is not None and self.img_path.exists():
            self.img_path.unlink()

    def save_img(self):
        # Image读取灰度图像不能有第三个维度
        Image.fromarray(self.img).save(self.img_path)

    def update_img(self, image_data):
        # 图片读取与保存，并删除旧图片
        self.remove_img()
        self.count += 1
        self.img = convert_form_to_image(image_data)
        self.img_path = self.dir_path.joinpath(f"img{self.count:04}.png")
        self.save_img()

    def test_table(self):
        table_data = [
            ["1", "衣服1", f"{np.random.rand()}%"],
            ["2", "衣服2", "50%"],
            ["3", "衣服3", "50%"],
            ["4", "衣服4", "40%"],
            ["5", "衣服5", "30%"],
        ]
        return table_data


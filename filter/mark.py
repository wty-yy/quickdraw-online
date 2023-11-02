import pickle
from pathlib import Path
from constant import names, PATH_LOGS
PATH_MARK = PATH_LOGS.joinpath("mark.pkl")

class Mark():  # 记录每个用户标记的总数目
    # mark.mark = {'selected': 已标记总数, 'total': 已显示图片总数,
    #              'name1': (用户1标记数目, 用户1显示图片数目),
    #              'name2': (用户2标记数目, 用户2显示图片数目), ...}
    # mark记录存储到路径"./logs/mark.pkl"中
    def __init__(self):
        self.mark = {'selected': 0, 'total': 0}
        self.load()

    def update(self, name, selected_num, total_num):  # 更新用户name新标记了num个图片
        # print(type(self.mark))
        self.mark['selected'] += selected_num
        self.mark['total'] += total_num
        self.mark[name][0] += selected_num
        self.mark[name][1] += total_num
        self.save()

    def load(self):  # 从mark.pkl文件中读取之前记录的信息，若不存在则重新创建
        if not PATH_MARK.exists():
            for name in names: self.mark[name] = [0, 0]
            self.save()
        with open(PATH_MARK, "rb") as file:
            self.mark = pickle.load(file)

    def save(self):  # 保存当前的mark信息
        with open(PATH_MARK, "wb") as file:
            pickle.dump(self.mark, file)
    
    def __str__(self) -> str:  # 重载print函数的输出显示
        ret = f"已筛选总数: {self.mark['total']}\n"
        for idx, name in enumerate(names):
            ret += f"{name}\t: {self.mark[name]:10}|  "
            if idx % 2 == 1 and idx: ret += '\n'
        return ret

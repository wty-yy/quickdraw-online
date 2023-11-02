from pathlib import Path
import json

PATH_ARCHIVES = Path(__file__).parent.parent.joinpath("archives")  # 文档存放路径
if not PATH_ARCHIVES.exists():
    raise BaseException(f"文件夹{PATH_ARCHIVES}不存在")

with open(PATH_ARCHIVES.joinpath("eng_to_chn.json"), "r", encoding="utf-8") as file:  # 标签英文转中文字典
    eng_to_chn = json.load(file)

with open(PATH_ARCHIVES.joinpath("target_labels.txt"), "r") as file:  # 读取筛选标签
    target_labels = file.read().split('\n')[:-1]

names = ['吴天阳', '张政', '师梓豪', '苏渝钦', '王承杰', '杨涵', '孙一珺', '程思诚']
# target_labels = ['ant', 'apple', 'axe']
target_counts = 500  # 每个类别目标筛选个数
total_targets = len(target_labels) * target_counts


# 若path对应的目录为创建，进行创建
def check_dir(path): path.mkdir(parents=True, exist_ok=True)

PATH_DATASET = Path(r"/home/wty/Coding/datasets/quick_draw")  # 数据集位置
PATH_LOGS = Path.cwd().joinpath("logs")  # 日志位置，当前路径下的logs文件夹
check_dir(PATH_LOGS)
PATH_CACHE = Path.cwd().joinpath("static/cache")  # 图片缓存位置，当前路径下的cache文件夹
check_dir(PATH_CACHE)
PATH_SELECTED = Path.cwd().joinpath("selected")  # 筛选好的图片保存位置，当前路径下的selected文件夹
check_dir(PATH_SELECTED)
for label in target_labels:  # 在缓存和筛选好的图片保存路径中创建类别对应的文件夹
    check_dir(PATH_CACHE.joinpath(label))
    check_dir(PATH_SELECTED.joinpath(label))

# HTML
img_show_row = 10  # 网页中每行显示的图片数
img_show_column = 3  # 网页中每列显示的图片数
img_show_total = img_show_row * img_show_column  # 显示的总图片数

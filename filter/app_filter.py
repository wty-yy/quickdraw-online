import re
import numpy as np
from mark import Mark
from pathlib import Path
from imagebag import ImageBag, selected_counts
from flask import Flask, render_template, request, redirect, url_for
from constant import names, img_show_row, img_show_column, img_show_total, eng_to_chn
from constant import total_targets, target_counts, target_labels

app = Flask(__name__)

def sort_zip(a, keys, reverse=True):
    sort_a_keys = sorted(zip(a, keys), key=lambda x: x[1], reverse=reverse)
    return [i[0] for i in sort_a_keys], [i[1] for i in sort_a_keys]

def get_infos():
    # 处理HTML现实的与类别相关的信息，分别为
    # messages每个类别已经筛选图片数的文本信息
    # num_label每个类别已筛选的个数和对应的英中文标签，进度比例
    # total_target目标筛选图片数
    # complete_count已完成筛选的类别数
    # complete_all_flag已完成全部筛选标签
    infos = {'messages': [], 'num_label': [], 'total_target': total_targets, 'complete_count': 0, 'complete_all_flag': False}
    for label, num in selected_counts.items():
        if label not in target_labels: continue
        label_en_cn = label+' '+eng_to_chn[label]
        infos['num_label'].append((num, label, eng_to_chn[label], np.round(num/target_counts*100,2)))
        message = f"类别{label_en_cn}"
        if num >= target_counts:
            infos['complete_count'] += 1
            message += f"已完成全部筛选，总共筛选了{num}张图片"
            delta = num - target_counts
            if delta > 0:
                message += f"并且多筛选了{delta}幅图片！"
                infos['total_target'] += delta
        else:
            message += f"已筛选{num}/{target_counts}个，还差{target_counts - num}个"
        infos['messages'].append(message)
    infos['messages'], infos['num_label'] = sort_zip(infos['messages'], keys=infos['num_label'])
    infos['num_label'] = enumerate(infos['num_label'])
    infos['complete_all_flag'] = (infos['complete_count'] == len(target_labels))
    return infos

@app.route("/", methods=['GET', 'POST'])
def index():
    login_check = True
    if request.method == 'POST':
        # print(request.form)
        name = request.form['name']
        if name in names:
            return redirect(f"/choose/{name}")
        else: login_check = False
    if mark.mark['total'] == 0:
        selected_rate = 0
    else:
        selected_rate = np.round(mark.mark['selected'] / mark.mark['total'] * 100, 2)
    infos = get_infos()
    # print(infos)
    return render_template("index.html", mark=mark.mark, login_check=login_check,
                           selected_rate=selected_rate, infos=infos)

def get_url_Paths(paths, label):
    count = 0
    url_Paths, tmp_paths = [], []
    for path in paths:
        tmp_paths.append((count, url_for('static', filename=f'cache/{label}/{path.name}')))
        count += 1
        if count % img_show_row == 0:
            url_Paths.append(tmp_paths)
            tmp_paths = []
    return url_Paths

def get_selected_idxs(form):
    seleted_idxs = []
    for key in form.keys():
        l = re.findall(r"img(\d+)", key)
        if len(l) == 0: continue
        seleted_idxs.append(int(l[0]))
    return seleted_idxs

@app.route("/choose/<name>", methods=['GET', 'POST'])
def choose(name):
    if request.method == 'POST' and 'submit' in request.form.keys() and bags[name] is not None:
        selected_idxs = get_selected_idxs(request.form)
        mark.update(name, len(selected_idxs), img_show_total)
        bags[name].update(selected_idxs)
        del bags[name]
        bags[name] = None
    if bags[name] is None:
        bags[name] = ImageBag()
    bag = bags[name]
    if bag.label == -1:
        return redirect("/")
    url_Paths = get_url_Paths(bag.paths, bag.label)
    label_verbose = bag.label + ' ' + eng_to_chn[bag.label]
    return render_template("choose.html", name=name, label=label_verbose, Paths=url_Paths,
                           row=img_show_row, column=img_show_column)

@app.route("/reset")
def reset():
    names = []
    for name, bag in bags.items():
        if bag is not None:
            names.append(name)
            print(f"解锁{name}未完成的类别{bag.label}")
            bag.reset()
            del bag
            bags[name] = None
    return f"重置所有用户的图片，当前正在处理的图片作废<br>重置的用户有{len(names)}位:{names}"


if __name__ == '__main__':
    bags = {}
    for name in names: bags[name] = None
    mark = Mark()
    app.run(debug=True, host='0.0.0.0')

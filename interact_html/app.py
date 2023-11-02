from manager import Manager, clean_cache, PATH_CACHE
from model import Model
from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from constant import target_labels, eng_to_chn

clean_cache(PATH_CACHE)
manager = Manager()
# model = Model('cnn')
model = Model('deeper_cnn')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        user = manager.add()
        return redirect(f"/interact/{user.id}")
    return render_template("index.html")

@app.route('/interact/<id>')
def interact(id):
    id = int(id)
    user = manager.get_user(id)
    if not user:
        return redirect("/")
    return render_template("interact.html",
                           table=user.table)

@socketio.on('refresh')
def reflesh(data):
    id = int(data['id'])
    user = manager.get_user(id)
    user.get_table()
    emit('update_show', {'table': user.table})

@socketio.on('upload_image')
def handle_upload_image(data):
    # print(data)
    id = int(data['id'])
    # print(id)
    user = manager.get_user(id)
    user.update_img(data['image_data'])
    # table_data = user.test_table()
    table_data = model.predict_table(user.img)
    # print(table_data)
    emit('update_data',
        # 'image_url' 已经不用了，原本测试是将画版而文件重新显示出来
        {'image_url': url_for("static", filename=user.get_relative_path()),
         'table_data': table_data})

@app.route('/info/')
def info():
    col = 10
    table, labels = [], []
    for idx, label in enumerate(target_labels):
        labels.append((label, eng_to_chn[label]))
        if (idx+1) % col == 0:
            table.append(labels)
            labels = []
    return render_template("info.html", table=table)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

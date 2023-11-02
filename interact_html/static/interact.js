canvas.width = 500
canvas.height = 500
//获取画笔
const ctx = canvas.getContext("2d")
ctx.fillStyle='green'
//是否绘画标记
var isDraw = false
//属性设置
const props = {
    // color: "#000",
    color: "#ffffff",
    size: 20
}
//画笔粗细
size.onchange = function () {
    props.size = this.value
}

//状态列表
var statusArr = []
statusArr[0]=ctx.getImageData(0, 0, canvas.width, canvas.height)
//总是指向当前状态
var statusIndex=0
//状态添加
function addStatus() {
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
    statusIndex++
    statusArr[statusIndex]=imageData
}
//绘画功能
function draw(x, y) {
    ctx.beginPath()
    //画笔颜色
    ctx.strokeStyle = props.color
    //画笔宽度
    ctx.lineWidth = props.size
    //绘画
    ctx.moveTo(x, y)
}
// 接收功能
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('update_data', function(data) {
    // 更新图片
    // var imgElement = document.querySelector('.fast_show img');
    // imgElement.src = data.image_url;

    // 更新表格
    var tableElement = document.getElementById('table');
    var tbody = tableElement.querySelector('tbody');
    tbody.innerHTML = '';
    data.table_data.forEach(function(row) {
        var tr = document.createElement('tr');
        row.forEach(function(cell) {
            var td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
});

//上传功能
function uploadImage() {
    console.log("上传图片")
    var image_data = canvas.toDataURL();
    // 从当前网址中提取 id 值
    var id = window.location.pathname.split('/').pop();
    socket.emit('upload_image', { image_data: image_data, id: id });
}
// 获取 Canvas 元素的相对位置和尺寸信息
var canvasRect = canvas.getBoundingClientRect();
var canvasX = canvasRect.left;
var canvasY = canvasRect.top;
//鼠标按下时开始
canvas.onmousedown = (e) => {
    isDraw = true
    draw(e.x-canvasX, e.y-canvasY)
}
//移动绘画
canvas.onmousemove = (e) => {
    if (isDraw) {
        ctx.lineTo(e.x-canvasX, e.y-canvasY)
        ctx.stroke()
    }
}
//停止绘画
canvas.onmouseup = () => {
    isDraw = false
    ctx.closePath()
    addStatus()
    let src = canvas.toDataURL("image/png")
    uploadImage()
}
//撤销
reback.onclick = () => {
    if(statusIndex>0){
        statusIndex--
    }
    let imageData = statusArr[statusIndex]
    ctx.putImageData(imageData,0,0)
    uploadImage()
}
//清空画布
clear.onclick = ()=>{
    ctx.clearRect(0,0,canvas.width,canvas.height)
    //初始化状态序列
    statusArr=[]
    statusArr[0]=ctx.getImageData(0, 0, canvas.width, canvas.height)
    statusIndex=0
}

// 根据网页中的刷新按钮，刷新show图片
document.getElementById('refresh').addEventListener('click', function() {
    console.log("按钮激活")
    // 从当前网址中提取 id 值
    var id = window.location.pathname.split('/').pop();
    socket.emit('refresh', { id: id });
});
// 接收新的show图片
socket.on('update_show', function(data) {
    // 更新show表格
    var tableElement = document.getElementById('show');
    var tbody = tableElement.querySelector('tbody');
    tbody.innerHTML = '';
    data.table.forEach(function(row) {
        var tr = document.createElement('tr');
        row.forEach(function(cell) {
            var td = document.createElement('td');
            cell.slice(0,2).forEach(function(string){
                var element = document.createElement('span');
                element.textContent = string
                td.appendChild(element)
                td.appendChild(document.createElement('br'))
            });
            var urlElement = document.createElement('img');
            urlElement.src = cell[2];
            td.appendChild(urlElement)
            // cell.forEach(function(param){
            //     var span = document.createElement('span');
            //     span.textContent = param;
            //     td.appendChild(span);
            //     td.appendChild(document.createElement('br'));
            // });
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
});
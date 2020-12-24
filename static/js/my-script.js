let info = document.querySelector('#id_info');
var board = document.querySelector('#id_board');
let isDragging = false;
let board_array;
let parrentOffSet;
let button_add_table;
var board_width;
var board_height;

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

let tableChange = document.querySelector('#id_tables')
tableChange.addEventListener('change', addInfo)

function sendServer(data, func_answer, ajax=true, url = document.location.pathname){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    if(ajax) xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(data);
    xhr.onload = function(){
        if (xhr.status != 200 ) {
            console.log('Ошибка ${xhr.status}: ${xhr.statusText}');}
        else if (func_answer){
            func_answer(JSON.parse(xhr.response));}
        else {
            data = JSON.parse(xhr.response);
            window.location=data.url;
        }
    }
}

function getNameDefault(){
        return "t"+(""+Date.now()).slice(-5);
}

function getValueResizeWidthBoard(){
    let width = window.innerWidth*0.8;
    if (width >= board_width) return width/board_width;
    else return board_width/width;
}

function resizeElem(elem, r, s){
    elem.style.width = elem.startwidth*r*s +'px';
    elem.style.height = elem.startheight*r*s + 'px';
}


function createBoard(){
    let div = document.createElement('div');
    div.classList.add("field");
    div.id = "id_field";
    div.startwidth = board_width;
    div.startheight =  document.querySelector('#id_length').value;;
    board.append(div);
    resizeElem(div, getValueResizeWidthBoard(), 0.5);
    board_array = div;
}

function createScheme(){
    board_width = document.querySelector('#id_width').value;
    board_height = document.querySelector('#id_length').value;
    if (!board_width || !board_height ) return;
    createBoard();
}

function addInfo(event){
    let i = event.target.value;
    let data = data_tables[i]
    let str_info = ''
    for(item in data){
        str_info += '<p>'+item +':'+ data[item] + '</p>';
    }
    str_info += '<button type="button" name="button" id="add_table">Добавить</button>';
    info.innerHTML = str_info
    button_add_table = document.querySelector('#add_table');
    button_add_table.addEventListener('click', _ => {
        addTable(data, i);
    })
}

function createDivTable(data, i, status=false ){
    let div = document.createElement('div');
    div.classList.add('table', data['shape']);
    div.startwidth = data['width']/100;
    div.startheight = data['length']/100;
    div.table_id = i;
    if (status){
        div.position_x = (10/(parseInt(board_array.style.width))*100).toFixed(2);
        div.position_y = (10/(parseInt(board_array.style.height))*100).toFixed(2);
        div.name_table = '';
        div.style.top = 10 + 'px';
        div.style.left = 10 + 'px';
        div.seats = data['max_seats'];
    }
    else{
        div.position_x = data['position_x'];
        div.position_y = data['position_y'];
        div.name_table = data['name_table'];
        div.innerHTML = data['name_table']
        div.style.top = data['position_y']+'%';
        div.style.left = data['position_x']+'%';
        div.seats = data['seats'];
        div.struct_id = data['id']
    }
    return div;
}

function addTable(data, i){
    if (confirm("Добавить стол")==false) return;
    let div = createDivTable(data,i, status=true);

    div.setAttribute('draggable', "true");
    board_array.append(div);
    resizeElem(div, getValueResizeWidthBoard(), 0.5);

    delete div.startwidth
    delete div.startheight

    div.addEventListener('dblclick', addName);
}

function addName(){
        let name = prompt("Введите имя", null);
        if (!name) return;
        this.name_table = name;
        this.innerHTML = '<p>' + name + '</p>';
    }


document.addEventListener('mousedown', event => {
    let dragElement = event.target.closest('.table');
    if (!dragElement) return;
    event.preventDefault();
    if (!parrentOffSet) parrentOffSet = dragElement.parentElement.getBoundingClientRect();
    dragElement.addEventListener('dragstart', _ => {return false;});
    startDrag(dragElement, event.clientX, event.clientY);
} )

function startDrag(element){
    if (isDragging) return;
    isDragging = true;
    document.addEventListener('mousemove',onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
    function onMouseMove(event){
        moveElement(element, event.clientX, event.clientY);
    }
    function onMouseUp(){
        if(!isDragging) return;
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }

    function moveElement(element, mouseX, mouseY){
        newLeft = mouseX - parrentOffSet.x - element.offsetWidth/2;
        newTop = mouseY - parrentOffSet.y - element.offsetHeight/2 +pageYOffset;
        if (newTop >= document.documentElement.clientHeight) window.scrollBy(0, 10);
        if (newTop <= 0) window.scrollBy(0, -10);
        if (newLeft <= 2) newLeft = 2;
        if (newLeft + element.offsetWidth >= parrentOffSet.width - 2) {
                newLeft =  parrentOffSet.width-element.offsetWidth-2;}
        if (newTop <= 2) newTop = 2;
        if ((newTop + element.offsetHeight) >= (parrentOffSet.height-2)) {
            newTop = parrentOffSet.height - element.offsetHeight-2;}
        element.style.top = newTop +'px';
        element.style.left = newLeft + 'px';
        element.position_x = (parseInt(element.style.left)/parrentOffSet.width*100).toFixed(2)
        element.position_y = (parseInt(element.style.top)/parrentOffSet.height*100).toFixed(2)
    }
}

function sendFormData(){
    if (!document.querySelector('#id_name').value) {
        alert('Введите название зала!');
        return};
    let dataTo = {};
    dataTo['hall'] = {}
    dataTo['hall']['restoran_id'] = document.querySelector('#id_restoran').value;
    dataTo['hall']['name'] = document.querySelector('#id_name').value;
    dataTo['hall']['width'] = parseInt(board_width);
    dataTo['hall']['length'] = parseInt(board_height);
    dataTo['tables'] = []
    if (board_array.childNodes.length){
        board_array.childNodes.forEach((item) => {
            dataTo['tables'].push(item);
        });
        console.log(dataTo);
        sendServer(JSON.stringify(dataTo), null, false)
    }
    else alert('Вы не разместили столы!');
}

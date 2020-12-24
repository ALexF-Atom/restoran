var span = document.getElementsByClassName("close")[0];
var modal = document.querySelector('#windowModal');
var tables = JSON.parse(document.querySelector('#tables').textContent);
var shape = JSON.parse(document.querySelector('#shape').textContent);
var board = JSON.parse(document.querySelector('#board').textContent);
var place = document.querySelector('#place');
var active;

span.addEventListener('click', disableModal);
document.addEventListener("DOMContentLoaded", createScheme)

function getValueResizeWidthBoard(){
    let width = window.innerWidth;
    if (width >= place.startwidth) return width/place.startwidth;
    else return place.startwidth/width;
}

function resizeElem(elem, r, s){
    elem.style.width = elem.startwidth*r*s +'px';
    elem.style.height = elem.startheight*r*s +'px';
}


function createBoard(){
    place.startwidth = board['width'];
    place.startheight =  board['height'];
    resizeElem(place, getValueResizeWidthBoard(), 1);
}


function addTextInfo(data){
	let status = '';
	if (data['reserved']=='busy') status = '(Забронирован)'
return '<div class="card-body"><h5 class="card-title">'
+data['name_table']+'</h5><p class="card-text">Столик для '
+data['seats']+' человек<br>'+status+'</div>'
// +'<a href="{{r.get_absolute_url}}">Заходите к нам</a></div>'
}

function addInfoTable(data){
	let div = document.createElement('div');
	div.classList.add('table', 'card', shape[data['shape']], data['reserved']);
	div.innerHTML = addTextInfo(data);
	div.style.top = data['position_y']+'%';
	div.style.left = data['position_x']+'%';
	div.struct_id = data['id'];
	div.startwidth = data['width']/100;
    div.startheight = data['height']/100;
    div.table_name = data['name_table']
	return div;
}

function createTable(){
	tables.forEach((data) => {
		let div = addInfoTable(data);
		place.append(div)
		resizeElem(div, getValueResizeWidthBoard(),1);
		div.addEventListener('click', reserv);
	});

}


function createScheme(){
	createBoard();
	createTable();
}


function reserv(){
	if (this.classList.contains('busy')) return;
	let table_id = document.querySelector('#id_reserver-table_id');
    let table_name = document.querySelector('#id_reserver-table_name');
	let date = document.querySelector('#id_reserver-date');
    table_id.value = this.struct_id;
    table_name.value = this.table_name;
	date.value =getDate();
	enableModal();

}
function enableModal(){
	modal.style.display = 'block';
}
function disableModal(){
	modal.style.display = 'none';
}

function getDate(){
	let date = document.querySelector('#id_date').value;
	return date;
}

function getLink(){
	window.location = getDate();
}

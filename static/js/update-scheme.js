


function addTableToBoard(){
	tables_scheme.forEach((table) => {
		let div = createDivTable(table, table.table_id);
		div.setAttribute('draggable', 'true')
		board_array.append(div);
	    resizeElem(div, getValueResizeWidthBoard(), 0.5);
	    delete div.startwidth;
	    delete div.startheight;
	    div.addEventListener('dblclick', addName);

	});
}

function createShemeUpdate(){
	board_width = document.querySelector('#id_width').value;
	board_height = document.querySelector('#id_length').value;
	createBoard();
	addTableToBoard();
}

document.querySelector('#button_update_board').addEventListener('click', sendFormData)
window.addEventListener('load', createShemeUpdate)

var modal = document.getElementById("windowModal");
var span = document.getElementsByClassName("close")[0];
var active;
var all_data_id = new Array()

//получение выбранной даты
function getDate(){
    let data = document.getElementById('id_date').value;
    return data
}
// управление выделением и модальным окном
span.addEventListener('click', event => {
    modal.style.display = "none";
    active.classList.remove('selected');
})
window.addEventListener('click', event => {
  if (event.target == modal) {
    modal.style.display = "none";
    active.classList.remove('selected')
}
})
document.querySelector('#parent').addEventListener('click', event => {
  const id = event.target.getAttribute('data-id');
  active = event.target
  if (!id) return;
  if (all_data_id.includes(parseInt(id))) return;
  active.classList.add('selected');
  modal.style.display = "block"
  document.getElementsByName('table')[0].value = id;
  document.getElementsByName('data_reserved')[0].value = getDate();
})

window.addEventListener('load', event=>{
    var value = JSON.parse(document.getElementById('reserv').textContent);
    if (value.length){
        value.forEach((item, i) => {
            let elem = document.getElementById('table'+item[0])
            elem.classList.add('busy');
            all_data_id.push(parseInt(elem.getAttribute('data-id')))
        });
    }
    console.log(all_data_id)
})

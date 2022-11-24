
console.log("Script for size is Running")

console.log("Script on chosing size");
var sizeChart = document.getElementsByClassName("sizeChart");
var sizes = document.getElementsByClassName("size");

for (var i = 0; i <= sizes.length - 1; i++) {
  sizes[i].addEventListener("click", function () {
    size_input = document.getElementById("size_input");
    size_input.value=this.innerText
    var current = document.getElementsByClassName("sizeCheck");
      
    if (current.length > 0) {
      current[0].className = current[0].className.replace("sizeCheck", "");
    }
    this.className += " sizeCheck";
    pd_id = document.getElementById('pd_id')
    $.ajax({
        type : 'GET',
        url : '/get_stock/'+pd_id.innerText+'/'+this.innerText
    }).done((data)=>{
        in_stock = document.getElementById('in_stock')
        in_stock.innerHTML ='In stock: '+ data

    })
  });
}
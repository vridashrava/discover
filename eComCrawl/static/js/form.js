var select = document.getElementsByTagName('select')[0];
select.onchange = function(){

  if(select.value == '2'){
    document.getElementsByTagName("table")[1].style.display="inline";
  }
  else{
    document.getElementsByTagName("table")[1].style.display = "none";
    document.getElementsByTagName("table")[2].style.display = "none";
  }

  if(select.value == '3'){
    document.getElementsByTagName("table")[1].style.display="inline";
    document.getElementsByTagName("table")[2].style.display="inline";
  }
  else{
    document.getElementsByTagName("table")[2].style.display = "none";
    document.getElementsByTagName("table")[3].style.display = "none";
  }

  if(select.value == '4'){
    document.getElementsByTagName("table")[1].style.display="inline";
    document.getElementsByTagName("table")[2].style.display="inline";
    document.getElementsByTagName("table")[3].style.display="inline";
  }
  else{
    document.getElementsByTagName("table")[3].style.display = "none";
    document.getElementsByTagName("table")[4].style.display = "none";
  }

  if(select.value == '5'){
    document.getElementsByTagName("table")[1].style.display="inline";
    document.getElementsByTagName("table")[2].style.display="inline";
    document.getElementsByTagName("table")[3].style.display="inline";
    document.getElementsByTagName("table")[4].style.display="inline";
  }
  else{
    document.getElementsByTagName("table")[4].style.display = "none";
    document.getElementsByTagName("table")[5].style.display = "none";
  }
  if(select.value == '6'){
    document.getElementsByTagName("table")[1].style.display="inline";
    document.getElementsByTagName("table")[2].style.display="inline";
    document.getElementsByTagName("table")[3].style.display="inline";
    document.getElementsByTagName("table")[4].style.display="inline";
    document.getElementsByTagName("table")[5].style.display="inline";
  }
  else{
    document.getElementsByTagName("table")[5].style.display = "none";
    document.getElementsByTagName("table")[6].style.display = "none";
  }

}

var opt = document.getElementById("urlOption");
opt.select = function(){
  if(select.value == "hover"){
    document.getElementById("xpath").style.display = "none";
  }
}

function show(){
  document.getElementsByTagName("table").innerHTML = url;
}


//Script for URL Option
var hoverLists = new Array(2) 
hoverLists["hover"] = ["True"]; 
hoverLists["clickAndHover"] = ["True"]; 
hoverLists["xpath"] = ["False"]; 


function hoverChange(selectObj) { 
  var idx = selectObj.selectedIndex; 
  var which = selectObj.options[idx].value; 
  cList = hoverLists[which]; 
  var cSelect = document.getElementById("hover"); 
  var len=cSelect.options.length; 
  while (cSelect.options.length > 0) { 
    cSelect.remove(0);
} 

var newOption; 
// create new options 
for (var i=0; i<cList.length; i++) { 
  newOption = document.createElement("option");
  newOption.value = cList[i];  // assumes option string and value are the same 
  newOption.text=cList[i]; 
  try { 
    cSelect.add(newOption);  // this will fail in DOM browsers but is needed for IE 
  } 
  catch (e) { 
    cSelect.appendChild(newOption); 
  } 
} 
}


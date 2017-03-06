<!-- <select id="selectElementId" onfocus="year_pop(this.id)"></select> -->


function year_pop(s){

    var min = 1960,
    max = 2016,
    select = document.getElementById(s);

    for (var i = min; i<=max; i++){
       var opt = document.createElement('option');
       opt.value = i;
       opt.innerHTML = i;
       select.appendChild(opt);
    }
}
function populate(s1,s2){
	var s1 = document.getElementById(s1);
	var s2 = document.getElementById(s2);
	s2.innerHTML = "";
	if(s1.value == "a"){
		var optionArray = ["|","camaro|Camaro","corvette|Corvette","impala|Impala"];
	} else if(s1.value == "b"){
		var optionArray = ["|","avenger|Avenger","challenger|Challenger","charger|Charger"];
	} else if(s1.value == "c"){
		var optionArray = ["|","mustang|Mustang","shelby|Shelby"];
	}
	for(var option in optionArray){
		var pair = optionArray[option].split("|");
		var newOption = document.createElement("option");
		newOption.value = pair[0];
		newOption.innerHTML = pair[1];
		s2.options.add(newOption);
	}
}

function populateOptions(pk, url1, url2, selector1, selector2){
    if (pk == 'No'){
      $(selector1).html('');
      $(selector2).html('');

    }
    else {
      $.when(
        $.ajax({
          url: url1,
          data: {'pk':pk },
          dataType: 'json',
        }),
        $.ajax({
          url: url2,
          data: {'pk':pk },
          dataType: 'json',
        })
      ).then(function([data1], [data2]){
          console.log(data1);
          var options1 = '<option value="No"> Select Level of Aggregation</option>';
          for (var i = 0; i < data1.length; i++){
            options1 += '<option value="' + data1[i].pk + '">' + data1[i].fields['name'] + '</option>'
          };
          console.log(options1, data1.length)
          $(selector1).html(options1);

          console.log(data2);
          var options2 = '<option value="No"> Select Frequecny</option>';
          for (var i = 0; i < data2.length; i++){
            options2 += '<option value="' + data2[i].pk + '">' + data2[i].fields['name'] + '</option>'
          };
          console.log(options2, data2.length)
          $(selector2).html(options2);         

          

        });
    
    }
  }


            
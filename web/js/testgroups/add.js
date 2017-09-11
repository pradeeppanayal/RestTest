

/*
Author    : Pradeep CH
Date      : 15-Aug-2017
Version   : 1.0.0
Since     : 1.0.0
*/

$(document).on('click', '#reset', function (event) {  
	event.preventDefault(); 
	$('#name').val('')
	$('#module').val('')
	$('#desc').val('')
});

$(document).on('click', '#save', function (event) {  
	event.preventDefault(); 
	name = $('#name').val()
	module = $('#module').val()
	desc = $('#desc').val()
        data = {'testname':name,'description':desc,'module':module}
        $.doPost('/rtest/create',data,loadResp)
});

function loadResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error'])
	}else{
		showSuccessMessage(obj['data'])
	}
}

function loadConsoleData(c){
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html(c).fadeIn(200)})
}

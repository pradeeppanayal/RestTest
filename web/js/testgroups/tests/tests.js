

/*
Author    : Pradeep CH
Date      : 15-Aug-2017
Version   : 1.0.0
Since     : 1.0.0
*/
 
$( document ).ready(function() {
   loadTests()
});

function loadTests(){
   url = getURL()
   parts = url.split('/')
   testGroupName = parts[parts.length-1]
   $('#testGroupName').html(testGroupName)
   targetUrl = '/rtest/'+testGroupName+'/tests'
   addLink = '/web/testgroups/tests/'+testGroupName+'/createTest'
   $('#addTest').attr('href',addLink)
   console.log($('#addTest'))
   $.doGet(targetUrl,loadResp)
}

function loadResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error']) 
	}else{
		content = ''
		deviceResp = obj['data']['tests']
		$.each(deviceResp,function(){
                        entry = this
			col1 = '<td><input type="checkbox" id='+entry.name+'></td>' 
			col2 = '<td>'+entry.name+'</td>'
			col3 = '<td>'+entry.api+'</td>'
			col4 = '<td>'+entry.type+'</td>'
			col5 = '<td>'+entry.order+'</td>'
                        $('#tests tr:last').after('<tr>'+col1+col2+col3+col4+col5+'</tr>');			
		});
		showInfo("Tests are loaded")
	}
}

function loadConsoleData(c){
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html(c).fadeIn(200)})
}

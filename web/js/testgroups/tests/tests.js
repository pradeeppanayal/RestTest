

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
   $('#delBut').hide()
   $('#editBut').hide()

   url = getURL()
   parts = url.split('/')
   testGroupName = parts[parts.length-1]
   $('#testGroupName').html(testGroupName)
   targetUrl = '/rtest/'+testGroupName+'/tests'
   addLink = '/web/testgroups/tests/'+testGroupName+'/createTest'
   uploadlink = '/web/testgroups/tests/'+testGroupName+'/uploadTests'
   $('#addTest').attr('href',addLink)
   $('#uploadTest').attr('href',uploadlink)
   console.log($('#addTest'))
   $.doGet(targetUrl,loadResp)
}

function getSelecetdTestGroups(){
   names = []
   $.each($('.select'),function(){
        if(this.checked){
           names.push(this.name)
        }
  });
  return names;
}

function loadResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error']) 
	}else{
		var content = ''
		var deviceResp = obj['data']['tests']
                $("#tests").find("tr:gt(0)").remove();
		$.each(deviceResp,function(){
                        entry = this
			col1 = '<td><input type="checkbox" name='+entry.name+' class="select"></td>' 
			col2 = '<td>'+entry.name+'</td>'
			col3 = '<td>'+entry.api+'</td>'
			col4 = '<td>'+entry.type+'</td>'
			col5 = '<td>'+entry.order+'</td>'
                        $('#tests tr:last').after('<tr>'+col1+col2+col3+col4+col5+'</tr>');			
		});
		showInfo("Tests are loaded")
	}
}

$(document).on('click', '#deleteTests', function (event) {  
   event.preventDefault(); 
   var testnames = getSelecetdTestGroups()
   var targetUrl = '/rtest/tests/delete'
   var data = {'testgroupname':testGroupName,testnames}
   $.doPost(targetUrl,data,loadActResp)
   
});

$(document).on('click', '#editTest', function (event) {  
   event.preventDefault(); 
   var testnames = getSelecetdTestGroups()
   updateLink = '/web/testgroups/tests/'+testGroupName+'/createTest?testname=' + testnames[0]
   redirect(updateLink)   
});


function loadActResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error']);
	}else{
		showSuccessMessage(obj['data']);
		loadTests();
	}
}


$(document).on('change', '.select', function (event) {  
   var testnames = getSelecetdTestGroups()
   $('#delBut').hide()
   $('#editBut').hide()
   if(testnames.length ==1){
        $('#editBut').show()
   }
   if(testnames.length > 0){
        $('#delBut').show()
   }
});
function loadConsoleData(c){
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html(c).fadeIn(200)})
}

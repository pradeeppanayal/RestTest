
/*
Author    : Pradeep CH
Date      : 16-Aug-2017
Version   : 1.0.0
Since     : 1.0.0
*/

testGroupName =''
$( document ).ready(function() {
    loadTests()
});
function loadTests(){
   url = getURL()
   
   parts = url.split('/')
   testGroupName = parts[parts.length-2] 
   $('#testGroupName').html(testGroupName)
   $('#testGroupName').attr('href','/web/testgroups/tests/'+testGroupName)
}

$(document).on('change', '#type', function (event) {  
	event.preventDefault(); 
        $('#payload').attr('disabled',$('#type').val()==='GET')
});

$(document).on('click', '#next1', function (event) {  
	event.preventDefault(); 
        $('#tryTab').click()
});

$(document).on('click', '#next2', function (event) {  
	event.preventDefault(); 
        var apiendpoint = $('#apiendpoint').val()
        var api = $('#api').val()
        var type = $('#type').val()
        var cookies = $('#cookies').val()
        var headers = $('#headers').val()
        var payload = type==='GET'?'':$('#payload').val()
        var data = {'api':api,'apiendpoint':apiendpoint,'type':type,'payload':payload,'headers':headers,'cookies':cookies}
        $.doPost('/rtest/getResponse',data,getResponseData)
        //$('#respTab').click()
});

function getResponseData(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error'])
	}else{
		$('#response').val(JSON.stringify(obj['data'],null,4))
        	$('#respTab').click()
        } 
}
$(document).on('click', '#next3', function (event) {  
	event.preventDefault(); 
        $('#valTab').click()
        resp = $('#response').val()
        if (resp === undefined || resp ===''){
		showError('There is no response to load')
		return	
	}
        jsonObj = JSON.parse(resp)
        generateResponseView(jsonObj);
});

$(document).on('click', '#next4', function (event) {  
	event.preventDefault();   
        prepareValidationJson();

        var apiendpoint = $('#apiendpoint').val()
        var cookies = $('#cookies').val()
        var headers = $('#headers').val()
        var envData = {'apiEndPoint':apiendpoint,'headers':headers,'cookies':cookies}

        var name = $('#name').val()
        var api = $('#api').val()
        var type = $('#type').val()
        var payload = type==='GET'?'':$('#payload').val() 
        var response = $('#response').val()
        var target = '/rtest/getValidationResult'
        var data= {'validations':rules,'response':response,'testname':name,'envData':envData,'testGroupName':testGroupName}
        $.doPost(target,data,loadValidationResp)
        
});

function loadValidationResp(r){
   if(r === undefined){
     showError('Invalid response from the server. :(')    
     return
   }
   if(r['status'] === 'error'){
     showError(r['error'])    
     return
   }   
   reportGenerator(r)
   $('#reportTab').click()
}

$(document).on('click', '#saveTest', function (event) {  
	event.preventDefault(); 
        var type = $('#type').val()
        var payload = type==='GET'?'':$('#payload').val()
        var name = $('#name').val()
        var api = $('#api').val()
        var target = '/rtest/tests/add'
        var testdata = {'api':api,'type':type,'payload':payload,'name':name}
        $.doPost(target,{'testname':testGroupName,'testdata':testdata,'validations':rules},loadResp)
});

function loadResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error'])
	}else{
		showSuccessMessage(obj['data'])
	}
}

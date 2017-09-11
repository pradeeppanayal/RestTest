

$( document ).ready(function() {
	loadGroups()
});
testnames = []
function loadGroups(){
   
   var param = getParamValue('testnames')

   if(param === undefined){
     showError('No testnames to prpare the validation response')
     return
   } 

   testnames = param.split(',') 
}

$(document).on('click', '#genarate', function (event) {   
	event.preventDefault();   

    	var apiendpoint = $('#apiendpoint').val()
        var cookies = $('#cookies').val()
        var headers = $('#headers').val()
        var envData = {'apiEndPoint':apiendpoint,'headers':headers,'cookies':cookies}
        target = '/rtest/validate'
        var data = {'envData':envData,testGroupNames:testnames}
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

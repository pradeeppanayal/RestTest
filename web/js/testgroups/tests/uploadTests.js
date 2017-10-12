
/*
Author    : Pradeep CH
Date      : 09-Oct-2017
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

$(document).on('click', '#uploadfiles', function (event) {  
	event.preventDefault();  
	var files = $('#my-file-selector')[0].files;  
        if(files === undefined || files.length==0){
		showError("Please select a file.")
		return;
        }else if(files.length>1){
		showError("Multiple files are not supported yet :(")
		return;
        }
        var target = '/rtest/tests/uploadTests';
        var data = new FormData()
        data.append("testGroupName", testGroupName);
        data.append("file1", files[0]);
        $.triggerPOSTCallWithoutContentType(target,data,loadResp)
	
});

function loadResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error'])
	}else{
		showSuccessMessage(obj['data'])
	}
}
 

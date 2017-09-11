

/*
Author    : Pradeep CH
Date      : 14-Aug-2017
Version   : 1.0.0
Since     : 1.0.0
*/

$( document ).ready(function() {
	loadGroups()
});

function loadGroups(){
   $.doGet('/rtest/testgroups',loadResp)
}

function loadResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error']) 
	}else{
		content = ''
		deviceResp = obj['data']
                $("#servers").find("tr:gt(0)").remove();
		$.each(deviceResp,function(){
                        entry = this
			col1 = '<td><input type="checkbox" name='+entry.name+' class="sel"></td>'
                        viewLink = "<a href='/web/testgroups/tests/"+entry.name+"'>"+ entry.name+"</a>"
			col2 = '<td>'+viewLink+'</td>'
			col3 = '<td>'+entry.module+'</td>'
                        d= new Date(entry.date)
			col4 = '<td>'+d.toUTCString()+'</td>'
			col5 = '<td>'+entry.description+'</td>'
                        $('#servers tr:last').after('<tr>'+col1+col2+col3+col4+col5+'</tr>');			
		});
		showInfo("Test groups are loaded")
	}
}

function loadActionResp(obj){
	if (obj['status'] =='error'){ 
		showError(obj['error']) 
	}else{
		showInfo(obj['data'])
		
	}
        //to just show the delete message :P
        setTimeout(function() {
			loadGroups()
  	}, 200);

}
function getSelecetdTestGroups(){
   names = []
   $.each($('.sel'),function(){
        if(this.checked){
           names.push(this.name)
        }
  });
  return names;
}

$(document).on('click', '#delete', function (event) {  
   event.preventDefault(); 
   var names = getSelecetdTestGroups()
   if(names.length == 0){
	showError("No test groups are selected to perform action") 
   	return
   }
   $.doPost('/rtest/delete',{'testgroupnames':names},loadActionResp)
});


$(document).on('click', '#execute', function (event) {  
   event.preventDefault(); 
   var names = getSelecetdTestGroups()
   if(names.length == 0){
	showError("No test groups are selected to perform action") 
   	return
   }// similar behavior as clicking on a link
   redirect("/web/testgroups/reportViewer?testnames="+names.toString());
});


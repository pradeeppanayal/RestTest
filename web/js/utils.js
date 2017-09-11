
homeURL = '/web/testgroups'

function showError(m){
    showMessage('alert-danger','Error!',m)
}

function showSuccessMessage(m){
    showMessage('alert-success','Success!',m)
}

function showInfo(m){
    showMessage('alert-info','Info!',m)
}

function showMessage(c,h,m){
    d= '<div class="alert '+c+' alert-dismissable" > <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a> <strong>'+h+'</strong>'+ m+'</div>'
    $('#consoleContent').html(d).fadeIn(200)
}

function getURL(){
   return document.location.href
}

function getParamValue(paramName){ 
        var url = getURL()
	var a = url.split('?')
	if(a.length!=2){
		return;
	}
	var a = a[1].split('&')
	var i = 0
	while(i<a.length){
		var b = a[i].split('=')		
		if(paramName == b[0] ){
			return b[1]
		}
		i++;
	}
}

function redirect(url){   
   window.location.href =url; "/web/testgroups/reportViewer?testnames="+names.toString();;
}

function goHome(){
  redirect(homeURL)
}

$(document).on('click', '#home', function (event) {    
   event.preventDefault();   
   goHome()
});
function log(msg){
	console.log(msg)
}

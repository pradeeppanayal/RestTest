//Jquery extention file
/*

Author  : Pradeep CH
Version : 1.0.0
Since   : 1.0.0
Date    : Mon Aug 14 2017

This file extends jquery to add two more feture to trigger post call and a API hit
*/

$.extend({ 
              doGet : function(target,targetMethod){
			$.ajax({
       				url: target,
       				type: 'GET',
       				success: function(response, status, xhr){  
					targetMethod(response);
				}
			});  
		},

              doPost : function(target,bodyContent,targetMethod){
                        bodyContent = JSON.stringify(bodyContent)
			$.ajax({
       				url: target,
       				type: "POST",
       				data: bodyContent,
                                dataType:'json',
                                contentType:'application/json',
       				success: function(response, status, xhr){  
					targetMethod(response);
				}
			});  
		} ,
		triggerPOSTCallWithoutContentType : function(target,bodyContent,targetMethod){
			$.ajax({
				url: target,
       				data: bodyContent,
    				cache: false,
   				contentType: false,
    				processData: false,
    				type: 'POST',
       				success: function(response, status, xhr){  
					targetMethod(response);
				}
			});  
		}
});

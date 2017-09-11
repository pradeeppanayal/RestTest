
/*
Author    : Pradeep CH
Date      : 19-Aug-2017
Version   : 1.0.0
Since     : 1.0.0
*/


validationIds = {}

function generateResponseView(resp){    
  rules = {}
  validationIds = {}

  var data = generateView(resp,'root')  
  var content = data[0]
  validationIds = data[1]
  $('#formatResp').html(content)
}

function generateView(jsonObj,name){
   type = jQuery.type(jsonObj)
   //get ite info
   var item = {}
   item['id'] = name
   nameParts = name.split('_')
   item['name'] = nameParts[nameParts.length-1]
   item['type'] = type

   //head
   var main = '<div class="panel panel-default">';  
   main += '	<div class="panel-heading" role="tab">';
   main += name.replace(/_/g,'/')
   main += '			<a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#' + name + '" aria-expanded="false" aria-controls="collapseThree"><span class="glyphicon glyphicon-chevron-down pull-right"></span></a>';
   main += '              </h4>'
   main += '      </div>';
   //body
   main += '      <div id="' + name + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">';
   main += ' 	     <div class="panel-body">'

   main += '	<label id="'+name+'Type">Type:'+type+'</label>'
   if (type==='object'){ 
      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Validate">Validate</label>' 
      main += '		</div>'


      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Size">Size</label>'
      main += '			<label> <input type="textBox" value="'+Object.keys(jsonObj).length+'" placeholder="size" id="'+name+'SizeVal" />' 
      main += '		</div>'

      main += '	<div>Properties</div>'
      main += '	<div id="'+name+'Properties">'
      var properties = []
      $.each(Object.keys(jsonObj),function(){
         var data = generateView(jsonObj[this],name+'_'+this)
         main +=data[0]
         properties.push(data[1])
       });

      item['property'] =properties
      main += '	</div>' 
   }else if (type === 'array'){ 
      
      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Validate">Validate</label>' 
      main += '		</div>'

      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Size">Size</label>'
      main += '			<label> <input type="textBox" value="'+jsonObj.length+'" placeholder="size" id="'+name+'SizeVal" />' 
      main += '		</div>'
      var properties = []
      if(jsonObj.length >0){
           obj = jsonObj[0]
       	   main += '	<div class="well" id="'+name+'Properties">'
           var data = generateView(obj,name+'_Item')
           main +=data[0]
           properties.push(data[1])
           main += '	</div>'           
      }
      item['property'] =properties
      main += '	</div>' 
   }else{// if (type === 'string'  ){ 
      
      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Validate">Validate</label>'  
      main += '		</div>'
 
      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Value">Expected</label>'
      main += '			<label> <input type="textBox" placeholder="" value="'+jsonObj+'" id="'+name+'ExpectedVal" />' 
      main += '		</div>'

      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Track">Track</label>'
      main += '			<label> <input type="textBox" placeholder="Track name" id="'+name+'TrackName" />' 
      main += '		</div>'

      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Header">Add to Header</label>'
      main += '			<label> <input type="textBox" placeholder="Header name" id="'+name+'HeaderName" />' 
      main += '		</div>'

      main += '		<div class="checkbox">'
      main += '			<label><input type="checkbox" id="'+name+'Cookie">Add to Cookies</label>'
      main += '			<label> <input type="textBox" placeholder="cookie name" id="'+name+'cookieName" />' 
      main += '		</div>'
      
   }
    main += '           </div>';
    main += '      </div>';
    main += '</div>'
   return [main,item];
   
} 

rules = {}

function prepareValidationJson(){
   if(validationIds.length == 0){
	showError('There is nothing to validate')
        return
   }
   rules = frameRules(validationIds)
}

function frameRules(item){
   var main = {}
   main['name'] = item['name']
   main['type'] = item['type']
   var idPrefix = item['id']

   main['validate'] = $('#'+idPrefix+'Validate')[0].checked;

   if(item['type']==='object' || item['type']==='array'){
      main['properties'] = []
      
      if (main['validate']){
          main['validateSize'] = $('#'+idPrefix+'Size')[0].checked;
          if(main['validateSize'] ){
             main['expectedSize'] = $('#'+idPrefix+'SizeVal').val()
          }
      } 

      $.each(item['property'],function(){
         main['properties'].push(frameRules(this));
      });
   }else{//boolean string int
      if(main['validate'] === true){
         main['validateExpectedValue'] =$('#'+idPrefix+'Value')[0].checked;
         if(main['validateExpectedValue']){
            main['expectedValue'] =$('#'+idPrefix+'ExpectedVal').val();        
         }
      }
         main['trackValue'] =$('#'+idPrefix+'Track')[0].checked;
         if(main['trackValue']){
            main['trackName'] =$('#'+idPrefix+'TrackName').val();        
         }
         main['addToHeader'] =$('#'+idPrefix+'Header')[0].checked;
         if(main['Header']){
            main['headerName'] =$('#'+idPrefix+'HeaderName').val();        
         }
         main['addToCookie'] =$('#'+idPrefix+'Cookie')[0].checked;
         if(main['addToCookie']){
            main['cookieName'] =$('#'+idPrefix+'cookieName').val();        
         }
   }
   return main;
}


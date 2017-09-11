/*
Author    : Pradeep CH
Date      : 19-Aug-2017
Version   : 1.0.0
Since     : 1.0.0
*/
function reportGenerator(resp) {
    console.log(resp)
    var testGroupContent = generateTestGroupContainers(resp)
    $('#testsIndex').html(testGroupContent)

    var content = ''
    $.each(Object.keys(resp), function() {
        var tests = resp[this]
        var currentTestGroupName = this

        content += '<div id="' + this + '" class="tab-pane fade">'
        content += '	<div class="accordion-wrap accordion-wrap-ext">';
        content += '	     <div class="accordion-option">';
        content += '         	<h5 class="title">' + currentTestGroupName + '</h5>';
        content += '	      </div>';
        content += '           <div class="clearfix"></div>';
        $.each(tests, function() {
            var name = Object.keys(this)[0]
            var item = this
            content += '		' + generateTest(name, item[name])
        });
        content += '</div>'
    });
    $('#testsContent').html(content)
}

function generateTest(name, data) {
    
    var main = '<div class="panel panel-default">';
    main += '	<div class="panel-heading" role="tab">';
    main += '	<div class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#' + name + '" aria-expanded="false" aria-controls="collapseThree">';
    main += '	<h4 class="panel-title">';
    main += name;
    main += ' <span class="label label-primary">'+data['total']+'</span>       ';
    main += '  <span class="label label-success">'+ data['success'] + '</span>  ';  
    main += '  <span class="label label-danger">' + data['failed'] + '</span>    ';

    main += data['total'] == data['success'] ? '<span class="label label-success">Pass</span> ' : '<span class="label label-danger">Fail</span> '; 
    
    main += '			<span class="glyphicon glyphicon-chevron-down pull-right"></span>'
    main += '              </h4>'
    main += '        </div>';
    main += '      </div>';
    main += '      <div id="' + name + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">';
    main += ' 	     <div class="panel-body">'
    main += genarateReport(data,name)
    main += '           </div>';
    main += '      </div>';
    main += '</div>'
    return main

}

function generateTestGroupContainers(testGroups) {
    var main = ''
    $.each(Object.keys(testGroups), function() {
        main += '<li><a data-toggle="tab" href="#' + this + '">' + this 
        var item = testGroups[this]
        var total = 0;
        var success = 0;
        
        $.each(item,function(){
           var testname= Object.keys(this)[0]
           var subTest = this[testname]
           total +=subTest['total'] ;
           success +=subTest['success'] ;
        });
        main += ' <span class="label label-primary">'+total+'</span>       ';
        main += '  <span class="label label-success">'+ success + '</span>  ';  
        main += '  <span class="label label-danger">' +(total-success) + '</span>    ';
        main += total==success ? '<span class="label label-success">Pass</span> ' : '<span class="label label-danger">Fail</span> ';
        main +='</a></li>'
        
    });
    return main;
}

function genarateReport(item,gname) { 

    var name = gname+'_'+item['validations']['name'] 

    var main = '<div class="panel panel-default">';
    main += '	<div class="panel-heading" role="tab">';
    main += '	<div class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#' + name + '" aria-expanded="false" aria-controls="collapseThree">';
    main += ' <h4 class="panel-title">';
    main += ' '+item['validations']['name']+'';
    main += ' <span class="label label-primary">'+item['total']+'</span>       ';
    main += '  <span class="label label-success">'+ item['success'] + '</span>  ';  
    main += '  <span class="label label-danger">' + item['failed'] + '</span>    ';

    main += item['total'] == item['success'] ? '<span class="label label-success">Pass</span> ' : '<span class="label label-danger">Fail</span> ';

    main += '	<span class="glyphicon glyphicon-chevron-down pull-right"></span>';
    main += '              </h4>'
    main += '        </div>';
    main += '      </div>';
    main += '      <div id="' + name + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">';
    main += ' 	     <div class="panel-body">'

    main += ' 	<table class="table" >'
    //add header
    main += '		<tr>'
    main += '				<th>Status</th>'
    main += '				<th>Key</th> '
    main += '				<th>Details</th> '
    main += '	        </tr>'
    //rows
    if (jQuery.inArray("validations", Object.keys(item['validations'])) > -1) {
        $.each(item['validations']['validations'], function() {
            main += '<tr>'
            main += '<td>' + this.testStatus + '</td>'
            main += '<td>' + this.itemName + '</td>'
            main += '<td>' + this.validationResp + '</td>'
            main += '</tr>'
        });
    }
    main += ' 	</table>'
    //load properties if any
    if (jQuery.inArray("properties", Object.keys(item['validations'])) > -1) {
        $.each(item['validations']['properties'], function() {
            main += genarateReport(this,name)
        });
    } 
    main += '           </div>';
    main += '      </div>';
    main += '</div>'
    return main
}



###########################
#                         #
#   Author : Pradeep CH   #
#  Date  : 10- Aug -2017  #
#                         #
###########################

from flask import Flask, request, send_from_directory,Response
import json

from testrunner import APIInvoker
from testrunner import TestExecutionWatcher
from testrunner import TestGroupExecutorDemo
from testrunner import executeTestGroups

from rtester import TestManager,view
from rtester import RXLImporter

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

#HTML
#index
@app.route('/web/restest')
def getHome():
    return send_from_directory('web/html/', 'index.htm') 

#test group
@app.route('/web/testgroups')
def staticIndex():
    return send_from_directory('web/html/testgroups/', 'view.htm') 
#add execute delete file
@app.route('/web/testgroups/<fname>')
def testGroupFiles(fname):
    print fname
    return send_from_directory('web/html/testgroups/', fname+'.htm') 

@app.route('/web/testgroups/tests/<groupname>')
def testGroupTests(groupname):
    #groupname is not used a single page will be loaded, another api call to get the tests
    return send_from_directory('web/html/testgroups/tests/', 'view.htm')  

@app.route('/web/testgroups/tests/<groupname>/<fname>')
def testGroupTestFiles(groupname,fname):
    #groupname is not used a single page will be loaded, another api call to get the tests
    return send_from_directory('web/html/testgroups/tests/', fname+'.htm')  

@app.route('/web/style/<filename>')
def cssFiles(filename):
    return send_from_directory('web/style/', filename)
#JS
@app.route('/web/js/<folder>/<filename>.js')
def jsFiles(folder,filename):
    return send_from_directory('web/js/'+folder+'/', filename+'.js')

#Other web files
@app.route('/web/fonts/<filename>')
def fonts(filename):
     
    return send_from_directory('web/fonts/', filename)

#JS
@app.route('/web/js/<folder1>/<folder2>/<filename>.js')
def jsFilesInnerFolder(folder1,folder2,filename):
    return send_from_directory('web/js/'+folder1+'/'+folder2+'/', filename+'.js')

@app.route('/web/js/<filename>.js')
def jsFilesFromRoot(filename):
    return send_from_directory('web/js/', filename+'.js')

#API
@app.route('/rtest/validate',methods=['POST'])
def validateTestGroup():
   data = request.get_json(silent=True)  
   try:  
      assert 'envData' in data.keys(),'envData is required'
      assert 'testGroupNames' in data.keys(),'testGroupNames is required'
      resp = executeTestGroups(data['envData'] , data['testGroupNames'])
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json')   

#API
@app.route('/rtest/getResponse',methods=['POST'])
def getResp():
   data = request.get_json(silent=True)  
   try:  
      resp = APIInvoker.invoke(data)
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json')  

@app.route('/rtest/getValidationResult',methods=['POST'])
def getValidationResp():
   data = request.get_json(silent=True)  
   try:  
      watcher = TestGroupExecutorDemo () 
      resp = watcher.executeTest(data['testGroupName'],data['testname'],data['envData'],data['response'],data['validations'])
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json')  

@app.route('/rtest/create',methods=['POST'])
def createTestGroup():
   data = request.get_json(silent=True)  
   try:
      assert  data,'Invalid payload'
      assert 'testname' in data.keys() and data['testname']!='','testname required'
      manager = TestManager(data['testname'])
      resp = manager.create(data)
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json')   

@app.route('/rtest/delete',methods=['POST'])
def deleteTestGroup():
   data = request.get_json(silent=True)  
   try:
      assert  data,'Invalid payload'
      assert 'testgroupnames' in data.keys(),'testname cannot be null' 
      for name in data['testgroupnames']:
         manager = TestManager(name)
         manager.delete()
      resp = {'status':'success','data':'Test groups deleted'}
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json')   

@app.route('/rtest/tests/add',methods=['POST'])
def addTest():
   data = request.get_json(silent=True)  
   try:
      assert  data,'Invalid payload'
      assert 'testname' in data.keys() and data['testname']!='','testname required' 
      manager = TestManager(data['testname'])
      resp = manager.addTest(data)
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

@app.route('/rtest/tests/update',methods=['POST'])
def updateTest():
   data = request.get_json(silent=True)  
   try:
      assert  data,'Invalid payload'
      assert 'testname' in data.keys(),'testname cannot be null' 
      assert 'testdata' in data.keys(),'testdata cannot be null' 

      manager = TestManager(data['testname'])
      resp = manager.updateTest(data)
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

@app.route('/rtest/tests/uploadTests',methods=['POST'])
def uploadTest(): 
   try:
      testGroupName = request.form['testGroupName']
      assert testGroupName,"Test group name required"
      assert  len(request.files)>0,'Please upload a file'
      assert  len(request.files)==1,'Multiple files are not supported yet :(' 
      uploadedFile = request.files['file1']
      assert uploadedFile and uploadedFile.filename !='',"Invalid file"
      filename = uploadedFile.filename#secure_filename(file.filename)
      importer = RXLImporter(uploadedFile,filename,testGroupName)
      resp = importer.importTests()       
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

@app.route('/rtest/tests/delete',methods=['POST'])
def deleteTests():
   data = request.get_json(silent=True)  
   try:
      assert  data,'Invalid payload'
      assert 'testgroupname' in data.keys(),'testname required' 
      assert 'testnames' in data.keys(),'testnames required' 
      manager = TestManager(data['testgroupname'])
      resp = manager.removeTests(data['testnames'])
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

@app.route('/rtest/testgroups',methods=['GET'])
def getall():  
   try: 
      resp = view.getAll()
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

@app.route('/rtest/<groupname>/tests',methods=['GET'])
def getTestsByGroup(groupname):  
   try: 
      manager = TestManager(groupname)
      resp = manager.getTests()
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

@app.route('/rtest/<groupname>/<testname>',methods=['GET'])
def getTestDetailsByGroupAndName(groupname,testname):  
   try: 
      manager = TestManager(groupname)
      resp = manager.getTestdata(testname)
   except Exception as e:
      resp = {'status':'error','error':str(e)} 
   resp = json.dumps(resp)
   return Response(resp, mimetype='application/json') 

if __name__ == "__main__":
   app.run(host= '0.0.0.0',threaded=True)



###########################
#                         #
# Author : Pradeep CH     #
# Date  : 10- Aug -2017   #
#                         #
###########################


import shutil
import os
from os.path import expanduser 
import json
import datetime
import uuid

from ArchiveManager import zipTest

sourcedirectory =  expanduser("~") + "/rtest/"
sourceFile = sourcedirectory + '/tests.json'
archiveFolder = sourcedirectory+'archive'

__author__='Pradeep CH'
__version__='1.0.0'


PAYLOAD_FILE = 'Payload.json'
TEST_FILE = 'Tests.json'
VALIDATION_FILE = 'Validations.json'

def readFile(fname):
   assert os.path.exists(fname),"Test "+ fname +" not found"
   with open(fname,'r') as f:
      return json.loads(f.read())

def writeFile(fname,data):
   #assert not os.path.exists(fname),"Test "+ fname +" not found"
   with open(fname,'w') as f:
      return f.write(data)

class TestManager(object):
   def __init__(self,testname):
      self.testname = testname
      self.dir = sourcedirectory + testname
      self.payloadFile = self.dir+'/' + PAYLOAD_FILE
      self.testFile = self.dir+'/' + TEST_FILE
      self.validationFile = self.dir+'/' + VALIDATION_FILE   

   def create(self,data):      
      assert 'description' in data.keys() and data['description']!='','description is required'
      assert 'module' in data.keys() and data['module']!='','module required'

      description = data['description']
      module= data['module']
 
      assert not os.path.exists(self.dir),"Test "+ self.testname +" is exist"      
      os.mkdir(self.dir)
      writeFile(self.payloadFile, '{}')
      writeFile(self.validationFile, '{}')
      writeFile(self.testFile , json.dumps({  "tests":{}}))
      data = readFile(sourceFile)
      date = datetime.datetime.now()

      #register the test
      data[self.testname] ={'name':self.testname,'description':description,"module":module,'date':str(date)}
      writeFile(sourceFile,json.dumps(data))
      return {'status':'success','data':'Test group created successfully'}

   def _validate(self,data):
      assert 'testdata' in data.keys(),'testdata required' 
      assert type(data['testdata']) is dict,"Invalid payload. testdata should be valid json"
      testdata = data['testdata']
      assert 'name' in testdata.keys() and testdata['name']!='','testdata:name required'
      assert 'type' in testdata.keys()  and testdata['type']!='','testdata:type required'
      assert 'api' in testdata.keys()  and testdata['api']!='','testdata:api required'
      assert "validations" in data.keys(),'validations cannot be null'

      if testdata['type'] != 'GET':
         assert 'payload' in testdata.keys(),'testdata:payload cannot be null for the type POST'

   def addTest(self,requestdata,order=0): 
      self._validate(requestdata)

      testdata = requestdata['testdata']
      validations = requestdata['validations']

      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"

      #Tests
      data = readFile(self.testFile)

      tests = data['tests']

      assert testdata['name'] not in tests.keys(),"The test " + testdata['name'] +" is already exist"

      #Payload
      if testdata['type'] == 'POST':
         payload = testdata['payload']
         payloads = readFile(self.payloadFile)
         payloads[testdata['name']] = payload
         writeFile(self.payloadFile,json.dumps(payloads))

      #last order if not specified
      if order == 0:
         order = len(tests)+1

      tests[testdata['name']]={'name':testdata['name'],'api':testdata['api'],
         'order':order, 'type':testdata['type']}      
      
      data['tests'] = tests
      writeFile(self.testFile,json.dumps(data)) 

      #Validations
      data = readFile(self.validationFile)
      data[testdata['name']] = validations
      writeFile(self.validationFile,json.dumps(data))
      return {'status':'success','data':'Test info added successfully'}

   def delete(self):
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"
      data = readFile(sourceFile)
      del data[self.testname]
      writeFile(sourceFile,json.dumps(data))
      zipTest(self.dir,self.testname)      
      shutil.rmtree(self.dir)
      return {'status':'success','data':'Test removed'}

   def _removeTest(self,name):
       #delete Tests
      data = readFile(self.testFile)
      tests = data['tests']
      assert name in tests.keys(),"The test " + name +" is does not exist"

      test = tests[name]
      del tests[name]
      data['tests'] = tests
      writeFile(self.testFile,json.dumps(data)) 

      #delete payload
      if test['type'] == 'POST':
         payloads = readFile(self.payloadFile)
         del payloads[name]
         writeFile(self.payloadFile,json.dumps(payloads))

      #delete validations 
      data = readFile(self.validationFile)
      del data[name]
      writeFile(self.validationFile,json.dumps(data))

   def removeTest(self,requestdata):
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"

      testdata = requestdata['testdata']

      assert "name" in testdata.keys(),"testdata:name is required"
      self._removeTest(testdata['name'])
      return {'status':'success','data':'Test ' + testdata['name'] +' removed from test group ' + self.testname}

   def removeTests(self,requestdata):
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"
      testdata = requestdata['testdata']
      assert "names" in testdata.keys(),"testdata:name is required"
      for name in testdata['names']:
         self._removeTest(name)
      return {'status':'success','data':'Tests deleted successfully'}

   def getTestdata(self,testname):
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"
      testdata = readFile(self.testFile)['tests']
      payloads = readFile(self.payloadFile)
      validations = readFile(self.validationFile)

      assert testname in testdata.keys(),"Test " + testname +" not found in test group " + self.testname
      test = testdata[testname]

      #payload
      payload =''
      if test['type'] == 'POST':
         payload = payloads[testname]

      testInfo = {'name':test['name'],'payload':payload,'api':test['api'],
                  'order':test['order'], 'type':test['type'],
                  'tracks':test['tracks'],'validations':validations[testname]
                 }  

      return {'status':'success','data':testInfo}

   def getTests(self):
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"
      testdata = readFile(self.testFile)  
      return {'status':'success','data':testdata}

   def updateTestParts(self,requestdata):
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"
      assert 'testdata' in requestdata.keys(),"testdata is required"
      testdata = requestdata['testdata']
      assert 'name'  in testdata.keys(),"testdata:name is required"
      assert 'key' in testdata.keys(),"testdata:key is required"
      assert 'content' in testdata.keys(),"testdata:content is required"
      assert testdata['key'] in ['payload','validation'],"testdata:key can be payload or validations"
       
          
      if testdata['key'] == 'payload':
         payloads = readFile(self.payloadFile)
         assert testdata['name'] in payloads.keys(),"Payload of requested test is not available"
         payloads[testdata['name']]  = testdata['content']
         writeFile(self.payloadFile,json.dumps(payloads))
      else:
         validations = readFile(self.validationFile)
         assert testdata['name'] in validations.keys(),"Validations of requested test is not available"
         validations[ testdata['name']] = testdata['content']
         writeFile(self.validationFile,json.dumps(validations))

         #TODO update validation
      return {'status':'success','data':'Test ' + testdata['name'] +' updated successfully'}

   def updateTest(self,requestdata): 
      self._validate(requestdata)
      testdata = requestdata['testdata']
      assert os.path.exists(self.dir),"Test "+ self.testname +" is does not exist"

      #delete Tests
      data = readFile(self.testFile)
      tests = data['tests']
      assert testdata['name'] in tests.keys(),"The test " + testdata['name'] +" is does not exist"

      test = tests[testdata['name']]

      #TODO get data and add if update failed
      self.removeTest(requestdata) 
      self.addTest(requestdata,test['order'])
      return {'status':'success','data':'Test ' + testdata['name'] +' updated successfully'}

         


from Processor import Processor
from APIInvoker import APIInvoker

import json

objectTypeMapper ={
   str(dict):'object',
   str(list):'array',
   str(str):'string',
   str(unicode):'string',
   str(bool):'boolean',
   str(int):'number',
   str(type(None)):'null'
}

class TestGroupExecutor(object):
   def __init__(self,envData):
      self.executor = TestExecutionWatcher(envData)

   def executeTests(self,tests):
      testData  = tests['testData']['tests']
      payloads  = tests['payloads']
      validations = tests['validations']
      executionRespons = []
      testData = self._getAsOrdered(testData)
      orderedTestKeys = testData.keys()
      orderedTestKeys.sort()

      for key in orderedTestKeys: 
          item = testData[key] 
          testName = item['name']
          if item['type'] !='GET':
             item ['payload'] = payloads[testName]
          resp = self.executor.executeTest(item)
          resp = self.executor.validate(resp,validations[testName])
          executionRespons.append({testName:resp})
      return executionRespons

   def _getAsOrdered(self,testData):
       
       data = {}
       for key in testData.keys():
           item = testData[key]
           data [item['order']] = item
       return data

   def executeTestGroups(self,testGroups):
      resp = {}
      for key in testGroups.keys():
         executionResp = self.executeTests(testGroups[key])
         resp[key] = executionResp
      return resp

class TestGroupExecutorDemo(object):
   def __init__(self):
      pass
   def executeTest(self,testGroupName,testname,envData,response,validations):
      if testname== '':
          testname = 'Unnamed'
      #testData['order'] =1 #always 1 only for the demo execution
      #testData = {'testData':{'tests':{testname:testData}},'payloads':{testname:testData['payload']},'validations':{testname:validations}}
      executor = TestExecutionWatcher(envData)
      response = json.loads(response)
      executionResp = executor.validate(response,validations)
      return {testGroupName:[{testname:executionResp}]}

class TestExecutionWatcher(object):
   def __init__(self,envData,tracks={}): 
     #TODO input validations
     self.apiEndPoint = envData['apiEndPoint']
     self.headers = json.loads(envData['headers'])
     self.cookies = json.loads(envData['cookies'])
     self.tracks ={}
     self.processor = Processor()
     self.apiInvoker = APIInvoker(self.apiEndPoint )
     self.total = 0
     self.success = 0

   def executeTest(self,testData):
     self.apiInvoker.cookies = self.cookies
     self.apiInvoker.headers =self.headers
     #TODO input validations
     api = testData['api']
     method = testData['type']
     payload = ''
     if method != 'GET':
        payload = json.loads(testData['payload'])
        payload = self.processor.processPayload(payload,self.tracks)
     formattedAPI = self.processor .processURL(api,self.tracks)
     if method == 'GET':
        return self.apiInvoker.doGet(api)
     elif method == 'POST':
        return self.apiInvoker.doPost(api,payload)
     else:
        assert False, 'Invalid method ' + str(method)

   def _generateTestResponse(self,status,itemname,msg):
      return {'testStatus':status,'itemName':itemname,'validationResp':msg}

   def _validate(self,obtained,expected):
      self.total +=1
      msg = 'Expected %s and obtained %s' %(str(expected),str(obtained))
      status = 'Success' if str(expected) == str(obtained) else 'Fail'

      if  status == 'Success':
         self.success +=1

      return [msg,status]
     
   def validate(self,response,validationItem):
      validationResult = {}
      validationResps = []
      validationResult['name']=validationItem['name']
      successBeforExecution = self.success 
      totalBeforExecution = self.total
      respType = objectTypeMapper[str(type(response))]

      [msg,status] =self._validate(respType,validationItem['type']) 
      
      validationResps.append(self._generateTestResponse(status,validationItem['name'],msg))
      if status != 'Success':
         #TODO refactor to avoid repeated code block
         validationResult['validations'] =  validationResps

         success = self.success - successBeforExecution
         total = self.total - totalBeforExecution
         return {'validations':validationResult,'total':total,'success':success,'failed':(total-success)}

      if validationItem['type']=='object':
         if validationItem['validate']:
            if validationItem['validateSize']:
               [msg,status] =self._validate(len(response.keys()),validationItem['expectedSize'])    
               validationResps.append(self._generateTestResponse(status,validationItem['name'],msg))
         propertiesResp = []
         for item in validationItem['properties']:       
            if item['name'] not in response.keys(): 
               tempResp = {}
               self.total +=1 #Increase the total so that the failure will be added to the tops
               tempResp['validations'] =  [self._generateTestResponse('Fail',validationItem['name'],'Key %s not found in %s' %(item['name'],validationItem['name']))] 
               fullResp =  {'validations':tempResp,'total':1,'success':0,'failed':1}
               propertiesResp.append(fullResp)
            else:
               propertiesResp.append(self.validate(response[item['name']],item))
         validationResult['properties'] = propertiesResp

      elif validationItem['type']=='array':
         if validationItem['validate']:
            if validationItem['validateSize']:
               [msg,status] =self._validate(len(response),validationItem['expectedSize'])      
               validationResps.append(self._generateTestResponse(status,validationItem['name']+':Size',msg))
         propertiesResp = []
         propertyValidations = validationItem['properties']
         for item in response:
               propertiesResp.append(self.validate(item,propertyValidations[0]))    
         validationResult['properties'] = propertiesResp        
      else:
         if validationItem['validate'] and validationItem['validateExpectedValue']:
            [msg,status] =self._validate(response,validationItem['expectedValue'])     
            validationResps.append(self._generateTestResponse(status,validationItem['name'],msg))
         #track values
         if validationItem['trackValue'] :
            self.tracks[validationItem['trackName']] = response
         if validationItem['addToHeader'] :
            self.headers[validationItem['headerName']] = response
         if validationItem['addToCookie'] :
            self.cookies[validationItem['cookieName']] = response

      validationResult['validations'] =  validationResps

      success = self.success - successBeforExecution
      total = self.total - totalBeforExecution

      resp = {'validations':validationResult,'total':total,'success':success,'failed':(total-success)}
      return resp
     

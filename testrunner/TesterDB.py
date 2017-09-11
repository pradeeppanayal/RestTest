
import os
import json

from os.path import expanduser 

###########################
#                         #
# Author : Pradeep CH     #
# Date   : 23- Aug -2017  #
#                         #
###########################



sourcedirectory =  expanduser("~") + "/rtest/"

PAYLOAD_FILE = 'Payload.json'
TEST_FILE = 'Tests.json'
VALIDATION_FILE = 'Validations.json'

#Load the file from a directory
def loadFile(directory,fileName):
   fullPath  = directory + '/' + fileName
   assert os.path.exists(fullPath),'The file '+fileName+' does not eixist'
   with open(fullPath,'r') as f:
      data = f.read()
   return data

class TesterDB(object):
   def __init__(self):
      pass

   def loadTestGroup(self,testname):     
      assert testname and testname!='' ,'Testname cannot be null or empty'
      testdir  = sourcedirectory + testname        
      assert os.path.exists(testdir),'The test "'+self.testname+'" does not exists'
      tests = loadFile(testdir,TEST_FILE )
      validations = loadFile(testdir,VALIDATION_FILE  )
      payloads = loadFile(testdir,PAYLOAD_FILE )
      return {'testData':json.loads(tests),'payloads':json.loads(payloads),'validations':json.loads(validations)}

   def loadTestGroups(self,testnames):
      resp = {}
      for testname in testnames: 
          resp[testname] = self.loadTestGroup(testname)
      return resp


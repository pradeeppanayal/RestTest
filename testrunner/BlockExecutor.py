
###########################
#                         #
# Author : Pradeep CH     #
# Date   : 23- Aug -2017  #
#                         #
###########################

from TesterDB import TesterDB
from TestExecutor import TestGroupExecutor

def executeTestGroup(envData,testname): 
   db = TesterDB();
   tests = db.loadTestGroup(testname)
   executor = TestGroupExecutor(envData)
   return executor.executeTests(tests)

def executeTestGroups(envData,testnames): 
   db = TesterDB();
   testgroups = db.loadTestGroups(testnames)
   executor = TestGroupExecutor(envData)
   return executor.executeTestGroups(testgroups)

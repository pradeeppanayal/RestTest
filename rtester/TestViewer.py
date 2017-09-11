

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


def readFile(fname):
   assert os.path.exists(fname),"Test "+ fname +" not found"
   with open(fname,'r') as f:
      return json.loads(f.read())


PAYLOAD_FILE = 'Payload.json'
TEST_FILE = 'Tests.json'
VALIDATION_FILE = 'Validations.json'

class TestViewer(object):
   def getAll(self):
      data = readFile(sourceFile)
      return {'status':'success','data':data} 
       

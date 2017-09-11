#!/usr/bin/env python

###########################
#                         #
# Author : Pradeep CH     #
# Date  : 10- Aug -2017   #
#                         #
###########################

import os
import zipfile


import os
from os.path import expanduser 

sourcedirectory =  expanduser("~") + "/rtest/"
archiveFolder = sourcedirectory+'archive/'

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def zipTest(sourcePath,testname):
    zipf = zipfile.ZipFile(archiveFolder+testname+'.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(sourcePath, zipf)
    zipf.close()
    
if __name__ == '__main__':
    zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('tmp/', zipf)
    zipf.close()

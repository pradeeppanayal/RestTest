
import openpyxl
import os
from rtester import TestManager


class XLReader(object):
   def __init__(self,filename):
      self.filename = filename
   def readData(self):
      wb = openpyxl.load_workbook(self.filename)
      sheetNames = wb.get_sheet_names()
      sheet = wb.get_sheet_by_name(sheetNames[0]) 
      rows = list(sheet.rows)
      headers = self._readHeader(rows)
      response = []
      for i in range(1,len(rows)):
         response.append(self._loadData(rows[i],headers))
      return response

   def _loadData(self,row,headers):
      data = {}
      i = 0
      for col in row:
         data[headers[i]] = col.value
         i +=1
      return data

   def _readHeader(self,rows):
      first_row = rows[0]
      colHeaders = []
      for col in first_row:
         colHeaders.append(col.value)
      return colHeaders

class RXLImporter(object):
   def __init__(self,sourceFile,filename,testGroup):
      self.sourceFile =sourceFile
      self. filename = filename
      self. testGroup = testGroup
   def _packAsRequestdata(self,data):
      testdata = {}
      testdata['name'] = data['name']
      testdata['type'] = data['type']
      testdata['api'] = data['api']
      testdata['payload'] = data['payload']
      testdata["response"] = data["response"]
      return {'validations':[],"testdata":testdata}
   def importTests(self):
      path = os.path.join('/tmp/',self.filename)
      self.sourceFile.save(path)
      reader =XLReader(path)
      data = reader.readData()
      success = 0
      total = len(data)
      testGorupHandler =  TestManager(self. testGroup )
      errors = []
      for test in data:
         try:
            requestdata = self._packAsRequestdata(test)
            order = 0
            if test['order'] != '':
               order = int (test['order'])
            testGorupHandler.addTest(requestdata,order)
            success +=1            
         except Exception as e:
            errors.append(str(e))
      errMessage = ''
      if total > success:
         errMessage = '('+ ','.join(errors) +")"
      return {"status":"success","data":"Tests uploaded. Total : %d, Success : %d, Failed : %d %s" %(total,success,total-success,errMessage)}


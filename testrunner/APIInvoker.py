

###########################
#                         #
# Author : Pradeep CH     #
# Date  : 10- Aug -2017   #
#                         #
###########################


__author__='Pradeep CH'
__version__='1.0.0'

import json
import requests

class APIInvoker(object):

   def __init__(self,apiendPoint,accept = 'application/json',contentType='application/json',track=False):
      self.apiendPoint = apiendPoint
      self.cookies = {}
      self.headers = { 'Accept' :accept,
                       'Content-Type' : contentType }
      self.track = True#track
      
   @staticmethod
   def invoke(data):
      assert data,"Invalid request payload"
      assert 'apiendpoint' in data.keys() and data['apiendpoint']!='','apiendpoint is required'
      assert 'api' in data.keys() and data['api']!='','api is required'
      assert 'type' in data.keys() and data['type']!='' ,'type is required'
      assert 'cookies' in data.keys() and data['cookies']!='' ,'cookies  required'
      assert 'headers' in data.keys() and data['headers']!='' ,'headers required'

      invoker = APIInvoker(data['apiendpoint']) 
      invoker.headers = json.loads( data['headers'])
      invoker.cookies = json.loads( data['cookies'])

      if data['type'] != 'GET':
         assert 'payload' in data.keys(),'payload is required'
         return {'status':'success','data':invoker.doPost(data['api'],data['payload'])}
      return {'status':'success','data':invoker.doGet(data['api'])}

   def doPost(self,api,data):
      url = self.apiendPoint + api
      if self.track:
          print 'POST:::%s' %url
          print "Payload:::%s" %str(data)

      if type(data) == dict or type(data) == list:
         data = json.dumps(data)
      response = requests.post(url,data=data,headers=self.headers,verify=False,cookies=self.cookies) 
      response.raise_for_status()
      responseJson = response.json()
      if self.track:
          print 'Response:::%s' %str(responseJson)
      return responseJson

   def doGet(self,api):
      url = self.apiendPoint + api      
      if self.track:
          print 'GET:::%s' %url

      response = requests.get(url,headers=self.headers,verify=False,cookies=self.cookies) 
      response.raise_for_status()
      responseJson = response.json()
      if self.track:
          print 'Response:::%s' %str(responseJson)
      return responseJson
if __name__ =='__main__':
   data = {}
   #a = APIInvoker.invoke()

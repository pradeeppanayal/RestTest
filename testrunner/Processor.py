

###########################
#                         #
# Author : Pradeep CH     #
# Date  : 10- Aug -2017   #
#                         #
###########################

import re

class Processor(object):

   def processURL(self,url,tracks):
      if 'track:' not in url:
         return url
      #TODO process url
      tracks = re.findall('track:.*?(?=&|$)',url) 
      for track in tracks:
         if track=='':
            continue
         trackKey = track.split(':')[1]
         assert trackKey in tracks,'The key "%s" not found in tracks' %trackKey
         url = url.replace(track, self.tracks[trackKey])
      return url 

   def processPayload(self,payload,tracks): 
      if type(payload) is dict: 
         for key in payload.keys(): 
            val = payload[key] 
            if type(val) is unicode : 
               if val.startswith('track:'):
                  trackKey = val.split(':')[1] 
                  assert trackKey in tracks,"The track '"+ trackKey+"' not found "
                  payload[key] = tracks[trackKey]

            elif type(val) in [dict,list]:
                payload[key] = self.processPayload(payload[key],tracks)
      elif type(payload) is list:
         for i in range(len(payload)):
            payload[i] =  self. processPayload(payload[i],tracks)
      return payload                  
          

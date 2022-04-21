#!/usr/bin/python
# Script check if cluster is balanaced or not. 
# Calculate number of Active Vbuckets and Vbucket Replicas for each cluster bucket and return an error if verification is not matched with valid number

from __future__ import print_function
import requests
import json
import sys
import time

sumActiveVbucket=0
sumReplicaVbucket=0
i=0

def cb_cluster_info():
 try:
   url = "http://" + sys.argv[1] + ":8091/pools/default/"
   cluster = json.loads(requests.get(url, auth=(sys.argv[2],sys.argv[3])).text)
 except Exception as err:
   print("Error: retrieve cluster information ", sys.exc_info())
   sys.exit(2)
 return cluster


cluster = cb_cluster_info()

while not cluster['balanced'] and i < 2:
   print (cluster['balanced'])
   time.sleep(5)
   cluster=cb_cluster_info()
   i += 1

if not cluster['balanced']:
  print("Cluster is not balanced!", cluster['clusterName'])
  sys.exit(2)

try:
  url = "http://" + sys.argv[1] + ":8091/pools/default/buckets"
  my_bucket = json.loads(requests.get(url, auth=(sys.argv[2],sys.argv[3])).text)
except Exception as err:
  print("Error: retrieve buckets list", sys.exc_info())
  sys.exit(2)

for mbkt in my_bucket:

  sumActiveVbucket=0
  sumReplicaVbucket=0

  for clu in cluster['nodes']:

     if 'kv' in clu['services']:
       url="http://" + clu['hostname'] + "/pools/default/buckets/" + mbkt['name'] + "/nodes/" + clu['hostname'] + "/stats"
       try:
         BucketStat = json.loads(requests.get(url, auth=(sys.argv[2],sys.argv[3])).text)     
       except Exception as err:
         print("Error: retrieve Vbucket detailed statistics  ", sys.exc_info())
         sys.exit(2)     

       lastActiveItem=len(BucketStat['op']['samples']['vb_active_num'])
       lastReplicaItem=len(BucketStat['op']['samples']['vb_replica_num']) 
       sumActiveVbucket=sumActiveVbucket + BucketStat['op']['samples']['vb_active_num'][lastActiveItem-1]
       sumReplicaVbucket=int(sumReplicaVbucket) + int(BucketStat['op']['samples']['vb_replica_num'][lastReplicaItem-1])

  if sumActiveVbucket < 1024:
    print("Wrong Active Vbucket number " +  mbkt['name'] + ": " , sumActiveVbucket)
    sys.exit(2)
  if sumReplicaVbucket < 1024*mbkt['replicaNumber']:
    print("Wrong Replica Vbucket number " +  mbkt['name'] + ": ", sumReplicaVbucket)     
    sys.exit(2)   

print(0)

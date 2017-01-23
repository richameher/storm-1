%matplotlib inline
from operator import itemgetter
import matplotlib.pyplot as pt
import math
import numpy as np
import random

mean=[]

f=open("/Users/richam112/Desktop/test_log_delay.rtf")

bolt_filter=[]
i=0
bolt_aggregate=[]
j=0
bolt_transform=[]
k=0
bolt_filter_2=[]
l=0
bolt_join=[]
m=0
bolt_output_sink=[]
n=0

for line in f:
    if "RecvQDelay" in line:
        latencies=line.rstrip("\\\n").split(" ")
        if latencies[-1]=="bolt_filter":
            bolt_filter.append([])
            bolt_filter[i].append(latencies[-5])
            bolt_filter[i].append(latencies[-4])
            i=i+1
        if latencies[-1]=="bolt_aggregate":
            bolt_aggregate.append([])
            bolt_aggregate[j].append(latencies[-5])
            bolt_aggregate[j].append(latencies[-4])
            j=j+1
        if latencies[-1]=="bolt_transform":
            bolt_transform.append([])
            bolt_transform[k].append(latencies[-5])
            bolt_transform[k].append(latencies[-4])
            k=k+1
        if latencies[-1]=="bolt_filter_2":
            bolt_filter_2.append([])
            bolt_filter_2[l].append(latencies[-5])
            bolt_filter_2[l].append(latencies[-4])
            l=l+1
        if latencies[-1]=="bolt_join":
            bolt_join.append([])
            bolt_join[m].append(latencies[-5])
            bolt_join[m].append(latencies[-4])
            m=m+1
        if latencies[-1]=="bolt_output_sink":
            bolt_output_sink.append([])
            bolt_output_sink[n].append(latencies[-5])
            bolt_output_sink[n].append(latencies[-4])
            n=n+1


aggre=[]
aggre.append([])
prev_timestamp=bolt_filter[0][1]
aggre[0].append(bolt_filter[0][0])
aggre[0].append(1)
aggre[0].append(prev_timestamp)
k=0

for i in range(1,len(bolt_filter),1):
    if bolt_filter[i][1]==prev_timestamp:
        aggre[k][1]=aggre[k][1]+1  # keeps a count of the number of tuples
        aggre[k][0]=float(aggre[k][0])+float(bolt_filter[i][0]) #find the avg
    else:
        aggre[k][0]=float(aggre[k][0])/float(aggre[k][1])
        aggre.append([])
        k=k+1
        prev_timestamp=bolt_filter[i][1]
        aggre[k].append(bolt_filter[i][0])
        aggre[k].append(1)
        aggre[k].append(prev_timestamp)

#repeat for all bolts

print(aggre)

x=[i[2] for i in aggre]
y=[i[0] for i in aggre]


fig, ax = pt.subplots()
ax.scatter(x,y,edgecolors="blue", marker =">")

# print(prev_timestamp)
# t(bolt_filter[0][0])

%matplotlib inline
from operator import itemgetter
import matplotlib.pyplot as pt
import math
import numpy as np
import random

mean=[]

f=open("/Users/richam112/Desktop/gdu3/Experiment_2/delayL1.txt")

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
first=0
batch_time=100
start_time=1485314610226
end_time=1485318159598
time=[]

for line in f:
    if "RecvQDelay" in line:
        latencies=line.rstrip("\\\n").split(" ")
        time.append(latencies[-4])
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
#         if latencies[-1]=="bolt_filter_2":
#             bolt_filter_2.append([])
#             bolt_filter_2[l].append(latencies[-5])
#             bolt_filter_2[l].append(latencies[-4])
#             l=l+1
#         if latencies[-1]=="bolt_join":
#             bolt_join.append([])
#             bolt_join[m].append(latencies[-5])
#             bolt_join[m].append(latencies[-4])
#             m=m+1
#         if latencies[-1]=="bolt_output_sink":
#             bolt_output_sink.append([])
#             bolt_output_sink[n].append(latencies[-5])
#             bolt_output_sink[n].append(latencies[-4])
#             n=n+1
# print(bolt_aggregate)
#need to convert timestamp into ms

bolt_transform=sorted(bolt_transform,key=itemgetter(1), reverse=False)
bolt_aggregate=sorted(bolt_aggregate,key=itemgetter(1), reverse=False)
bolt_filter=sorted(bolt_filter,key=itemgetter(1), reverse=False)
time=sorted(time,key=itemgetter(1), reverse=False)
# bolt_filter_2=sorted(bolt_filter_2,key=itemgetter(1), reverse=False)
# bolt_join=sorted(bolt_join,key=itemgetter(1), reverse=False)
# bolt_output_sink=sorted(bolt_output_sink,key=itemgetter(1), reverse=False)

print("Start-time",start_time)
# all_timestamps=np.linspace(start_time,end_time,num=(end_time-start_time))
aggre=[]
aggre.append([])
prev_timestamp=int(bolt_aggregate[0][1])
aggre[0].append(bolt_aggregate[0][0])
aggre[0].append(1)
aggre[0].append(prev_timestamp)
k=0
count=0
for i in range(1,len(bolt_aggregate),1):
    if float(bolt_aggregate[i][1])-prev_timestamp<=batch_time:
        aggre[k][1]=aggre[k][1]+1  # keeps a count of the number of tuples
        aggre[k][0]=float(aggre[k][0])+float(bolt_aggregate[i][0])#find the avg
        if i==(len(bolt_aggregate)-1):
            aggre[k][0]=float(aggre[k][0])/float(aggre[k][1]) #avg queue delay
            aggre[k][2]=int((int(bolt_aggregate[i-1][1])+prev_timestamp)/2)
            aggre[k].append(float(aggre[k][1])*float(aggre[k][0]))
    else:
        aggre[k][0]=float(aggre[k][0])/float(aggre[k][1])
        aggre[k][2]=int((int(bolt_aggregate[i-1][1])+prev_timestamp)/2)
        if aggre[k][0]>0:
            aggre[k].append(float(aggre[k][1])/float(aggre[k][0])) # no_of_tuples/avg_delay
        else:
            aggre[k].append(0)
        if i<(len(bolt_aggregate)-1):
            aggre.append([])
            k=k+1
            prev_timestamp=int(bolt_aggregate[i][1])
            aggre[k].append(bolt_aggregate[i][0])
            aggre[k].append(1)
            aggre[k].append(prev_timestamp)

#repeat for all bolts
aggre=[x for x in aggre if x!=[]]

time_aggre=aggre[0][2]

val = start_time
for i in range(0, len(aggre)):
    aggre[i][2] = (aggre[i][2] - val)/1000

end_time=(end_time-start_time)/1000
start_time=0


x=[i[2] for i in aggre]
y=[i[0] for i in aggre]
z=[i[3] for i in aggre] # removal



fig,ax= pt.subplots()
# ax.scatter(x,y,edgecolors="green",label="L1 Avg queue_removal rate", marker ="*")
ax.scatter(x,w,edgecolors="red",label="Avg removal rate", marker ="*")
ax.set_xlim(start_time,end_time)
# ax.set_ylim(0,1000)
ax.set_xlabel('s')
ax.set_ylabel('Avg queue removal rate')
ax.vlines(x=(1485317146688-1485314610226)/1000, ymax=50000 , ymin=0,  colors='black',label="rebalance")
ax.vlines(x=(1485317146700-1485314610226)/1000, ymax=50000 , ymin=0,  colors='black')
ax.set_title("Avg queue removal rate bolt_aggregate")
pt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2,prop={'size':10})
# plt.savefig("outputsimpletuples"+'.png', bbox_inches='tight')
pt.savefig("P62 Queue_Removal rate"+'.png', bbox_inches='tight')

fig,ax= pt.subplots()
# ax.scatter(x,w,edgecolors="green",label="Avg queue_delay", marker ="*")
ax.scatter(x,z,edgecolors="red",label="L1 Avg queue_delay", marker ="*")
ax.set_xlim(start_time,end_time)
ax.set_xlabel('s')
ax.set_ylabel('Avg queue delay per 100ms')
ax.vlines(x=(1485317146688-1485314610226)/1000, ymax=30 , ymin=0,  colors='black',label="rebalance")
ax.vlines(x=(1485317146700-1485314610226)/1000, ymax=30 , ymin=0,  colors='black')
ax.set_title("Avg queue delay bolt_aggregate")
# ax.legend
pt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2,prop={'size':10})
pt.savefig("P62 Queue delay"+'.png', bbox_inches='tight')

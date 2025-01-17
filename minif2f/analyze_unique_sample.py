import json
collect_file='collects/report_2025-01-15_20-11-30.txt'
with open(collect_file,'r') as f:
    js=json.load(f)

print('sample number: %s'%len(js))
dt={}
for j in js:
    sb=j['state_before']
    sa=j['state_after']
    if sb==sa:
        print(sa)
    if sb not in dt.keys():
        dt[sb]=1
    else:
        dt[sb]+=1
v=dt.values()
import matplotlib.pyplot as plt

hs=plt.hist(v)
print(hs)
plt.show()
print(dt)

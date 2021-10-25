import requests
import time
import os
now = time.time()
for i in range(1,365):
    goal = now - 86400*i
    time_str = time.strftime("%Y%m%d",time.localtime(goal))
    if os.path.exists("./pub_apnic_static_apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str)):
        print('{0} is already downloaed, skip.'.format(time_str))
        continue
    file_url = "http://ftp.apnic.net/apnic/stats/apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str)
    r = requests.get(file_url) 
    print('dowloading {0}'.format(file_url))
    with open("./pub_apnic_static_apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str),'wb') as f:
        f.write(r.content)
        print('save to '+"./pub_apnic_static_apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str))
import requests
import time
now = time.time()
for i in range(10,20):
    goal = now - 86400*i
    time_str = time.strftime("%Y%m%d",time.localtime(goal))
    file_url = "http://ftp.apnic.net/apnic/stats/apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str)
    r = requests.get(file_url) 
    print('dowloading {0}'.format(file_url))
    with open("./pub_apnic_statc_apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str),'wb') as f:
        f.write(r.content)
        print('save to '+"./pub_apnic_statc_apnic/{0}/delegated-apnic-{1}.gz".format(time_str[:4],time_str))
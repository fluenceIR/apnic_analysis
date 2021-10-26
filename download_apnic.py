import requests
import time
import os
import logging

class DOWNLOAD_APNIC(object):
    def __init__(self):
        pass
    def work(self,begin_date,end_date):
        now = time.time()
        for i in range(begin_date,end_date):
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

if __name__=='__main__':
    a = DOWNLOAD_APNIC()
    a.work(1,365)
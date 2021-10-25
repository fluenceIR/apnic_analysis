import os
import time
from IPV4_DATABASE import IPV4_DATABASE
import math

class apnic_database(object):
    def __init__(self):
        self.sonNic={}
    def preload(self, fp):
        fh = open(fp)
        file_boxs = {}
        # step1: read the file
        while True:
            ip = fh.readline()
            if ip:
                if '#' in ip:
                    continue
                line_box = ip.strip().split('|')
                if 'ipv4' not in line_box:
                    continue
                if 'summary' in line_box:
                    continue
                print(ip)
                print(line_box)
                if line_box[1] not in self.sonNic.keys():
                    self.sonNic[line_box[1]]=IPV4_DATABASE(line_box[1])
                    if not os.path.exists('./countries/{0}'.format(line_box[1])):
                        os.mkdir('./countries/{0}'.format(line_box[1]))
                    file_boxs[line_box[1]]=open('./countries/{0}/{0}_{1}'.format(line_box[1],date_str),'w',encoding='utf-8')
                    file_boxs[line_box[1]].write('# create at %{0} \n'.format(time.strftime('%Y/%m/%d %X',time.localtime())))
                file_boxs[line_box[1]].write(line_box[3]+'/'+str(int(math.log(int(line_box[4]),2)))+'\n')
            else:
                break
        for key in file_boxs:
            file_boxs[key].close()


for i in range(1,10):
    now = time.time()
    goal = now - 86400*i
    date_str = time.strftime("%Y%m%d",time.localtime(goal))
    filename = 'delegated-apnic-{0}'.format(date_str)
    extrac_cmd = "7z x ./pub_apnic_statc_apnic/{0}/delegated-apnic-{1}.gz".format(date_str[:4],date_str)
    os.popen(extrac_cmd)
    time.sleep(2)
    a = apnic_database()
    a.preload("./delegated-apnic-{1}".format(date_str[:4],date_str))
    os.remove(filename)
    
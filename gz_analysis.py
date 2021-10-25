import os
import time
import logging
from IPV4_DATABASE import IPV4_DATABASE
import math

class apnic_database(object):
    def __init__(self):
        self.sonNic={}
        self.analysis_box={}
    def preload(self, fp, country=None):
        # decompression from gz file to ./countries/[CN]/[CN]_20210101
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
                # line_box example:['apnic', 'AU', 'ipv4', '1.0.0.0', '256', '20110811', 'assigned']
                if country != None and line_box[1] not in country:
                    continue
                if line_box[1] not in self.sonNic.keys():
                    self.sonNic[line_box[1]]=IPV4_DATABASE(line_box[1])
                    if not os.path.exists('./countries/{0}'.format(line_box[1])):
                        os.mkdir('./countries/{0}'.format(line_box[1]))
                    file_boxs[line_box[1]]=open('./countries/{0}/{0}_{1}'.format(line_box[1],date_str),'w',encoding='utf-8')
                    file_boxs[line_box[1]].write('# create at %{0} \n'.format(time.strftime('%Y/%m/%d %X',time.localtime())))
                file_boxs[line_box[1]].write(line_box[3]+'/'+str(32-int(math.log(int(line_box[4]),2)))+'\n')
            else:
                break
        for key in file_boxs:
            file_boxs[key].close()
    def analysis(self,country,begin_time,end_time):
        # create the self.analysis_box:list and self.total:IPV4_DATABASE
        now = time.time()
        self.analysis_box.clear()
        self.total=IPV4_DATABASE('total')
        for i in range(begin_time,end_time):
            goal = now - 86400*i
            date_str = time.strftime("%Y%m%d",time.localtime(goal))
            filepath='./countries/{0}/{0}_{1}'.format(country,date_str)
            print('loading {0}'.format(filepath))
            assert os.path.exists(filepath)
            self.analysis_box['{0}_{1}'.format(country,date_str)]=IPV4_DATABASE('{0}_{1}'.format(country,date_str))
            with open(filepath) as file:
                self.analysis_box['{0}_{1}'.format(country,date_str)].loads(file)
            self.total = self.total + self.analysis_box['{0}_{1}'.format(country,date_str)]
            self.total.name='total'
        

if __name__=='__main__':
    for i in range(1,365):
        now = time.time()
        goal = now - 86400*i
        date_str = time.strftime("%Y%m%d",time.localtime(goal))
        filename = 'delegated-apnic-{0}'.format(date_str)
        extrac_cmd = "7z x ./pub_apnic_static_apnic/{0}/delegated-apnic-{1}.gz".format(date_str[:4],date_str)
        os.popen(extrac_cmd)
        time.sleep(2)
        a = apnic_database()
        a.preload("./delegated-apnic-{1}".format(date_str[:4],date_str),['CN','HK','TW'])
        os.remove(filename)

if __name__=='__main__2':
    a = apnic_database()
    a.analysis('CN',1,365)
now = time.time()
goal1=now - 86400*1
goal2 = goal1 - 86400*365
date_str1 = time.strftime("%Y%m%d",time.localtime(goal1))
date_str2 = time.strftime("%Y%m%d",time.localtime(goal2))
file = open('./report.txt','w',encoding='utf-8')
file.write('analysis of CN from {0} to {0}\n\n'.format(date_str1,date_str2))
diff_total=0
for i in range(1,364):
    goal1=now - 86400*i
    goal2 = goal1 - 86400
    date_str1 = time.strftime("%Y%m%d",time.localtime(goal1))
    date_str2 = time.strftime("%Y%m%d",time.localtime(goal2))
    if a.analysis_box['CN_{0}'.format(date_str1)]==a.analysis_box['CN_{0}'.format(date_str2)]:
        print('CN_{0} is equal CN_{1}'.format(date_str1,date_str2))
    else:
        after = a.analysis_box['CN_'+date_str1]
        before = a.analysis_box['CN_'+date_str2]
        file.write('CN_'+date_str1 +' diff from CN_' + date_str2+':\n')
        temp = before -after
        diff_total+=temp.ip_totals
        for ip in temp.ipgroup:
            file.write('  - '+ip.strFullsize()+'\n')
        temp = after -before
        diff_total+=temp.ip_totals
        for ip in temp.ipgroup:
            file.write('  + '+ip.strFullsize()+'\n')
        print('----CN_{0} is not equal CN_{1}'.format(date_str1,date_str2))
    file.write('\nsummary:\nthe total diff ip is {0}, total ip is {1}, occupies {2:.8%}'.format(diff_total,a.total.ip_totals,diff_total/a.total.ip_totals))
file.close()
        

        
        
        
        
        
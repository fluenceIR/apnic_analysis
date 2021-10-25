##################################################
# author: Xu Penghao
# date: 2021/10/19 first create
#       2021/10/20 space pattern update
# MD5: C19D5D566CC39DEEFA24800C298398D4
##################################################
import math
import time
import re
import IPy

class IPV4_DATABASE(object):
    @staticmethod
    def begin_ip(ip):
        assert isinstance(ip, IPy.IP)
        return ip.int()
    @staticmethod
    def end_ip(ip):
        assert isinstance(ip, IPy.IP)
        return ip.int()+((2**32)>>(ip.prefixlen()))-1
    @staticmethod
    def num2str(num,mode=1):
        # mode = 0 loosely align but stort
        # mode = 1 strictly align but long
        if mode==0:
            return "{0}.{1}.{2}.{3}".format(num// (2 ** 24),num% (2 ** 24) // (2 ** 16),\
            num% (2 ** 16) // (2 ** 8),num% (2 ** 8))
        if mode == 1:
            return "{0:3d}.{1:3d}.{2:3d}.{3:3d}".format(num// (2 ** 24),\
            num% (2 ** 24) // (2 ** 16),num% (2 ** 16) // (2 ** 8),num% (2 ** 8))
    @staticmethod
    def height(num):
        height = 0
        while num%2==0 and height<32:
            height+=1
            num//=2
        return height
    @staticmethod
    def nums2IPs(num1,num2):
        assert num2>num1
        IPs=[]
        while num1<num2:
            k_length = int(math.log(num2-num1,2))
            h_num1 = IPV4_DATABASE.height(num1)
            span = min(k_length,h_num1)
            IPs.append(IPy.IP(IPV4_DATABASE.num2str(num1)+'/'+str(32-span)))
            num1 = num1 + (1<<span)
        return IPs
    @staticmethod
    def set_byte(byte,index,val):
        if val ==1:
            return byte | (1 << index)
        else:
            return byte & ~(1 << index)
    @staticmethod
    def planeneedling(obj1,obj2):
        result = []
        # the a in result means num, up/down, obj1/obj2
        result.extend([[a[0],1,a[1]] for a in obj1])
        result.extend([[a[0],0,a[1]] for a in obj2])
        result.sort(key=lambda a:4*a[0]+2*a[1]+a[2])
        # d:print('result:\n',result[:20])
        result2 = [[-1,0]]
        for i in range(result.__len__()):
            if result[i][0]>result2[-1][0]:
                result2.append([result[i][0],result2[-1][1]])
            elif result[i][0]==result2[-1][0]:
                pass
            else:
                raise RuntimeError('in planeneedling')
            result2[-1][1] = IPV4_DATABASE.set_byte(result2[-1][1],index = result[i][1],val=result[i][2])
        # d:print('result2:\n',result2[:20])
        def check(result):
            flag = True
            for i in range(result.__len__()-1):
                if result[i][1]==result[i+1][1]:
                    flag = False
                    break
            return True
        assert check(result2)
        return result2
    def __init__(self,name):
        # a in space,a[0]:int mean the number, a[1]:bool ,True means from down to up, False means from up to down
        # Section left closed right open
        self.space=[[-1,0]]
        self.ipgroup = []
        self.name = name
        self._ip_totals = 0
    @property
    def ip_totals(self):
        return self._ip_totals
    def loads(self,fh):
        # step1: read the file
        while True:
            ip = fh.readline()
            if ip:
                if '#' in ip:
                    continue
                self.ipgroup.append(IPy.IP(ip))
            else:
                break
        # step2: sort the ipgroup
        self.ipgroup.sort(key=lambda x:int(x.strDec()))
        # step3: generate the space
        for ip in self.ipgroup:
            self.space.append([self.begin_ip(ip),1])
            self.space.append([self.end_ip(ip)+1,0])
        # step4: loosely check the space
        self._distribute_check(mode = 0)
        # step5: optimize the space
        flag = 1
        while flag<self.space.__len__():
            if self.space[flag][0]>self.space[flag-1][0]:
                flag+=1
            elif self.space[flag][0]==self.space[flag-1][0]:
                assert self.space[flag][1]!= self.space[flag-1][1]
                self.space.pop(flag)
                self.space.pop(flag-1)
                flag-=1
        # step6: strictly check the space
        self._distribute_check()
    def _distribute_check(self,mode =1):
        # if don't overlay, means distribute well,return True, otherwise return False
        # 1.范围内，2.有序，3.不重叠，4.不连续
        # mode =1 严格递增， mode= 0 不严格递增
        if mode ==1:
            try:
                for i in range(self.space.__len__()-1):
                    assert self.space[i][0]<self.space[i+1][0]
                    assert self.space[i][1] != self.space[i+1][1]
            except:
                return False
            else:
                return True
        if mode ==0:
            try:
                for i in range(self.space.__len__()-1):
                    assert self.space[i][0]<=self.space[i+1][0]
                    assert self.space[i][1] != self.space[i+1][1]
            except:
                return False
            else:
                return True
    def dumps(self,fh,mode=1):
        # mode=1 save like a.b.c.d/e
        # mode=2 save like a.b.c.d-e.f.g.h
        fh.write("# "+time.strftime("%Y/%m/%d %X",time.localtime())+'\n')
        fh.write("# "+self.name+'\n')
        # self.group_update()
        if mode==1:
            for ip in self.ipgroup:
                fh.write(ip.strFullsize()+'\n')
        if mode ==2:
            for ip in self.ipgroup:
                fh.write(ip.strDec()+'-'+self.num2str(ip.int()+(1<<(32-ip.prefixlen())))+'\n')
    def report(self):
        print('-' * 50)
        print('一共有{0}个条目在{1}中'.format((self.space.__len__()-1)/2, self.name))
        num = 0
        for i in range((self.space.__len__()-1)//2):
            num += (self.space[2*i+2][0] - self.space[2*i+1][0])
        print('共覆盖{}个IP地址，占全部IPv4地址池的{:.4%}'.format(num, num / (2 ** 32)))
        self._ip_totals = num
        for i in range((self.space.__len__()-1)//2):
            print('{0:4d}: {1}--{2}'.format(i, self.num2str(self.space[2*i+1][0]),self.num2str(self.space[2*i+2][0])))
    def judge(self, ip):
        result = []
        ip_num = IPy.IP(ip).int()
        for net in self.space:
            result.append(net[0]<=ip_num and ip_num <= net[1])
        if True in result:
            return True
        else:
            return False
    def group_update(self):
        self.ipgroup.clear()
        for i in range(self.space.__len__()):
            if self.space[i][1]==1:
                self.ipgroup.extend(self.nums2IPs(self.space[i][0],self.space[i+1][0]))
    def __add__(self, other):
        # step1: assert check
        assert isinstance(other, IPV4_DATABASE)
        assert self._distribute_check()
        assert other._distribute_check()
        # step2: init the result
        result = IPV4_DATABASE('(sub of ' + self.name + ' ' + other.name+')')
        result.space.pop()
        # step3: generate the auxiliary group
        advance_list = IPV4_DATABASE.planeneedling(self.space,other.space)
        # step4: generate the result
        for i in range(advance_list.__len__()):
            if advance_list[i][1] == 0:
                result.space.append([advance_list[i][0],0])
            else:
                if result.space[-1][1]==0:
                    result.space.append([advance_list[i][0],1])
                else:
                    pass
        result.group_update()
        return result
    def __mul__(self, other):
        # step1: assert check
        assert isinstance(other, IPV4_DATABASE)
        assert self._distribute_check()
        assert other._distribute_check()
        # step2: init the result
        result = IPV4_DATABASE('(sub of ' + self.name + ' ' + other.name+')')
        result.space.pop()
        # step3: generate the auxiliary group
        advance_list = IPV4_DATABASE.planeneedling(self.space,other.space)
        # step4: generate the result
        for i in range(advance_list.__len__()):
            if advance_list[i][1] == 3:
                result.space.append([advance_list[i][0],1])
            else:
                if result.space[-1][1]==1:
                    result.space.append([advance_list[i][0],0])
                else:
                    pass
        result.group_update()
        return result
    def __sub__(self, other):
        # step1: assert check
        assert isinstance(other, IPV4_DATABASE)
        assert self._distribute_check()
        assert other._distribute_check()
        # step2: init the result
        result = IPV4_DATABASE('(sub of ' + self.name + ' ' + other.name+')')
        result.space.pop()
        # step3: generate the auxiliary group
        advance_list = IPV4_DATABASE.planeneedling(self.space,other.space)
        # step4: generate the result
        for i in range(advance_list.__len__()):
            if advance_list[i][1] == 2:
                result.space.append([advance_list[i][0],1])
            else:
                if result.space[-1][1]==1:
                    result.space.append([advance_list[i][0],0])
                else:
                    pass
        result.group_update()
        return result
    def __eq__(self,other):
        assert isinstance(other, IPV4_DATABASE)
        assert self._distribute_check()
        assert other._distribute_check()
        if self.space.__len__()!=other.space.__len__():
            return False
        for i in range(self.space.__len__()):
            if self.space[i]!=other.space[i]:
                return False
        return True
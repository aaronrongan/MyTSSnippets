import urllib.request
import re
import os
#来源
#知乎
# https://www.zhihu.com/question/29979949/answer/49553763

f=open('stock_num.txt')
stock = []
for line in f.readlines():
    #print(line,end = '')
    line = line.replace('\n','')
    stock.append(line)
#print(stock)
f.close()
#print(stock)

for each in stock:
    url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'+each+'/page_type/ndbg.phtml'
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    page = urllib.request.urlopen(req)
    try:
        html = page.read().decode('gbk')
        target = r'&id=[_0-9_]{6}'
        target_list = re.findall(target,html)
        os.mkdir('./'+each)
        sid = each
        #print(target_list)
        for each in target_list:
            #print(a)
            #print(each)
            target_url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid='+sid+each
            #print(target_url)
            treq = urllib.request.Request(target_url)
            treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
            tpage = urllib.request.urlopen(treq)
            try:
                thtml = tpage.read().decode('gbk')
                #print(thtml)
                file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml)
                try:
                    #print(file_url.group(0))
                    local = './'+sid+'/'+file_url.group(0).split("/")[-1]+'.pdf'
                    #调试用作文件占位
                    #open(local, 'wb').write(b'success')
                    #print(local)
                    urllib.request.urlretrieve(file_url.group(0),local,None)
                except:
                    print('PDF失效;'+target_url)
            except:
                print('年报下载页面编码错误;'+target_url)
    except:
        print('年报列表页面编码错误;'+url)
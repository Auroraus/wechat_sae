# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os,re
import urllib2,urllib
from lxml import etree
from HTMLParser import HTMLParser
import sys
import math
reload(sys)
sys.setdefaultencoding('utf8')

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="zhangfan" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        
    def POST(self):  
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType=='text':
            if content==u'张凡':
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'是一个大帅哥(：')
            elif content==u'实用网站':
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"http://1095f1f.nat123.cc:10834/myblog/info1.html")
            elif content==u'个人博客':
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"http://1095f1f.nat123.cc:10834/myblog/index.html")
            elif content[:2]==u'电影':
                if len(content)>=4:
                    flist=content.split(' ')
                    return self.render.reply_text(fromUser,toUser,int(time.time()),self._film(flist[1]))
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'歌曲':
                if len(content)>=20:
                    slist=content.split(' ')
                    return self.render.reply_text(fromUser,toUser,int(time.time()),self._song(slist[-1]))
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content==u'帮助':
                return self.render.reply_text(fromUser,toUser,int(time.time()),'https://github.com/hfutzf/wechat_sae/blob/master/index.py')
            elif content==u'test':
                r = urllib2.urlopen('http://1095f1f.nat123.cc:10834/myblog/test.txt').read()
                return self.render.reply_text(fromUser,toUser,int(time.time()),r)
            elif content[:2]==u'维基':
                if len(content)>=4:
                    weiji=content[3:]
                    if re.compile('[a-z]').findall(weiji):
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'https://en.wikipedia.org/wiki/'+weiji)
                    else:
                        weiji=self._trans(weiji,fr='zh',to='en').replace(' ','').replace(',','')
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'https://en.wikipedia.org/wiki/'+weiji)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'百科':
                if len(content)>=4:
                    weiji=content[3:]
                    ask = weiji.encode('UTF-8')
                    enask = urllib2.quote(ask)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'https://baike.baidu.com/item/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'知乎':
                if len(content)>=4:
                    weiji=content[3:]
                    ask = weiji.encode('UTF-8')
                    enask = urllib2.quote(ask)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'https://www.zhihu.com/search?type=content&q='+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:5]==u'quora':
                if len(content)>=7:
                    weiji=content[6:]
                    if re.compile('[a-z]').findall(weiji):
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'https://www.quora.com/search?q='+weiji)
                    else:
                        weiji=self._trans(weiji,fr='zh',to='en').replace(' ','').replace(',','')
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'https://www.quora.com/search?q='+weiji)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'海词':
                if len(content)>=4:
                    weiji=content[3:]
                    if re.compile('[a-z]').findall(weiji):
                        	return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.cn/'+weiji)
                    else:
                        ask = weiji.encode('UTF-8')
                        enask = urllib2.quote(ask)
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.cn/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'有道':
                if len(content)>=4:
                    weiji=content[3:]
                    if re.compile('[a-z]').findall(weiji):
                        	return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.youdao.com/w/'+weiji)
                    else:
                        ask = weiji.encode('UTF-8')
                        enask = urllib2.quote(ask)
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.youdao.com/w/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'俄汉':
                if len(content)>=4:
                    weiji=content[3:]
                    ask = weiji.encode('UTF-8')
                    enask = urllib2.quote(ask)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#ru/zh/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'汉俄':
                if len(content)>=4:
                    weiji=content[3:]
                    ask = weiji.encode('UTF-8')
                    enask = urllib2.quote(ask)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#zh/ru/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[0]==u'英':
                if len(content)>=3:
                    weiji=content[2:]
                    ask = weiji.encode('UTF-8')
                    enask = urllib2.quote(ask)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#en/zh/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[0]==u'汉':
                if len(content)>=4:
                    weiji=content[2:]
                    ask = weiji.encode('UTF-8')
                    enask = urllib2.quote(ask)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#zh/en/'+enask)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content==u'天气':
                return self.render.reply_text(fromUser,toUser,int(time.time()),'http://www.caiyunapp.com/map/')
            elif content[:2]==u'指令':
                if len(content)>=4:
                    try:
                        zhi=content[3:]
                        data={'username':zhi}
                        data = urllib.urlencode(data) 
                        request = urllib2.Request('http://520966b1.nat123.cc:10834/login', data=data)
                        response = urllib2.urlopen(request)
                        return_value=response.read().decode("utf8")
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令发送成功')
                    except:
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令发送失败，树莓派服未开启（10834端口）')
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'提醒':
                if len(content)>=4:
                    try:
                        zhi=content[3:]
                        data={'username':zhi}
                        data = urllib.urlencode(data) 
                        request = urllib2.Request('http://520966b1.nat123.cc:10834/login', data=data)
                        response = urllib2.urlopen(request)
                        return_value=response.read().decode("utf8")
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令发送成功')
                    except:
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令发送失败，树莓派服未开启（10834端口）')
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'指令输入错误，请检查后再输入')
            elif content[:2]==u'数据':
                if content>=4:
                    try:
                        da=content.split(' ')
                        if len(da)==4:
                            L=float(da[1])
                            H=float(da[2])
                            D=float(da[3])
                            dat=self.count(L,H,D)
                            if len(dat)==2:
                                return self.render.reply_text(fromUser,toUser,int(time.time()),u'F12,H ='+str(dat[0])+'\nF12,V =：'+str(dat[1]))
                            else:
                                return self.render.reply_text(fromUser,toUser,int(time.time()),dat[0])
                        else:
                            return self.render.reply_text(fromUser,toUser,int(time.time()),u'有数据遗漏【应该输入三个数据】，请检查后重新输入')
                    except:
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'指令不符合规范')
            elif content[:6]==u'线性回归方程':
                if content>=4:
                    try:
                        da=content.split(' ')
                        if len(da)==4:
                            xstr=da[2]
                            ystr=da[3]
                            formula=self.linear('yes',xstr,ystr)
                            return self.render.reply_text(fromUser,toUser,int(time.time()),formula)
                        elif len(da)==3:
                            xstr=da[1]
                            ystr=da[2]
                            formula=self.linear('no',xstr,ystr)
                            return self.render.reply_text(fromUser,toUser,int(time.time()),formula)
                        else:
                            return self.render.reply_text(fromUser,toUser,int(time.time()),'指令不符合规范')
                    except:
                        return self.render.reply_text(fromUser,toUser,int(time.time()),'指令不符合规范')
                            
            else:
                if re.compile('[a-z]').findall(content):
                    return self.render.reply_text(fromUser,toUser,int(time.time()),self._trans(content,fr='en',to='zh'))
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),self._trans(content,fr='zh',to='en'))
    def _film(self,furl):
        u='http://jqaaa.com/jx.php?url=&url='
        url = 'https://v.qq.com/x/search/?q='#腾讯
        ask = furl.encode('UTF-8')
        enask = urllib2.quote(ask)
        url = url+enask
        r = urllib2.urlopen(url)
        find=re.compile('a href="(.*?)" class="figure result_figure" ').findall(r.read())[0]
        return HTMLParser().unescape(str(u)+str(find))
    def _song(self,murl):
        url='http://music.163.com/song/media/outer/url?id='
        ID=re.compile(r'\d+').findall(murl)[1]
        surl=url+ID+'.mp3'
        return str(surl)
    def _trans(self,word,fr,to):
        appid='5aec697c047d5'
        appkey='6f5ac30e00e2cc6299d11e78b3913fc3'
        ask = word.encode('UTF-8')
        enask = urllib2.quote(ask)
        url='http://api.yeekit.com/dotranslate.php?from='+fr+'&to='+to+'&app_kid='+appid+'&app_key='+appkey+'&text='+enask
        r=urllib2.urlopen(url)
        text=r.read()
        fanyi=re.compile('text(.*?)transla').findall(text.replace('"','').replace('{','').replace('}','').replace('[','').replace(']','').replace(':','').replace('\n','').replace('\t',''))[0]
        if re.compile('[a-z]').findall(fanyi):
            return fanyi.replace('\'','`')
        else:
            return fanyi.replace(' ','')
    def _wea(self,word):
        url1='http://api.map.baidu.com/geocoder/v2/?address='
        url2='&output=json&ak=ED6kl4a3rKvi5QU7w7CBV21HUsVBUKNk'
        ask = word.encode('UTF-8')
        enask = urllib2.quote(ask)
        url=url1+enask+url2
        r = urllib2.urlopen(url)
        text=r.read()
        t=text.replace('"','').replace('{','').replace('}','').replace('[','').replace(']','').replace(':','').replace('\n','').replace('\t','')
        jing=re.compile('locationlng(.*?),lat').findall(t)
        wei=re.compile(',lat(.*?),preci').findall(t)
        la=[]
        la.append(jing[0])
        la.append(wei[0])
        return la

    def count(self,L,H,D):
        h=2*H/D
        S=2*L/D
        B=(1+S*S)/(2*S)
        A=(h*h)/(2*S)+B
        if (((A+1)*(S-1))/((A-1)*(S+1)))>0 and (((B+1)*(S-1))/((B-1)*(S+1)))>0:
            a=math.sqrt(((A+1)*(S-1))/((A-1)*(S+1)))
            b=math.sqrt(((B+1)*(S-1))/((B-1)*(S+1)))
            c=h/math.sqrt(S*S-1)
            d=math.sqrt((S-1)/(S+1))
            e=(B-1/S)/(math.pi*(B*B-1))
            f=(A-1/S)/(math.pi*(A*A-1))
            FH=e/math.tan(b)-f/math.tan(a)
            FV=(1/(math.pi*S))/math.tan(c)-(h/(math.pi*S))/math.tan(d)+(A*h/(math.pi*S*math.sqrt(A*A-1)))/math.tan(a)
            return [FH,FV]
        else:
            return ['输入数据不符合规范,计算过程中根号下出现负值，请检查后再输入']
    def linear(self,number,xstr,ystr):
        xtuple=eval(xstr)
        xlist=[]
        if number=='yes':
            for x in xtuple:
                if x>0:
                    xlist.append(math.log(float(x))) #这里的numpy.log(是为了金属工艺学实验而加的，后面必须去掉)变为：xlist=list(xtuple)
                else:
                    return('负数不能取对数')
        else:
            for i in xtuple:xlist.append(float(i))
        ytuple=eval(ystr)
        ylist=[]
        if number=='yes':
            for y in ytuple:
                if y>0:
                    ylist.append(math.log(float(y))) #这里的numpy.log(是为了金属工艺学实验而加的，后面必须去掉)变为：xlist=list(xtuple)
                else:
                    return('负数不能取对数')
        else:
            for i in ytuple:ylist.append(float(i))
        if len(ylist)==len(xlist):
            pass
        else:
            return('请确保输入的x数据和y数据个数相等')
        xaver=float(sum(xlist))/len(xlist)
        yaver=float(sum(ylist))/len(ylist)
        xy=[] 
        for i in xlist:
            for j in ylist:
                if xlist.index(i)==ylist.index(j):
                    a=i*j
                    xy.append(a)
        xx=[]
        for ii in xlist:
            b=ii**2
            xx.append(b)
        xyaver=float(sum(xy))/len(xy)
        xxaver=float(sum(xx))/len(xx)
        if (xaver**2-xxaver)!=0:
            para=(xaver*yaver-xyaver)/(xaver**2-xxaver)
            bbb=yaver-para*xaver
            if bbb>=0:
                if number=='yes':
                    return('线性方程为：y='+str(round((math.e)**bbb,4))+'x^'+str(round(para,4)))
                else:
                    	return('线性方程为：y='+str(round(para,4))+'x+'+str(round(bbb,4)))
            elif bbb<0: 
                if number=='yes':
                    return('线性方程为：y='+str(round((math.e)**bbb,4))+'x^'+str(round(para,4)))
                else:
                	return('线性方程为：y='+str(round(para,4))+'x'+str(round(bbb,4)))
        else:
            return("您的数据有错误！，请检查后重新输入")

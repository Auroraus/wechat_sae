# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time,random
import os,re
import urllib2,json
from lxml import etree
from HTMLParser import HTMLParser

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
        token="xxxxxxxxxxxx" #这里改写你在微信公众平台里输入的token
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
            if content==u'xx':
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'是一个大帅哥(：')
            elif content==u'实用网站':
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"http://1095f1f.nat123.cc:10834/myblog/info1.html")
            elif content==u'个人博客':
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"http://1095f1f.nat123.cc:10834/myblog/index.html")
            elif content[:2]==u'电影':
                flist=content.split(' ')
                return self.render.reply_text(fromUser,toUser,int(time.time()),film(flist[1]))
            elif content[:2]==u'歌曲':
                slist=content.split(' ')
                return self.render.reply_text(fromUser,toUser,int(time.time()),song(slist[-1]))
            elif content[:2]==u'帮助':
                return self.render.reply_text(fromUser,toUser,int(time.time()),content)
            elif content[:2]==u'维基':
                weiji=content[3:]
                if re.compile('[a-z]').findall(weiji):
                	return self.render.reply_text(fromUser,toUser,int(time.time()),'https://en.wikipedia.org/wiki/'+weiji)
                else:
                    weiji=trans(weiji,fr='zh',to='en').replace(' ','').replace(',','')
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'https://en.wikipedia.org/wiki/'+weiji)
            elif content[:2]==u'百科':
                weiji=content[3:]
                ask = weiji.encode('UTF-8')
                enask = urllib2.quote(ask)
                return self.render.reply_text(fromUser,toUser,int(time.time()),'https://baike.baidu.com/item/'+enask)
            elif content[:2]==u'知乎':
                weiji=content[3:]
                ask = weiji.encode('UTF-8')
                enask = urllib2.quote(ask)
                return self.render.reply_text(fromUser,toUser,int(time.time()),'https://www.zhihu.com/search?type=content&q='+enask)
            elif content[:5]==u'quora':
                weiji=content[6:]
                if re.compile('[a-z]').findall(weiji):
                	return self.render.reply_text(fromUser,toUser,int(time.time()),'https://en.wikipedia.org/wiki/'+weiji)
                else:
                    weiji=trans(weiji,fr='zh',to='en').replace(' ','').replace(',','')
                    return self.render.reply_text(fromUser,toUser,int(time.time()),'https://en.wikipedia.org/wiki/'+weiji)
            elif content[:2]==u'海词':
                weiji=content[3:]
                if re.compile('[a-z]').findall(weiji):
                    	return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.cn/'+weiji)
                else:
                   	ask = weiji.encode('UTF-8')
                   	enask = urllib2.quote(ask)
                   	return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.cn/'+enask)
            elif content[:2]==u'有道':
                weiji=content[3:]
                if re.compile('[a-z]').findall(weiji):
                    	return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.youdao.com/w/'+weiji)
                else:
                   	ask = weiji.encode('UTF-8')
                   	enask = urllib2.quote(ask)
                   	return self.render.reply_text(fromUser,toUser,int(time.time()),'http://dict.youdao.com/w/'+enask)
            elif content[:2]==u'俄汉':
                weiji=content[3:]
                return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#ru/zh/'+weiji)
            elif content[:2]==u'汉俄':
                weiji=content[3:]
                ask = weiji.encode('UTF-8')
                enask = urllib2.quote(ask)
                return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#zh/ru/'+enask)
            elif content[0]==u'英':
                weiji=content[2:]
                return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#en/zh/'+weiji)
            elif content[0]==u'汉':
                weiji=content[2:]
                ask = weiji.encode('UTF-8')
                enask = urllib2.quote(ask)
                return self.render.reply_text(fromUser,toUser,int(time.time()),'http://fanyi.baidu.com/translate#zh/en/'+enask)
            elif content==u'天气':
                return self.render.reply_text(fromUser,toUser,int(time.time()),'http://www.caiyunapp.com/map/')
            else:
                if re.compile('[a-z]').findall(content):
                    return self.render.reply_text(fromUser,toUser,int(time.time()),trans(content,fr='en',to='zh'))
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),trans(content,fr='zh',to='en'))
def film(furl):
    u='http://jqaaa.com/jx.php?url=&url='
    url = 'https://v.qq.com/x/search/?q='#腾讯
    ask = furl.encode('UTF-8')
    enask = urllib2.quote(ask)
    url = url+enask
    r = urllib2.urlopen(url)
    find=re.compile('a href="(.*?)" class="figure result_figure" ').findall(r.read())[0]
    return HTMLParser().unescape(str(u)+str(find))
def song(murl):
    url='http://music.163.com/song/media/outer/url?id='
    ID=re.compile(r'\d+').findall(murl)[1]
    surl=url+ID+'.mp3'
    return str(surl)
def trans(word,fr,to):
    appid='xxxxxx'
    appkey='xxxxxxxxxxx'
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
def wea(word):
    url1='http://api.map.baidu.com/geocoder/v2/?address='
    url2='&output=json&ak=【你的百度地图ak号】'
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



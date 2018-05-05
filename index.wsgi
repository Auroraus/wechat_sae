# coding: UTF-8
import os
import sae
import web
from index import WeixinInterface
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
urls = ('/weixin','WeixinInterface')
app = web.application(urls, globals()).wsgifunc()        
application = sae.create_wsgi_app(app)

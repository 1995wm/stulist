# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

import reqs
import os.path



handlers = [
    (r"/aa",  reqs.MaineHandler),
    (r"/login",  reqs.LoginHandler),
    (r"/logout",  reqs.LogoutHandler),
    (r"/xw1", reqs.Xw1Handler),
    (r"/xw2", reqs.Xw2Handler),
    (r"/xw3", reqs.Xw3Handler),
    (r"/xw4", reqs.Xw4Handler),
    (r"/xw5", reqs.Xw5Handler),
    (r"/xw6", reqs.Xw6Handler),
    (r"/xw7", reqs.Xw7Handler),
    (r"/xw8", reqs.Xw8Handler),
    (r"/xw9", reqs.Xw9Handler),
    (r"/xsgl", reqs.XsglHandler),
    (r"/xw", reqs.XwHandler),
    (r"/coulist", reqs.CourseListHandler),
    (r"/couedit/(\d+|new)", reqs.CourseEditHandler),
    (r"/coudel/(\d+)", reqs.CourseDelHandler),
    (r"/", reqs.MainHandler),
]

home_path = os.path.dirname(__file__)

settings = {
     "cookie_secret":"_此处为应为随机生成的密钥_",
     "login_url":'/login', # 妆饰器@tornado.web.authenticated认证失败需要转向登录的url
     "static_path": os.path.join(home_path, "static"),
    "debug": "true"
}

application = tornado.web.Application(handlers, **settings)

application.listen(8080)

if __name__ == '__main__':
    import ioloop
    ioloop.run() # 服务主调度

# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor
user_passwds = { 'xy' : '1', 'qq' : '2' ,'gmr':'3','gs':4,'wj':'5'}
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # 重载RequestHandler函数，以便子类可以使用current_user属性得到合法用户的标识
        # 如果当前用户没有验证，则没有相应的cookie，因此返回的是None
        return self.get_secure_cookie("user")
class MaineHandler(BaseHandler):

    """首页处理器"""
    @tornado.web.authenticated
    def get(self):
        # 使用妆饰器@tornado.web.authenticated完成这段所注释的逻辑
        # # 如果没有合法用户存在，则重定向到登录页面，要求用户登录
        # if not self.current_user:
        #     self.redirect("/login") # 重定向到登录页面
        #     return

        user_id = tornado.escape.xhtml_escape(self.current_user)
        self.render("pages/main1.html", user_id=user_id)
class LoginHandler(BaseHandler):
    """登录处理器"""

    def get(self):
        """绘制登录页面"""
        self.render("pages/login.html", errmsg=None)

    def post(self):
        """验证登录表单录入的用户名和密码是否一致"""

        userid = self.get_argument('userid')
        passwd = self.get_argument('passwd')

        # 检查输入的密码和密码表的密码是否一致
        if passwd != user_passwds.get(userid, None):
            self.render("pages/login.html", errmsg='验证失败')
            self.set_status(403) # 设置状态码
            return

        # 验证成功，利用cookie设置已验证的用户信息
        self.set_secure_cookie("user", userid)
        self.redirect("/coulist") # 验证成功，重定向到首页

class LogoutHandler(BaseHandler):
    """注销登录请求的处理器"""
    def get(self):
        # 清除含有用户信息的cookie，即为注销登录
        self.clear_cookie("user") 
        self.redirect("/aa")
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")
class Xw1Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻1.html")
class Xw2Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻2.html")
class Xw3Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻3.html")
class Xw4Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻4.html")
class Xw5Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻5.html")
class Xw6Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻6.html")
class Xw7Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻7.html")
class Xw8Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻8.html")
class Xw9Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/新闻9.html")
class XsglHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/xsgl.html")
class XwHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/xinwen.html")
class CourseListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_list.html", courses = dal_list_courses())

class CourseEditHandler(tornado.web.RequestHandler):
    def get(self, stu_no):

        cou = None
        if stu_no != 'new' :
            cou = dal_get_course(stu_no)
        
        if cou is None:
            cou = dict(stu_no='new', cou_no='', name='',sex='',pro='',grade='',
                       notes='')

        self.render("pages/cou_edit.html", course = cou)

    def post(self, stu_no):
        cou_no = self.get_argument('cou_no')
        name = self.get_argument('name', '')
        sex = self.get_argument('sex','')
        pro = self.get_argument('pro','')
        grade = self.get_argument('grade','')
        notes = self.get_argument('notes', '')

        if stu_no == 'new' :
            dal_create_course(cou_no, name,sex,pro,grade,
                       notes)
        else:
            dal_update_course(stu_no, cou_no, name,sex,pro,grade, notes)

        self.redirect('/coulist')

class CourseDelHandler(tornado.web.RequestHandler):
    def get(self, stu_no):
        dal_del_course(stu_no)
        self.redirect('/coulist')

# -------------------------------------------------------------------------

def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_no, cou_no, name, sex,pro,grade,notes FROM course ORDER BY stu_no DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(stu_no=r[0], cou_no=r[1], name=r[2], sex=r[3],pro=r[4],
                       grade=r[5],notes=r[6])
            data.append(cou)
    return data


def dal_get_course(stu_no):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_no, cou_no, name,sex,pro,grade, notes FROM course WHERE stu_no=%s
        """
        cur.execute(s, (stu_no, ))
        r = cur.fetchone()
        if r :
            return dict(stu_no=r[0], cou_no=r[1], name=r[2], sex=r[3],pro=r[4],
                       grade=r[5],notes=r[6])


def dal_create_course(cou_no, name, sex,pro,grade,notes):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_stu_no')")
        stu_no = cur.fetchone()
        assert stu_no is not None

        print('新课程内部序号%d: ' % stu_no)

        s = """
        INSERT INTO course (stu_no, cou_no, name,sex,pro,grade, notes) 
        VALUES (%(stu_no)s, %(cou_no)s, %(name)s, %(sex)s,%(pro)s,%(grade)s, %(notes)s)
        """
        cur.execute(s, dict(stu_no=stu_no, cou_no=cou_no, name=name,sex=sex,pro=pro,grade=grade, notes=notes))


def dal_update_course(stu_no, cou_no, name, sex, pro, grade, notes):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE course SET
          cou_no=%(cou_no)s, 
          name=%(name)s,
          sex=%(sex)s,
          pro=%(pro)s,
          grade=%(grade)s, 
          notes=%(notes)s
        WHERE stu_no=%(stu_no)s
        """
        cur.execute(s, dict(stu_no=stu_no, cou_no=cou_no, name=name,sex=sex,pro=pro,grade=grade, notes=notes))


def dal_del_course(stu_no):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM course WHERE stu_no=%(stu_no)s
        """
        cur.execute(s, dict(stu_no=stu_no))
        print('删除%d条记录' % cur.rowcount)

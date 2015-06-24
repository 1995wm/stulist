#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS course;

    CREATE TABLE IF NOT EXISTS course  (
        stu_no   INTEGER,     --序号
        cou_no   TEXT,        --学生号
        name     TEXT,        --姓名
        sex      TEXT,       --性别
        pro      TEXT,        --专业
        grade    TEXT,        --成绩
        notes    TEXT,        --备注
        PRIMARY KEY(stu_no)
    );
    -- CREATE UNIQUE INDEX idx_stu_no ON course(cou_no);

    CREATE SEQUENCE seq_stu_no 
        START 10000 INCREMENT 1 OWNED BY course.stu_no;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM course;

    INSERT INTO course (stu_no,cou_no, name,sex,pro,grade,notes)  VALUES 
        (101,'1','邓硕成','男','信息',98,'学委'), 
        (102,'2','张付东','男','信息',98,'心理委员'),
        (103, '3','郭明睿','女','信息',98,'团委');

    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')


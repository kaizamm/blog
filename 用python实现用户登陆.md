---
title: 用python实现用户登陆
date: 2017.7.4

---
### 流程图
![用户登陆流程图][用户登陆流程图]
[用户登陆流程图]: ./用python实现用户登陆/用户登陆流程图.png


### 代码

```
#!/usr/bin/env python
# _*_ coding=utf-8 _*_
# @python2.7

import os,sys
username = "" #定义全局变量
password = "" #定义全局变量
i=0  # 循环次数
while(i<3):  #while...else语法
  username = raw_input("enter your username:")
  password = raw_input("enter your password:")
  with open("denied_file.txt","r") as f: #打开文件方式用with open,避免open打开文件句柄后需关闭
    for line in f.readlines():
      with open("denied_file.txt","r") as f:
        #print line.strip().split()  #str的方法strip()去掉多余无关字符如 "\n"空格，split()取字符串
        if username.strip().split() == line.strip().split():
          sys.exit("locked")
  if username == "kaizamm" and password == "123456":
    print "Welcome,%s" % username
    break
  else:
    print "fail,you have %s shots" % (2-i)
    i += 1
else:
  with open("denied_file.txt","a") as f:
    f.write("\n")
    f.write(username)
    sys.exit("locked")

```

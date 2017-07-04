#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import os,sys
i=0
password = ""
username = ""
while(i<3):
  username = raw_input("enter your username:")
  password = raw_input("enter your password:")
  with open("denied_file.txt","r") as f:
    for line in f.readlines():
      with open("denied_file.txt","r") as f:
        #print line.strip().split()
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

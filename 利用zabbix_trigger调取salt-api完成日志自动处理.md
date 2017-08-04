---
title: 利用zabbix trigger调取salt-api完成日志自动处理
date: 2017.8.4
---
### 准备工作
安装好对应zabbix server/agent，salt-master、salt-minion、salt-api

### 对应zabbix添加script,action
![1.png][1.png]
[1.png]: ./利用zabbix_trigger调取salt-api完成日志自动处理/1.png
### 对应zabbix添加script,action
![2.png][2.png]
[2.png]: ./利用zabbix_trigger调取salt-api完成日志自动处理/2.png
![3.png][3.png]
[3.png]: ./利用zabbix_trigger调取salt-api完成日志自动处理/3.png
![4.png][4.png]
[4.png]: ./利用zabbix_trigger调取salt-api完成日志自动处理/4.png
![5.png][5.png]
[5.png]: ./利用zabbix_trigger调取salt-api完成日志自动处理/5.png

### ZABBIX 传参
![6.png][6.png]
[6.png]: ./利用zabbix_trigger调取salt-api完成日志自动处理/6.png

### ZABBIX执行脚本
```
#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
#BGP-NETAM-01
__author__ = "kaiz"

import sys,os,requests,time,re
cur_time = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))

if __name__ == "__main__":
  session = requests.Session()
  session.post('http://172.30.33.183:7991/login', json={
    'username': 'Lsaltapiuser',
    'password': '&87YuApi$',
    'eauth': 'pam',
  })
  try:
    hostname = sys.argv[1]
    log_path = sys.argv[2]
    bak_path_ = sys.argv[3]
    save_days = sys.argv[4]
    resp = session.post('http://172.30.33.183:7991', json=[{
      'client': 'local',
      'tgt': hostname,
      'fun': 'state.sls',
      'arg': ['logrotate'],
      'kwarg': {"pillar":{"log_path":log_path,"bak_path_":bak_path_,"save_days":save_days}},
    }])
    a = str(resp.json())
    print "INFO:" + a
    m = re.search("The function \"state.sls\" is running as PID",a)
    if m is not None:
      #若能匹配到The function \"state.sls\" is running as PID这个，则取出jid
      list = a.strip().split()
      index = list.index("jid")+1
      jid = re.search("\d+",list[index])
      jid = jid.group()
      #取出jid后执行类似salt '*' saltutil.signal_job 20140211102239075243 15
      resp = session.post('http://172.30.33.183:7991', json=[{
      'client': 'local',
      'tgt': hostname,
      'fun': 'saltutil.signal_job',
      'arg': [ jid,'15'],
    }])
      aa = resp.json
      with open("/tmp/logrotate.log","w") as f:
        f.write(cur_time+':'+str(aa)+"\n")
      print "INFO:"+"saltutil.signal_job jid 15"+str(aa)
  except Exception, e:
    err = str(e)
    err = "EROR"+":"+cur_time+":"+err
    print err
    with open("/tmp/logrotate_err.log","w") as f:
      f.write(err)


```

### SALT 模块调用
```
#!/USR/BIN/ENV PYTHON
# _*_ ENCODING: UTF-8 _*_
__AUTHOR__="KAIZ"

IMPORT OS,SYS,TIME

#处理日志
CLASS ANAYSISLOG:
    #两个变量，备份目录及目录名，初始化
    DEF __INIT__(SELF,BAK_PATH,LOG_PATH,SAVE_DAYS):
        SELF.BAK_PATH = BAK_PATH
        SELF.LOG_PATH = LOG_PATH
        SELF.SAVE_DAYS = SAVE_DAYS

    #压缩日志文件
    DEF LOGROTATE(SELF):
        #开始压缩
        PRINT "[INFO]START LOGROTATE,WAIT..."
        #文件压缩信号
        IF NOT OS.PATH.ISDIR(BAK_PATH): OS.MAKEDIRS(BAK_PATH)
        LOGROTATE_FILE_FLAG1 = OS.POPEN('FIND %S -MTIME +%S -NAME "*TXT" ' % (LOG_PATH,SAVE_DAYS)).READLINES()
        LOGROTATE_FILE_FLAG2 = OS.POPEN('FIND %S -MTIME +%S -NAME "*LOG" ' % (LOG_PATH,SAVE_DAYS)).READLINES()
        LOGROTATE_FILE_FLAG3 = OS.POPEN('FIND %S -MTIME +%S -NAME "*GZ" ' % (LOG_PATH,SAVE_DAYS)).READLINES()
        LOGROTATE_FILE_FLAG4 = OS.POPEN('FIND %S -MTIME +%S -NAME "*BZ2" ' % (LOG_PATH,SAVE_DAYS)).READLINES()
        LOG_PATH_ = OS.PATH.DIRNAME(OS.PATH.DIRNAME(LOG_PATH))
        LOGROTATE_FILE_FLAG5 = OS.POPEN('FIND %S -NAME "CATALINA.OUT" ' % LOG_PATH_).READLINES()
        LOGROTATE_FILE_FLAG6 = OS.POPEN('FIND %S -MTIME +30 ' % BAK_PATH).READLINES()
        #开始移动日志到备份目录
        OS.POPEN('FIND %S -MTIME +%S -NAME "*TXT" -EXEC MV {} %S \;' % (LOG_PATH,SAVE_DAYS,BAK_PATH))
        OS.POPEN('FIND %S -MTIME +%S -NAME "*LOG" -EXEC MV {} %S \;' % (LOG_PATH,SAVE_DAYS,BAK_PATH))
        OS.POPEN('FIND %S -NAME "*GZ" -EXEC MV {} %S \;' % (LOG_PATH,BAK_PATH))
        OS.POPEN('FIND %S -NAME "*BZ2" -EXEC MV {} %S \;' % (LOG_PATH,BAK_PATH))
        #删除BAK_PATH的一个月以前的压缩文件
        IF LOGROTATE_FILE_FLAG6:
            OS.POPEN('FIND %S -MTIME +30 -EXEC RM {} -RF \;' % BAK_PATH)
            PRINT "DEL FILES BEFORE 30 DAYS UNDER %S" % BAK_PATH
        #将备份目录里的日志压缩打包
        OS.POPEN('FIND %S  -NAME "*LOG" -EXEC BZIP2 {} \;' % BAK_PATH)
        #是否有文件被移动或CATALINA.OUT是否被清空
        IF LOGROTATE_FILE_FLAG1 OR LOGROTATE_FILE_FLAG2 OR LOGROTATE_FILE_FLAG3 OR LOGROTATE_FILE_FLAG4:
            PRINT "[INFO]LOGROTATE SUCCESS"
        ELIF LOGROTATE_FILE_FLAG5:
            #清空CATALINA.OUT
            WITH OPEN (LOGROTATE_FILE_FLAG5[0].STRIP(),"R+") AS F:
                F.TRUNCATE()
            PRINT "[INFO]JUST TRUNCATE CATALINA.OUT"
        ELSE:
            PRINT "[INFO]LOGROTATE NOTHING"

#主程序从这开始
IF __NAME__ == "__MAIN__":
    #实例化
    TRY:
    #源日志目录
        LOG_PATH = SYS.ARGV[1]
        #备份目录，取当前时间
        CUR_TIME = TIME.STRFTIME('%Y-%M-%D-%H:%M')
        BAK_PATH_ = SYS.ARGV[2]
        BAK_PATH = BAK_PATH_+'/'+CUR_TIME
        #在源日志目录保留日志的天数
        SAVE_DAYS = SYS.ARGV[3]
        A = ANAYSISLOG(LOG_PATH,BAK_PATH_,LOG_PATH)
        #压缩
        A.LOGROTATE()
    EXCEPT EXCEPTION,E:
        ERR = "[ERROR]"+CUR_TIME+STR(E)+"\N"
        WITH OPEN("/TMP/LOGRATE_ERR.LOG","A+") AS F:
          F.WRITE(ERR)
        PRINT ERR

```

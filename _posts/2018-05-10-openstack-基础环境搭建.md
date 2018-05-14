---
layout: post
title:  openstack基础环境搭建
date:   2018-05-10
categories: document
tag:
  - openstack

---
* content
{:toc}

### 概述
[官网](https://docs.openstack.org/mitaka/zh_CN/install-guide-rdo/)
[参考1](https://www.cnblogs.com/nmap/p/6416017.html)
[参考2](https://www.unixhot.com/article/407)


openstack三大项，**计算**、**网络**、**存储**。

OpenStack是一个由NASA（美国国家航空航天局）和Rackspace合作研发并发起的，以Apache许可证授权的自由软件和开放源代码项目。

openstack主要目标是来简化资源的管理和分配，把计算 网络 存储。三大项虚拟成三大资源池，例如需要计算资源我这里可以提供，需要网络资源这里也可以提供以及存储资源的需求，对外提供api，通过api进行交互。


计算资源：管理cpu和内存 <br>
存储资源：存储数据 <br>
网络资源：网络资源这块，最近比较火的就是SDN，软件定义网络，真正生产使用的很少。青云的sdn做的比较好<br>

命名从A开始<br>
E版开始，在国内开始有用了，此时功能比较简陋，G版用的也比较多
I 版 ：最后一个支持centos6和python2.6的，I版本以后的都是默认python2.7开始的了

<img src="{{ '/styles/images/openstack/release.png' | prepend: site.baseurl }}" alt="示意图" width="810" />

<img src="{{ '/styles/images/openstack/overview-diagram.svg' | prepend: site.baseurl }}" alt="示意图" width="810" />

业界使用openstack做公有云的有：金山云，乐视云，京东云，携程，惠普云，华为，IBM

阿里云，青云，腾讯云都是自己开发的

私有云以vmware为主

### 关键服件
openstack系统由几个关键服件组成，**计算服务**,**认证服务**，**网络服务**，**镜像服务**，**块存储服务**，**对象存储服务**，**计量服务**，**编排服务**，**数据库服务**。

+ 认证服务（Identity，代号为“Keystone”）


用数据库连接客户端以 root 用户连接到数据库服务器
```
mysql -uroot -p
```
创建 keystone 数据库
```
CREATE DATABASE keystone;
```
对keystone给予恰当权限
```
MariaDB [(none)]> grant all privileges on keystone.* to 'keystone'@'localhost' identified by '123.com';
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> grant all privileges on keystone.* to 'keystone'@'%' identified by '123.com';
Query OK, 0 rows affected (0.00 sec)
```
退出后生成一个随机值，在初始的配置中作为管理员的令牌
```
[root@linux-node3 system]# openssl rand -hex 10
2cc4ea41401aae657ac2
```

安装并配置组件

*使用带有mod_wsgi的Apache HTTP服务器来服务认证服务请求，端口为5000和35357。缺省情况下，Kestone服务仍然监听这些端口。然而，本教程手动禁用keystone服务。*



+ 计算服务(Compute，代号为“Nova”)

根据需求提供虚拟的服务器。Rackspace和HP公司提供商业云计算服务正是建立在Nova之上，在Mercado Libre和NASA（Nova项目的起源地）内部也是使用的Nova。
+ 控制面板（Dashboard，代号为“Horizon”）

为OpenStack的所有服务提供一个模块化的基于Web的用户界面。使用这个Web图形界面，可以完成云计算平台上的大多数的操作，如启动客户机、分配IP地址、设置访问控制权限等。
<img src="{{ '/styles/images/openstack/dashboard.png' | prepend: site.baseurl }}" alt="" width="810" />

+ 网络服务（Network，代号为“Neutron”）

+ 镜像服务（Image，代号为“Glance”）

+ 块存储服务（Block Storage，代号为“Cinder”）

+ 对象存储服务（Object Storage，代号为“Swift”）

提供的对象存储服务，允许对文件进行存储或者检索（但不是通过挂载文件服务器上目录的方式来实现）。
目前已经有好几家公司开始提供基于Swift的商业存储服务，这些公司包括KT公司、Rackspace公司（Swift项目的发源地）和Internap公司，
而且，有很多大公司内部也使用Swift来存储数据。
+ 计量服务

+ 编排服务

+ 数据库服务

+ 文件共享系统服务

+ Telemetry服务

[更多](https://docs.openstack.org/mitaka/zh_CN/install-guide-rdo/)

### 实验环境准备
硬件所需最小资源
<img src="{{ '/styles/images/openstack/hwreqs.png' | prepend: site.baseurl }}" alt="示意图" width="810" />

Vmware Workstation<br>
虚拟机系统2个<br>
系统版本：centos7.1.1503 x86_64<br>
内存：4GB<br>
网络：两台机器都是nat<br>
磁盘：40GB<br>
额外：勾选vt-x<br>
注意：vmare的网关为x.x.x.2，所以nameserver也要设置为x.x.x.2<br>
IP:

|          控制节点      |          计算节点     |
|-----------------------|-----------------------|
|     192.168.56.11     |     192.168.56.12     |
|linux-node1.example.com|linux-node2.example.com|


在安装系统时，设置Bios保证网卡名为eth0<br>
网卡设置
```
[root@linux-node1 ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE="Ethernet"
BOOTPROTO="static"
NAME="eth0"
DEVICE="eth0"
ONBOOT="yes"
IPADDR="192.168.56.11"
NETMASK="255.255.255.0"
GATEWAY="192.168.56.2"
```

两台主机配好主机名解析
```
[root@linux-node1 ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.56.11 linux-node1 linux-node1.example.com
192.168.56.12 linux-node2 linux-node2.example.com
```

时钟同步<br>

----------------------------
~~以下这个可以忽略，可当作个补充，请直接跳转至虚线以下~~

 控制节点和计算节点同步时间，这里去同步阿里云的时间服务器
```
[root@linux-node1 ~]# yum install -y ntpdate
[root@linux-node1 ~]# ntpdate time1.aliyun.com
```
当然也可以设置控制节点为时间服务器，让计算节点来同步<br>
这个地方使用ntpdate(相当于是ntpd的客户端命令，当服务端装一个ntpd服务后，可以使用这个命令，让client与server保持时间同步)，不过centos7开始默认使用chrony，不过，即使这个不在使用，也比直接用date -s 10：00  这种强行来改时间的方法强。关于chrony，这里延伸一下
```
#chrony的相关用法
timedatectl #查看日期时间、时区及NTP状态
timedatectl list-timezones #查看时区列表
timedatectl set-timezone Asia/Shanghai #修改时区
timedatectl set-time "2015-01-21 11:50:00" #（可以只修改其中一个） 修改日期时间
timedatectl set-ntp true/flase  #开启NTP
timedatectl  status #查看状态
chronyc tracking #校准时间服务器
```
关于用chrony设置集群中时间同步，client及server都需要将配置文件中的同步源修改为server IP,[参考1](https://renwole.com/archives/1032)  [参考2](https://www.cnblogs.com/clsn/archive/2017/11/16/7844857.html)
```
firewall-cmd --add-service ntp
```
------------------------

```
yum install -y chrony && systemctl start chronyd.service && systemctl enable chronyd.service
```

换阿里源
```
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
yum makecache
```

如果不换阿里源，装个epel仓库也行，二选一即可
```
rpm -ivh http://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm
```

安装openstack仓库
```
yum install -y centos-release-openstack-queens
```

安装openstack仓库,此时安装queen版本
```
yum install -y centos-release-openstack-queens
```


安装openstack client
```
yum install -y python-openstackclient
```
安装openstack selinx包,生产中我我们通常关闭selinx,但是如果我们不关闭,我们可以通过这个软件对它自动配置。
```
yum install -y openstack-selinux
```
安装mysql
```
yum install -y mariadb mariadb-server python2-PyMySQL   
```
修改mysql配置文件



启动mysql
```
systemctl start mariadb && systemctl enable mariadb
```
初始化
```
mysql_secure_installation
```

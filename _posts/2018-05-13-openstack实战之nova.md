---
layout: post
title:  openstack实战之nova
date:   2018-05-13
categories: document
tag:
  - openstack

---
* content
{:toc}

## 控制节点
### 安装
```
yum install -y openstack-nova-api openstack-nova-placement-api \
  openstack-nova-conductor openstack-nova-console \
  openstack-nova-novncproxy openstack-nova-scheduler
```

### 数据库配置
```
vim /etc/nova/nova.conf
[api_database]
connection= mysql+pymysql://nova:nova@192.168.56.11/nova_api
[database]
connection= mysql+pymysql://nova:nova@192.168.56.11/nova
```

### RabbitMQ配置
```
#vim /etc/nova/nova.conf
[DEFAULT]
transport_url = rabbit://openstack:openstack@192.168.56.11
```

### Keystone相关配置
```
#vim /etc/nova/nova.conf
[api]
auth_strategy=keystone
[keystone_authtoken]
auth_uri = http://192.168.56.11:5000
auth_url = http://192.168.56.11:35357
memcached_servers = 192.168.56.11:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = nova
```

5.关闭Nova的防火墙功能
```
[DEFAULT]
use_neutron=true
firewall_driver = nova.virt.firewall.NoopFirewallDriver
```
6.VNC配置
```
# vim /etc/nova/nova.conf
[vnc]
enabled=true
server_listen = 0.0.0.0
server_proxyclient_address = 192.168.56.11
```
7.设置glance
```
[glance]
api_servers = http://192.168.56.11:9292
```
8.在 [oslo_concurrency] 部分，配置锁路径：
```
[oslo_concurrency]
lock_path=/var/lib/nova/tmp
```

9.设置启用的api
```
[DEFAULT]
enabled_apis=osapi_compute,metadata
```
10.设置placement
```
[placement]
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://192.168.56.11:35357/v3
username = placement
password = placement
```
11.修改nova-placement-api.conf
```
# vim /etc/httpd/conf.d/00-nova-placement-api.conf
<Directory /usr/bin>
   <IfVersion >= 2.4>
      Require all granted
   </IfVersion>
   <IfVersion < 2.4>
      Order allow,deny
      Allow from all
   </IfVersion>
</Directory>
</VirtualHost>
# systemctl restart httpd

```
12.同步数据库
```
su -s /bin/sh -c "nova-manage api_db sync" nova
```
注册cell0数据库
```
su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
```
13.创建cell1的cell
```
su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
```
14.同步nova数据库
```
su -s /bin/sh -c "nova-manage db sync" nova
```
15.验证cell0和cell1的注册是否正确
```
nova-manage cell_v2 list_cells
```
16.测试数据库同步情况
```
mysql -h 192.168.56.11 -unova -pnova -e " use nova;show tables;"
mysql -h 192.168.56.11 -unova -pnova -e " use nova_api;show tables;"
```
17.启动Nova Service
```
# systemctl enable openstack-nova-api.service \
openstack-nova-consoleauth.service \
  openstack-nova-scheduler.service \
openstack-nova-conductor.service \
  openstack-nova-novncproxy.service

# systemctl start openstack-nova-api.service \
  openstack-nova-consoleauth.service \
  openstack-nova-scheduler.service openstack-nova-conductor.service \
  openstack-nova-novncproxy.service
```
### Nova服务注册
```
# source admin-openstack.sh
# openstack service create --name nova --description "OpenStack Compute" compute
# openstack endpoint create --region RegionOne compute public http://192.168.56.11:8774/v2.1
# openstack endpoint create --region RegionOne compute internal http://192.168.56.11:8774/v2.1
# openstack endpoint create --region RegionOne compute admin http://192.168.56.11:8774/v2.1

# openstack service create --name placement --description "Placement API" placement
# openstack endpoint create --region RegionOne placement public http://192.168.56.11:8778
# openstack endpoint create --region RegionOne placement internal http://192.168.56.11:8778
# openstack endpoint create --region RegionOne placement admin http://192.168.56.11:8778
```

验证控制节点服务

```
openstack host list
```

## 计算节点安装
```
[root@linux-node2 ~]# yum install -y openstack-nova-compute sysfsutils

[root@linux-node1 ~]# scp /etc/nova/nova.conf 192.168.56.12:/etc/nova/nova.conf
[root@linux-node2 ~]# chown root:nova /etc/nova/nova.conf
```
1.删除多余的数据配置

2.修改VNC配置
计算节点需要监听所有IP，同时设置novncproxy的访问地址
```
[vnc]
enabled=true
server_listen = 0.0.0.0
server_proxyclient_address = 192.168.56.12
novncproxy_base_url = http://192.168.56.11:6080/vnc_auto.html
```
3.虚拟化适配
```
[root@linux-node2 ~]# egrep -c '(vmx|svm)' /proc/cpuinfo
[libvirt]
virt_type=qemu
```
如果返回的是非0的值，那么表示计算节点服务器支持硬件虚拟化，需要在nova.conf里面设置
```
[libvirt]
virt_type=kvm
```

启动nova-compute
```
# systemctl enable libvirtd.service openstack-nova-compute.service
# systemctl start libvirtd.service openstack-nova-compute.service
```
验证计算节点
```
[root@linux-node1 ~]# openstack host list
```
计算节点加入控制节点
```
[root@linux-node1 ~]# su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
```

---
layout: post
title:  openstack实战篇之neutron（5）
date:   2018-05-13
categories: project
tag:
  - openstack

---
* content
{:toc}

### Neutron安装
```
[root@linux-node1 ~]# yum install -y openstack-neutron openstack-neutron-ml2 \
openstack-neutron-linuxbridge ebtables
```
### Neutron数据库配置
```
[root@linux-node1 ~]# vim /etc/neutron/neutron.conf
[database]
connection = mysql+pymysql://neutron:neutron@192.168.56.11:3306/neutron
```
### Keystone连接配置
```
[DEFAULT]
…
auth_strategy = keystone

[keystone_authtoken]
auth_uri = http://192.168.56.11:5000
auth_url = http://192.168.56.11:35357
memcached_servers = 192.168.56.11:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = neutron
```
### RabbitMQ相关设置
```
[root@linux-node1 ~]# vim /etc/neutron/neutron.conf
[DEFAULT]
transport_url = rabbit://openstack:openstack@192.168.56.11
```
### Neutron网络基础配置
```
[DEFAULT]
core_plugin = ml2
service_plugins =
```
### 网络拓扑变化Nova通知配置
```
[DEFAULT]
notify_nova_on_port_status_changes = True
notify_nova_on_port_data_changes = True

[nova]
auth_url = http://192.168.56.11:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = nova
password = nova

#在 [oslo_concurrency] 部分，配置锁路径：
[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
```
### Neutron ML2配置
```
[root@linux-node1 ~]# vim /etc/neutron/plugins/ml2/ml2_conf.ini
[ml2]
type_drivers = flat,vlan,gre,vxlan,geneve #支持多选，所以把所有的驱动都选择上。
tenant_network_types = flat,vlan,gre,vxlan,geneve #支持多项，所以把所有的网络类型都选择上。
mechanism_drivers = linuxbridge,openvswitch,l2population #选择插件驱动，支持多选，开源的有linuxbridge和openvswitch
#启用端口安全扩展驱动
extension_drivers = port_security,qos

[ml2_type_flat]
#设置网络提供
flat_networks = provider

[securitygroup]
#启用ipset
enable_ipset = True
```
### Neutron Linuxbridge配置
```
[root@linux-node1 ~]# vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = provider:eth0

[vxlan]
#禁止vxlan网络
enable_vxlan = False

[securitygroup]
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
enable_security_group = True

```
### Neutron DHCP-Agent配置
```
[root@linux-node1 ~]# vim /etc/neutron/dhcp_agent.ini
[DEFAULT]
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = True

```
### Neutron metadata配置
```   
[root@linux-node1 ~]# vim /etc/neutron/metadata_agent.ini
[DEFAULT]
nova_metadata_host = 192.168.56.11

metadata_proxy_shared_secret = unixhot.com
```
### Neutron相关配置在nova.conf
```
[root@linux-node1 ~]# vim /etc/nova/nova.conf
[neutron]
url = http://192.168.56.11:9696
auth_url = http://192.168.56.11:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
service_metadata_proxy = True
metadata_proxy_shared_secret = unixhot.com

[root@linux-node1 ~]# ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
```
同步数据库
```
[root@linux-node1 ~]# su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
--config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
```
### 重启计算API 服务
```
# systemctl restart openstack-nova-api.service
```
启动网络服务并配置他们开机自启动。
```
# systemctl enable neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service
# systemctl start neutron-server.service \
  neutron-linuxbridge-agent.service neutron-dhcp-agent.service \
  neutron-metadata-agent.service
```
### Neutron服务注册
```
# openstack service create --name neutron --description "OpenStack Networking" network
```
创建endpoint
```
# openstack endpoint create --region RegionOne network public http://192.168.56.11:9696
# openstack endpoint create --region RegionOne network internal http://192.168.56.11:9696
# openstack endpoint create --region RegionOne network admin http://192.168.56.11:9696
```
### 测试Neutron安装
```
[root@linux-node1 ~]# openstack network agent list
```
### Neutron计算节点部署

安装软件包
```
 [root@linux-node2 ~]# yum install -y openstack-neutron openstack-neutron-linuxbridge ebtables
```
### Keystone连接配置
```
[root@linux-node2 ~]# vim /etc/neutron/neutron.conf
[DEFAULT]
…
auth_strategy = keystone

[keystone_authtoken]
auth_uri = http://192.168.56.11:5000
auth_url = http://192.168.56.11:35357
memcached_servers = 192.168.56.11:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = neutron
```
### RabbitMQ相关设置
```
[root@linux-node2 ~]# vim /etc/neutron/neutron.conf
[DEFAULT]  
transport_url = rabbit://openstack:openstack@192.168.56.11   #注意是在DEFAULT配置栏目下，因为该配置文件有多个transport_url的配置
```


### 锁路径
```
[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
```
### 配置LinuxBridge配置
```
[root@linux-node1 ~]# scp /etc/neutron/plugins/ml2/linuxbridge_agent.ini 192.168.56.12:/etc/neutron/plugins/ml2/
```
### 设置计算节点的nova.conf
```
[root@linux-node2 ~]# vim /etc/nova/nova.conf
[neutron]
url = http://192.168.56.11:9696
auth_url = http://192.168.56.11:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
```

### 重启计算服务
```
[root@linux-node2 ~]# systemctl restart openstack-nova-compute.service
```
启动计算节点linuxbridge-agent
```
[root@linux-node2 ~]# systemctl enable neutron-linuxbridge-agent.service
[root@linux-node2 ~]# systemctl start neutron-linuxbridge-agent.service
```
### 在控制节点上测试Neutron安装
```
[root@linux-node1 ~]# source admin-openstack.sh
[root@linux-node1 ~]# openstack network agent list
```
看是否有linux-node2.example.com的Linux bridge agent

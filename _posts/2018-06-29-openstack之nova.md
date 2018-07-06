---
layout: post
title:  openstack官网
date:   2018-06-29
categories: document
tag:
  - openstack

---
* content
{:toc}

### 前言

### 介绍

目前的Nova主要由API，Compute，Conductor，Scheduler组成

+ Compute：用来交互并管理虚拟机的生命周期；
+ Scheduler：从可用池中根据各种策略选择最合适的计算节点来创建新的虚拟机；
+ Conductor：为数据库的访问提供统一的接口层。

Compute Service Nova 是 OpenStack 最核心的服务，负责维护和管理云环境的计算资源。
OpenStack 作为 IaaS 的云操作系统，虚拟机生命周期管理也就是通过 Nova 来实现的

Glance 为 VM 提供 image <p>
Cinder 和 Swift 分别为 VM 提供块存储和对象存储 <p>
Neutron 为 VM 提供网络连接<p>

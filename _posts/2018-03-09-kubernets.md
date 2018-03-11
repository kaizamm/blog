---
layout: post
title:  kubernets入门
date:   2018-03-09 01:08:00 +0800
categories: document
tag:
  - k8s

---

* content
{:toc}

### 前言

参考文档 https://www.kubernetes.org.cn/k8s

关于k8s,接触有很长时间了，但一直没有仔细去研究，现在要着手开始准备好好搞搞了。Kubernetes是一个开源的，用于管理云平台中多个主机上的容器化的应用，Kubernetes的目标是让部署容器化的应用简单并且高效（powerful）,Kubernetes提供了应用部署，规划，更新，维护的一种机制。在Kubenetes中，所有的容器均在Pod中运行,一个Pod可以承载一个或者多个相关的容器。在后边的案例中，同一个Pod中的容器会部署在同一个物理机器上并且能够共享资源。一个Pod也可以包含O个或者多个磁盘卷组（volumes）,这些卷组将会以目录的形式提供给一个容器，或者被所有Pod中的容器共享，对于用户创建的每个Pod,系统会自动选择那个健康并且有足够容量的机器，然后创建类似容器的容器,当容器创建失败的时候，容器会被node agent自动的重启,这个node agent叫kubelet,但是，如果是Pod失败或者机器，它不会自动的转移并且启动，除非用户定义了 replication controller。

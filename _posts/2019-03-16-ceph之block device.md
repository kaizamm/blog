---
layout: post
published: true
title:  ceph之block device
categories: [document]
tags: [ceph,存储]
---
* content
{:toc}


### 内核操作rbd

rbd是操作block device的命令行工具

首先创建一个Pool，pgs 64
```
ceph osd pool create cephblock 64
```
然后在这个pool里创建一个映像

```
[root@node2 ceph]# rbd create --size 1024 cephblock/bar
[root@node2 ceph]# rbd ls cephblock
bar
[root@node2 ceph]# rbd info cephblock/bar
rbd image 'bar':
	size 1 GiB in 256 objects
	order 22 (4 MiB objects)
	id: b0236b8b4567
	block_name_prefix: rbd_data.b0236b8b4567
	format: 2
	features: layering, exclusive-lock, object-map, fast-diff, deep-flatten
	op_features:
	flags:
	create_timestamp: Sat Mar 16 05:56:19 2019
[root@node2 ceph]# rbd resize --size 2048 cephblock/bar
Resizing image: 100% complete...done.
[root@node2 ceph]# rbd rm cephblock/bar
Removing image: 100% complete...done.
```

现在来挂载
```
[root@node1 my-cluster]# rbd ls cephblock
bar
[root@node1 my-cluster]# rbd map cephblock/bar
/dev/rbd0
```

取消挂载
```
[root@node1 my-cluster]# rbd device ls
id pool      image snap device
0  cephblock bar   -    /dev/rbd0
[root@node1 my-cluster]# rbd device unmap /dev/rbd0
[root@node1 my-cluster]# rbd device ls
```

<table><tr><td bgcolor=gray>
将ceph.client.admin.keyring拷备到需要挂载的节点/etc/ceph下后，可以直接用ceph命令行工具来访问集群进行操作
</td></tr></table>

### 快照
快照是映像在某个特定时间点的一份只读副本。 Ceph 块设备的一个高级特性就是你可以为映像创建快照来保留其历史。 Ceph 还支持分层快照，让你快速、简便地克隆映像（如 VM 映像）。 Ceph 的快照功能支持 rbd 命令和多种高级接口，包括 QEMU 、 libvirt 、 OpenStack 和 CloudStack 。

<table><tr><td bgcolor=gray>
注意：在做快照时尽量停止IO操作，不然获取不到最新的数据，停止io操作的命令是fsfreeze，[命令的中文man](http://www.mplinux.com/util-linux/fsfreeze8.html)
</td></tr></table>
```
rbd snap rollback/ls/create/protect rbd/foo@snapname
rbd clone ...
```
### 分层
COW 写时复制

Ceph 块设备的分层是个简单的过程。你必须有个映像、必须为它创建快照、并且必须保护快照，执行过这些步骤后，你才能克隆快照

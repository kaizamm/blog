---
layout: post
title:  k8s安装
date:   2018-03-09 01:08:00 +0800
categories: document
tag:
  - k8s

---

* content
{:toc}

### 什么是k8s

[官网](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

k8s是一个便携式、可扩展的开源平台，管理容器负载和服务，配置及自动化。提供了应用部署，规划，更新，维护的一种机制

### 安装docker
### 内核
内核必须支持 memory and swap accounting 。确认你的linux内核开启了如下配置
```bash
 $cat /boot/config-***-generic
 CONFIG_RESOURCE_COUNTERS=y
CONFIG_MEMCG=y
CONFIG_MEMCG_SWAP=y
CONFIG_MEMCG_SWAP_ENABLED=y
CONFIG_MEMCG_KMEM=y
```
以命令行参数方式,在内核启动时开启 memory and swap accounting 选项:
```
GRUB_CMDLINE_LINUX="cgroup_enable=memory	swapaccount=1"
```

```bash
$vim /etc/default/grub
```
修改 GRUB_CMDLINE_LINUX="" ==> GRUB_CMDLINE_LINUX="cgroup_enable=memory"

保存后, 更新grub.cfg
```bash
update-grub
reboot
$cat /proc/cmdline
BOOT_IMAGE=/boot/vmlinuz-3.18.4-aufs root=/dev/sda5 ro cgroup_enable=memory swapaccount=1
```
### 用kubeadm安装k8s
本机环境：ubuntu LTS 1604
```bash
Linux master-node-01 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:23:04 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
```

安装kubeadm
```bash
apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl
```

初始化master
```
kubeadm init
```

在初始化输出后有提示
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

当然如果是root用户还可以设置
```
export KUBECONFIG=/etc/kubernetes/admin.conf
```

继续看，还提示要为cluster部署一个网络pod
```bash
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  http://kubernetes.io/docs/admin/addons/
```

访问提示的网站，可以看到有很多供选择，如 Calico,Canal,Flannel,Kube-router,Romanna,Weave Net


运行 kubeadm apply，选择一个network pod，每个cluster只能选择一种，这里我们选择calico

为了能让Network Policy能够正常工作，在kubeadmin init时需传入'--pod-network-cidr=192.168.0.0/16'。

```
kubectl apply -f https://docs.projectcalico.org/v3.0/getting-started/kubernetes/installation/hosted/kubeadm/1.7/calico.yaml
```

若network已安装成功，可通过检查kube-dns pod是否正常运行

```
kubectl get pods --all-namespaces
```

kube-dns pod运行成功后，就可以继续加入nodes

因为安全原因，默认cluster不会在master节点调度pods，如果你想在master上调度pod，可运行

```
kubectl taint nodes --all node-role.kubernetes.io/master-un
```

再住下看，还有提示加入cluster的信息
```bash
 kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>
```

workloads工作负载包含pods和containers等，nodes是工作负载运行的地方。在每个新node上执行以下步骤可将其加入集群

+ ssh to the machine
+ become root(sudo su -)
+ kubeamin init
```
kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>
```

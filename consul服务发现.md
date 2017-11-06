---
title: consul服务发现
date: 2017.11.3
---
### 什么是consul
+ Consul是个分布式、高可用的系统。此篇只介绍基础功能，深入的请移步[in-depth architecture overview](https://www.consul.io/docs/internals/architecture.html)。
+ 每个向consul提供服务的node节点都是一个consul agent。运行agent并不是为了服务发现或键值存储，而是为了健康检查。consul agent可以与多个consul servers通信。
+ Consul agent就是数据存储和复制的地方。Servers选举出一个leader。官方推荐3至5个。每个Datacenter建议有一个cluster。
+ 需要发现其他服务和节点的组件可以查询任何consul servers和consul agents。agents自动同步查询请求到servers
+ 任何一个datacenter跑一个consul server cluster。当一个跨数据中心服务发现我配置的请求产生，本地的consul servers把这个请求发送到远端数据中心并返回结果。
+ consul有多个组件，但总体来说，主要用于服务发现与配置。

#### 服务发现 Service Discovery
Consul Client能提供service，如api/mysql，其他的Clients能用Consul发现Service的provider。使用DNS或HTTP,application可以很容易找到他们所依赖的service

#### 健康检查 Health Checking
Consult Clients能提供多个健康检查，或者关联一个给定的service(一个返回200的webserver),或是一个本地的node(内存使用低于90%)。这些信息可以被用来当cluster health的指标，同是被service discovery组件在路由时避开不健康的host

#### 键值存储 KV Store
键值存储，可利用HTTP API

#### 多数据中心 Multi Datacenter

### consul的安装
https://www.consul.io/intro/getting-started/install.html
### Run the Consult Agent
当consult已经安装完成后，agent 要跑起来，agent可以以server或clent模式运行。每个dc必须得至少有一个server，建议最好有3至5个server。单个server的部署造成数据的丢失是不可避免的当碰到一个失败的情景时。其他所有的agent以client模式运行。一个client是一个非常经量的进程，用于注册服务、健康检查、和转发查询到servers。agent必须在cluster的每个node节点上运行。
#### Start the Agent
```
[root@node1 ~]# consul agent  -dev
==> Starting Consul agent...
==> Consul agent running!
           Version: 'v1.0.0'
           Node ID: 'd3649a7c-7030-127a-a17b-1600bb7df2a1'
         Node name: 'node1'
        Datacenter: 'dc1' (Segment: '<all>')
            Server: true (Bootstrap: false)
       Client Addr: [127.0.0.1] (HTTP: 8500, HTTPS: -1, DNS: 8600)
      Cluster Addr: 127.0.0.1 (LAN: 8301, WAN: 8302)
           Encrypt: Gossip: false, TLS-Outgoing: false, TLS-Incoming: false

==> Log data will now stream in as it occurs:

    2017/11/03 10:23:56 [DEBUG] Using random ID "d3649a7c-7030-127a-a17b-1600bb7df2a1" as node ID
    2017/11/03 10:23:56 [INFO] raft: Initial configuration (index=1): [{Suffrage:Voter ID:d3649a7c-7030-127a-a17b-1600bb7df2a1 Address:127.0.0.1:8300}]
    2017/11/03 10:23:56 [INFO] raft: Node at 127.0.0.1:8300 [Follower] entering Follower state (Leader: "")

```
正如你所看到的，agent已经运行起来了，并且产生了很多日志，从日志可以看出来，agent以server模式运行，并声明了cluster的leadership。另外本地members都被标记为了cluster的健康成员。
> 注意：consul利用hostname当作默认的node name。如果你的hostname有周期，DNS在查询时会失效。为了避免这个问题，需明确地用 -node 指出该node的name

#### Cluster Members
+ 命令行查询

```
[vagrant@node1 ~]$ consul members
Node   Address         Status  Type    Build  Protocol  DC   Segment
node1  127.0.0.1:8301  alive   server  1.0.0  2         dc1  <all>

```

+ Http API查询

```
[root@node1 ~]# curl localhost:8500/v1/catalog/nodes
[
    {
        "ID": "d3649a7c-7030-127a-a17b-1600bb7df2a1",
        "Node": "node1",
        "Address": "127.0.0.1",
        "Datacenter": "dc1",
        "TaggedAddresses": {
            "lan": "127.0.0.1",
            "wan": "127.0.0.1"
        },
        "Meta": {
            "consul-network-segment": ""
        },
        "CreateIndex": 5,
        "ModifyIndex": 6
    }
]
```

+ DNS API 查询node。注意你需要确保将你的DNS的记录指向默认端口为8600的Consul Agent的DNS服务

```
[root@node1 ~]# dig @127.0.0.1 -p 8600 node1.node.consul

; <<>> DiG 9.9.4-RedHat-9.9.4-51.el7 <<>> @127.0.0.1 -p 8600 node1.node.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47502
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;node1.node.consul.		IN	A

;; ANSWER SECTION:
node1.node.consul.	0	IN	A	127.0.0.1

;; Query time: 0 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Mon Nov 06 02:17:24 GMT 2017
;; MSG SIZE  rcvd: 62
```
#### stopping agent
直接杀死进程后，该node将会被检测到失败，当一个member leave后，它的service和checks会从catalog中移除。当一个member fail时，它的health 仅会被标记为critical，但不会从Catalog中移除。consul会自动尝试去连接failed的nodes，当它恢复正常后，会将其加入到特定的network中。另外，如果一个agents以server的方式运行。强制leave会非常重要目的是为了避免潜在的协议异常。

### Registering Services
上一节讲了运行agent，cluster members的查看，node的查询。这一节我们将注册我们的第一个服务并查询。
#### Defining a Service
register service有两种方式： service defining 和 连接 HTTP API ,service defining是最常用的方式。首先创建一个目录存放consul configuration。Consul从该目录加载所有配置文件。所以一般创建为/etc/consul.d。第二步，写一个service defining configuration文件。假定该服务的name为'web'，端口80.另外，给它一个tag ,我们可以利用它用另外一种方式来查询service。
```
[root@node1 consul.d]# echo '{"service":{"name":"web","tags":["rails"],"port":80}}' | tee /etc/consul.d/web.json
{"service":{"name":"web","tags":["rails"],"port":80}}
```
现在重新运行agent
```
[root@node1 ~]# consul agent -dev -config-dir=/etc/consul.d/
==> Starting Consul agent...
...
2017/11/06 02:43:39 [INFO] agent: Synced service 'web
...
```

#### Quering Service
一旦agent运行和service synce后，我们可以利用DNS & HTTP API来查询该service.
##### DNS API
首先我们利用DNS API来查询service。对于DNS API，该service的DNS name是NAME.service.consul。默认所有的DNS names就是该Consul的命名空间，尽管该项是可配置的。Service的子域告诉了consul我们要查询service。该NAME就是该service的名字。
```
[root@node1 consul.d]# dig @127.0.0.1 -p 8600 web.service.consul
...
;; QUESTION SECTION:
;web.service.consul.		IN	A
;; ANSWER SECTION:
web.service.consul.	0	IN	A	127.0.0.1
...
```
另，你可以得用DNS API去检索Address/Port对当成SRV记录
```
dig @127.0.0.1 -p 8600 web.service.consul SRV
...
;; QUESTION SECTION:
;web.service.consul.		IN	SRV

;; ANSWER SECTION:
web.service.consul.	0	IN	SRV	1 1 80 node1.node.dc1.consul.

;; ADDITIONAL SECTION:
node1.node.dc1.consul.	0	IN	A	127.0.0.1
node1.node.dc1.consul.	0	IN	TXT	"consul-network-segment="
...
```
最后我们也可以通过DNS API利用tags去过滤services
##### HTTP API
查询所有的node
```
$ curl http://localhost:8500/v1/catalog/service/web
```
查询通过健康检查的实例
```
$ curl 'http://localhost:8500/v1/health/service/web?passing'
```

### Consul Cluster
当一个agent启动后，它是个孤立的。为了与其他members联系起来，需将其加入到一个clusert中。加入到一个存在的Cluster，只需要知道一个单独存在的members就行。加入后，该agent与其member会建立联系并一起discovery 该cluster中的其他members。在我们的上面例子中，，我们用-dev参数快速的启动了一个development server。然而，在cluster环境中并不适用。我们将省略该参数并指定我们的clustering flags。每个cluster中的node需有一个惟一的name。默认，使用hostname，但我们需要手动指定，利用 -node command-line option。我们同样要指定bind address。这个地址是Consul监听的地址，它同时需要让其他node能访问。尽管bind address不是严格必要，但最好还是提供一个。Consul默认监听系统中所有的IPV4接口，但如果发现有多个ipv4接口，则会启动报错。第一个node我们让其成为server,需用server switch指明它。"-bootstrap-expect"参数向Consul Server指明其他的我们希望加入的node的数量。"-enable_script_checks"参数用额外的script去health check。"config-dir" 参数指定配置目录。
```
consul agent -server -bootstrap-expect=1 -data-dir=/tmp/consul -node=agent-one -bind=192.168.0.11 -enable-script-checks=true -config-dir=/etc/consul.d

[root@node2 consul.d]# consul agent -data-dir=/tmp/consul -node=agent-two -bind=192.168.0.12 -enable-script-checks=true -config-dir=/etc/consul.d

```
现在启动了两个agent，一个server，一个client，相互独立，现在把client和server加入到一个cluster中来
```
[root@node1 ~]# consul join 192.168.0.12
Successfully joined cluster by contacting 1 nodes.
[vagrant@node2 ~]$ consul members
Node       Address            Status  Type    Build  Protocol  DC   Segment
agent-one  192.168.0.11:8301  alive   server  1.0.0  2         dc1  <all>
agent-two  192.168.0.12:8301  alive   client  1.0.0  2         dc1  <default>
```

#### Health Checks
同service一样，check有两种方式，一个是check defining,另一个是通过http api创建合适的请求
```
[root@node2 vagrant]#  echo '{"check":{"name":"ping","script":"ping -c1 www.baidu.com>/dev/null","interval":"30s"}}' > /etc/consul.d/ping.json

[root@node2 vagrant]#  echo '{"service": {"name": "web", "tags": ["rails"], "port": 80,"check": {"script": "curl localhost >/dev/null 2>&1", "interval": "10s"}}}'>/etc/consul.d/web.json
```
上面的一个defining增加了一个check名字为ping。30s种检测，如：ping -c1 www.baidu.com；第二个改变了web service加入了一个check，每10s发送一个请求。
```
[root@node2 consul.d]# consul agent -data-dir=/tmp/consul -node=agent-two -bind=192.168.0.12 -enable-script-checks=true -config-dir=/etc/consul.d
==> Starting Consul agent...
...
2017/11/06 04:16:47 [WARN] agent: Check 'service:web' is now critical
...
```
最下面一行提示curl test失败，原因为没有运行web server

#### Check Health Status
现在我们可以加入一些简单的checks，我们可以用HTTP API去检查他们。首先我们可以通过command去查找falling checks。这个可以在任何一个node上运行。
```
vagrant@n1:~$ curl http://localhost:8500/v1/health/state/critical
[{"Node":"agent-two","CheckID":"service:web","Name":"Service 'web' check","Status":"critical","Notes":"","ServiceID":"web","ServiceName":"web"}]
```
另外我们可以通过DNS查询web service。如果所有的servcie都不是unhealthy,那么Consul不会返回任何结果。
```
dig @127.0.0.1 -p 8600 web.service.consul
...

;; QUESTION SECTION:
;web.service.consul.        IN  A
```
### KV DATA
除了service discovery和helth checking，Consul可以提供KV存储。
```
$ consul kv get redis/config/minconns
Error! No key exists at: redis/config/minconns.

$ consul kv put redis/config/minconns 1
Success! Data written to: redis/config/minconns

$ consul kv put redis/config/maxconns 25
Success! Data written to: redis/config/maxconns

$ consul kv get redis/config/minconns

$ consul kv get -detailed redis/config/minconns
```

### Consul Web UI
Consul提供一个UI。UI可以用于浏览所有的service和nodes，以及读写key/value数据，支持multi-datacenter
```
$ consul agent -ui
```

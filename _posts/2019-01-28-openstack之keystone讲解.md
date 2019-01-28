---
layout: post
published: true
title:  openstack之keystone讲解
categories: [document,blog]
tags: [openstack,私有云]
---
* content
{:toc}

## 前言
Keystone是openstack的服务，通过identify API提供API客户端认证，服务发现，和分布式多租户认证  
官网 https://docs.openstack.org/keystone/latest/getting-started/architecture.html
## Services
通过暴露服务的endpoints，让user/project认证，成功后通过Token service创建并返回token

### Idenify
通过LDAP来做CRUD操作

#### Users  
usrs并不是全局惟一的，它只是在在其domain下惟一

#### Groups  
它是多个user的集合，与users一样，只在其domain下惟一

### Resource
提供projects和domains的数据

#### projects
只在其domain下惟一，若不指定其doain，则默认为 **Default**

#### domains
它是Projects/users/groups的一个容器，通过namespace隔离，默认为Default，domain name全局惟一，通过assginment可以让User在不同的domain下访问数据

### Assignment
提供role和 role Assignments的数据

#### Roles
定义user的认证级别，roles可以授权到doamin级别，也可以授权到project级别；一个role要绑定一个独立的user或是一个组;
#### Role Assignments
它是个元组包含三个元素[Role,Resource,Identify]

### Token
通过Token service提供，访问令牌

### Catalog
通过Catalog sevice为endpint discovery 提供endpoint registry

## Application Construction
keystone对其它的服务而言一个HTTP的Frontend；跟其它应用一样，通过python的WSGI动态网关接口；应用的HTTP endpoint通过WSGI的pipeline组装而成，如：
```bash
[pipeline:api_v3]
pipeline = healthcheck cors sizelimit http_proxy_to_wsgi osprofiler url_normalize request_id build_auth_context json_body ec2_extension_v3 s3_extension service_v3
```

## Data Model
+ User  
+ Group  
+ Project  
+ Domain  
+ Role  
+ Token  
+ Extra  
+ Rule  

## Policy
在每个服务的对应的配置目录，如![/etc/keystone/policy.json](/styles/images/keystone1.jpg)  
具体对应的每个API的policy，参考[点我](https://docs.openstack.org/keystone/latest/getting-started/policy_mapping.html)

## Plugins
+ keystone.auth.plugins.external.Base  
+ keystone.auth.plugins.mapped.Mapped  
+ keystone.auth.plugins.oauth1.OAuth  
+ keystone.auth.plugins.password.Password  
+ keystone.auth.plugins.token.Token  
+ keystone.auth.plugins.totp.TOTP  

通过curl获取数据，如：token
```bash
curl -i \
  -H "Content-Type: application/json" \
  -d '
{ "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "admin",
          "domain": { "id": "default" },
          "password": “Fiberhome.2019"
        }
      }
    },
    "scope": {
      "project": {
        "name": “admin",
        "domain": { "id": "default" }
      }
    }
  }
}' \
  "https://10.190.48.204:5000/v3/auth/tokens” -k
```  

拿到token后，就可以获取项目上的数据了，如获取虚机   
```bash
token=37a9799a28f94d5498737cf0018107f8
project_id=6f12225f5fc946c7bae62646fff5dfb2
url="https://10.190.48.204:8774/v2.1/$project_id/servers"
curl -s -H "X-Auth-Token:$token" $url -k |python -m json.tool
```

## keystone package
Keystone的安装包对应的[代码模块](https://docs.openstack.org/keystone/latest/api/keystone.assignment.backends.base.html)

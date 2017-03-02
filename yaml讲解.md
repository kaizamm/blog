---
title: yaml讲解
date: 2017.3.2
---
### yaml是一种通用的串行化数据格式，规则如下：

+ 大小写敏感
+ 使用缩进表示层级关系
+ 缩进时不允许使用TAB键，只允许使用空格
+ 缩进的空格数目不重要，只要相同的层级的元素左侧对齐即可
+ "#"表示注释

### 数据格式

+ 对象：键值对的集合，又称映射（mapping）/哈希（hashes）/字典（dictionary）
+ 数组： 一组按次序排列的值，又称为序列（sequence）/列表（list）
+ 纯量（scalars)：单个的、不可再分的值

#### 对象
+ 对象的一组键值对，使用冒号结构表示 `animal：pets `
+ 转化为javascript为 `{animal: 'pets'}`
+ yaml允许另一种写法，将所有的键值对写成一个行内对象 `hash: { name:steven, foo: bar }`
+ 转化为javascript为 `{ hash: { name: 'steven', foo: 'bar' } } `

#### 数组
+ 一组连词开头的行，构成一个数组
```
- cat
- dog
- goldfish
```
+ 转化为javascript为 `{[ 'cat','dog','goldfish' ]}`
+ 数组也可以采用行内表示法 ` [ 'cat','dog' ] `

#### 复合结构
对象和数组结合使用，形成复合结构
```
languages:
  - Ruby
  - Perl
  - Python
  - Php
websites:
  YAML: yaml.org
  Ruby: ruby-lang.org
  Pyhon: python.org
  perl: use.per.org
```
转化为javascript为：
```
{ languages: [ 'Ruby', 'Perl', 'Python', 'Php' ],
  websites:
  {YAML: 'yaml.org',
   Ruby: 'ruby-lang.or',
   Python: 'python.org',
   perl: 'use.per.org'}}
```

#### 纯量
纯量是最基本的、不可再分的值。以下数据类型都属于javascript的纯量
+ 字符串
+ 布尔值
+ 整数
+ 浮点数
+ Null
+ 时间
+ 日期

##### 举例
+ 数值直接以字面量的形式表示: `number: 12.3`
+ 转化为javascript为： `{ number: 12.3}`
+ 布尔值用true和false表示   `isSet: true`
+ 转化为javascript: `{isSet: true}`
+ 日期：`date: 2017-03-02`

#### 字符串
字符串是最常见的，也是最复杂的一种数据类型
+ 字符串默认不使用引号表示 `str: 这是一行字符串`
+ 转化为javascript为`{str: '这是一行字符串'}`；
+ 若字符串中有空格或特殊字符，需要放在引号之中。
`str: '内容： 字符串'`，转化为javascript为{str: '内容： 字符串'}
+ 单引号和双引号都可以用，双引号不会对特殊字符转义
```
s1: '内容\n字符串'
s2: "内容\n字符串"
转化为javascript为
{ s1: '内容\\n字符串'，s2: '内容\n字符串' }
```
### 引用
锚点&和别名*

### 函数和正则

http://www.ruanyifeng.com/blog/2016/07/yaml.html

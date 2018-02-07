---
title: python迭代器与可迭代
date: 2016.12.6
---

### 1.定义
Iterators:一种遍历的容器对象
Iteration:可以通过 for ... in 循环来遍历一个字符串、列表、元组或字典等，这种遍历称为迭代。
### 2.应用说明及应用场景
a.字符串的迭代
```
>>> a = "asdfjl"
>>> for i in a:
...   print i
...
a
s
d
f
j
l
```
b.列表的迭代
```
>>> a = ['aba',123]
>>> for i in a:
...   print i
...
aba
123
```
c.元组的迭代
```
>>> for i in a:
...   print i
...
z
k
c
```
d.字典的迭代
```
>>> a = {'name':'kaiz','age':26,'sex':'M'}
>>> for i in a:
...   print i
...
age
name
sex
```
说明：字典的迭代只能打印出key值，若要打印value，如下：
```
>>> a = {'name':'kaiz','age':26,'sex':'M'}
>>> for i in a.itervalues():
...   print i
...
26
kaiz
M
```
若要打印key及value，如下:
```
>>> a = {'name':'kaiz','age':26,'sex':'M'}
>>> for key,value in a.iteritems():
...   print key,value
...
age 26
name kaiz
sex M
```
说明:当我们使用for循环时，只要作用于一个可迭代的对象，for循环就可以正常运行，而我们不太关心该对象是字符串、列表、元组、字典还是其他数据类型。那么如何判断一个对象是可迭代对象呢？方法是通过collections模块的Iterable类型判断，如：
```
>>> from collections import Iterable
>>> isinstance('abc',Iterable) #str是否可迭代
True
>>> isinstance([1,2,3],Iterable) #list是否可迭代
True
>>> isinstance(121,Iterable)#整数是否可迭代
```
如何创建迭代器？
对一个对象调用 iter() 就可以得到它的迭代器。如果你传递一个参数给 iter() , 它会检查你传递的是不是一个序列, 如果是, 那么很简单: 根据索引从 0 一直迭代到序列结束. 另一个创建迭代器的方法是使用类。
关于迭代器Iterators,有两个基本方法：
1）next方法：返回容器的下一个元素
2）__iter__方法：返回迭代器本身，可使用内建的iter方法创建，如：
```
>>> a = iter('abc')#注意需要用iter()函数来创建迭代器
>>> a.next()
'a'
>>> a.next()
'b'
>>> a.next()
'c'
>>> a.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```
>>>

### 3.特点
迭代只能向前不能向后，只到异常
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

---
layout:       post
title:        "python-Build-in-Functions"
date:         2017-08-16 12:00:00
categories: document
tag: python
---

* content
{:toc}

### Build-in Functions
参考 https://docs.python.org/3/library/functions.html#exec


| Build-in    | *         |*             |*           |*                   |
| ------------|-----------|--------------|------------|--------------------|
|   abs()     |dict()     |help()        |min()       |setattr()           |
|   all()	    |dir()	    |hex()         |	next()    |	slice()            |
|   any()     |divmod()   |	id()         |	object()	|sorted()            |
|   ascii()   |enumerate()|	input()	     |oct()       |	staticmethod()     |
|   bin()     |eval()     |	int()        |	open()    |	str()              |
|   bool()    |	exec()    |isinstance()	 |ord()	      |sum()               |
|  bytearray()|filter()	  |issubclass()	 |pow()       |	super()            |
|  bytes()	  |float()	  |iter()        |	print()   |	tuple()            |
|  callable() |	format()	|len()	       |property()	|type()              |
|  chr()	    |frozenset()|list()        |	range()   |	vars()             |
|classmethod()|getattr()  |	locals()	   |repr()	    |zip()               |
|  compile()	|globals()	|map()	       |reversed()	|*\__import\__()*    |         |
|  complex()	|hasattr()  |	max()        |	round()	  |set()               |
|  delattr()	|hash()	    |memoryview()

重点
+ all()
```
all(iterable)
Return True if all elements of the iterable are true (or if the iterable is empty). Equivalent to:

def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True
```
+ any()
+ \__import\__
+ eval()
```
>>> x = 1
>>> eval('x+1')
2
```
+ zip()
```
>>> x = [1, 2, 3]
>>> y = [4, 5, 6]
>>> zipped = zip(x, y)
>>> list(zipped)
[(1, 4), (2, 5), (3, 6)]
>>> x2, y2 = zip(*zip(x, y))
>>> x == list(x2) and y == list(y2)
True
```
+ map(function,iterable)
+ filter(function,iterable)
相当于
```
(item for item in iterable if function(item)) if function is not None and (item for item in iterable if item) if function is None.
```
+ enumerate()
对可迭代对象进行操作，加上index
```
In [26]: iter = ['coffee','tea','sugar']

In [27]: for i,text in enumerate(iter):
   ....:     print i,text
   ....:     
0 coffee
1 tea
2 sugar
```
+ lambda()
+ getattr()
+ chr()
+ ord()

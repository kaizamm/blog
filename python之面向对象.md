---
title: python之面向对象
date: 2017.7.21
---
### 概述
+ 面向过程：根据业务逻辑从上到下写垒代码
+ 函数式： 将某功能代码封装到函数中，日后便无需重复编写，仅调用函数即可
+ 面向对象： 对函数进行分类和封装，让开发“更快更好更强”
### 创建类和对象
面向对象其实就是对类和对象的使用，类就是一个模版，模版里包含多个函数，函数里实现一些功能；对象则是根据模版创建实例，通过实例对象可以执行类中的函数。
```
#创建类
class Foo:
  #创建类中的函数
  def Bar(self):
    #do something

#根据类Foo创建对象obj
obj = Foo()
```
### 面向对象的三大特性
#### 封装
封装故名思义就是将内容封装到某个地方，以后再去调用被封装在某处的内容。所以在使用面向对象的封装特性时，需要：
##### 将内容封装到某处
```
class Foo:
  def __init__(self,name,age):
    self.name = name
    self.age = age

#根据类Foo创建对象
#创建对象时，会自动执行类的__init__方法
obj1 = Foo('kaiz',18)
obj2 = Foo('amm',28)
#如上，即是将kaiz,18分别封装到obj1/self的name和age属性中
#self是一个形式参数，当执行obj1 = Foo('kaiz',18)时，self等于obj1
```
##### 从某处调用被封装的内容
调用被封装的内容时，有两种情况：
###### 通过对象直接调用
```
class Foo:
  def __init__(slef,name,age):
    self.name = name
    self.age = age
obj1 =Foo('kaiz',18)
print obj1.name
print obj1.age
```
###### 通过self间接调用
```
class Foo:
  def __init__(slef,name,age):
    self.name = name
    self.age = age

  def detail(self):
    print self.name
    print self.age
```

### 继承
继承，子类继承父类（派生类继承基类）
```
class Father:
  def __init__(self,name,age):
    self.name = name
    self.age = age

  def bad_hobby:
    print "smoke,drink"

class Son(Father):
  def __init__(self,name,age):
    self.name = name
    self.age = age
#创建Son类的对象
obj = Son('amm',18)
#由于是继承，因此obj具由Father类的方法
obj.bad_hobby
> smoke,drink
```

同时继承后，子类可以改良父类的方法。另：类分经典类和新式类，如果父类继承了object类，那么该类就是新式类，否则便是经典类。在多继承中，当类是经典类时，会按照深度优先方式查找；当类是新式类时，会按照广度优先试查找。
```
#多继承
class A(B,C)
```

### 多态
```
class F1:
    pass


class S1(F1):

    def show(self):
        print 'S1.show'


class S2(F1):

    def show(self):
        print 'S2.show'

def Func(obj):
    print obj.show()

s1_obj = S1()
Func(s1_obj)

s2_obj = S2()
Func(s2_obj) 
```























### 概述
ADT abstract data type 抽象数据类型，设计者在考虑一个程序部件时，首先给出一上清晰边界，通过一套接口描述说明这一种功能，如果适合实际需要，就通过接口使用，并不需要其具体实现细节。抽象数据类型的基本想法是把数据定义为抽象的对象集合，只为他们定义合法的数据操作。抽象数据类型提供的操作应该满足这些要求。
+ 构造操作： 这类操作基于一些已知的信息，产生出这种类型的一个新对象。
+ 解析操作： 这种操作从一个对象取得有用的信息
+ 变动操作： 这类操作修改被操作的对象内部状态。


### isinstance()
python提供了内置函数isinstance，专门用于检查类和对象的关系。表达式isinstance(obj，cls)检查对象obj是否为类cls的实例,当obj的类是cls时得到True，否则得到False。实际上，isinstance可以用于检测任何对象与任何类型的关系，如检查一个变量或参数的值是否为int类型或float类型等。
### 静态方法和类方法
+ 静态方法，定义的形式就是def行前加修饰符@staticmethod，静态方法实际上就是普通函数，只是由于某种原因需要定义在类里面。
+ 类方法，定义形式是在def行前加修饰符@classmethod这种方法必须有一个表示其调用类的参数，习惯用cls作为参数名，还可以有任意多个其他参数。类方法也是类对象的属性，可以以属性的形式调用。在类方法执行时调用它的类将自动约束到方法的cls参数，可以通过这个参数访问该类的其他属性。

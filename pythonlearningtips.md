---
title: pythonlearningtips
---
### 1.python中print与return的区别
*return是返回值的意思，print是个过程，打印出变量的值，举例说明：*
```
def function1(x,y):
  return x+y
result1 = function1(1,2)
print result1
->3

def function2(x,y):
  print x+y
result2 = function2(1,2)
print result2
->none
```
### 2.函数

在python中，函数通过def关键字、函数名和可选的参数列表定义。通过return关键字返回值。我们举例来说明如何定义和调用一个简单的函数：
```
def foo():
     return 1
foo()
->1
```
方法体（当然多行也是一样的）是必须的，通过缩进来表示，在方法名的后面加上双括号()就能够调用函数

### 3.函数也是类对象,'()'只是调用函数的操作，函数的名称只是很其他变量一样的表标识符而已
 ```
 def add(x, y):
     return x + y
def sub(x, y):
     return x - y
def apply(func, x, y): # 1
     return func(x, y) # 2
apply(add, 2, 1) # 3
->3
apply(sub, 2, 1)
->1
```
add和sub是非常普通的两个python函数，接受两个值，返回一个计算后的结果值。在#1处你们能看到准备接收一个函数的变量只是一个普通的变量而已，和其他变量一样。在#2处我们调用传进来的函数'()'代表着调用的操作并且调用变量包含的值。在#3处，你们也能看到传递函数并没有什么特殊的语法。” 函数的名称只是很其他变量一样的表标识符而已

### 4.装饰器
1.装饰器其实就是一个闭包，把一个函数当做参数然后返回一个替代版函数。我们一步步从简到繁来瞅瞅：
```
def outer(some_func):
     def inner():
         print "before some_func"
         ret = some_func() # 1
         return ret + 1
     return inner
def foo():
     return 1
decorated = outer(foo) # 2
decorated()
before some_func
2
```
2.仔细看看上面这个装饰器的例子。们定义了一个函数outer，它只有一个some_func的参数，在他里面我们定义了一个嵌套的函数inner。inner会打印一串字符串，然后调用some_func，在#1处得到它的返回值。在outer每次调用的时候some_func的值可能会不一样，但是不管some_func的之如何，我们都会调用它。最后，inner返回some_func() + 1的值 – 我们通过调用在#2处存储在变量decorated里面的函数能够看到被打印出来的字符串以及返回值2，而不是期望中调用函数foo得到的返回值1。

我们可以认为变量decorated是函数foo的一个装饰版本，一个加强版本。事实上如果打算写一个有用的装饰器的话，我们可能会想愿意用装饰版本完全取代原先的函数foo，这样我们总是会得到我们的”加强版“foo。想要达到这个效果，完全不需要学习新的语法，简单地赋值给变量foo就行了
```
foo = outer(foo)
foo # doctest: +ELLIPSIS
<function inner at 0x>
```
现在，任何怎么调用都不会牵扯到原先的函数foo，都会得到新的装饰版本的foo，现在我们还是来写一个有用的装饰器。

想象我们有一个库，这个库能够提供类似坐标的对象，也许它们仅仅是一些x和y的坐标对。不过可惜的是这些坐标对象不支持数学运算符，而且我们也不能对源代码进行修改，因此也就不能直接加入运算符的支持。我们将会做一系列的数学运算，所以我们想要能够对两个坐标对象进行合适加减运算的函数，这些方法很容易就能写出：
```
class Coordinate(object):
     def __init__(self, x, y):
         self.x = x
         self.y = y
     def __repr__(self):
         return "Coord: " + str(self.__dict__)
def add(a, b):
     return Coordinate(a.x + b.x, a.y + b.y)
def sub(a, b):
     return Coordinate(a.x - b.x, a.y - b.y)
one = Coordinate(100, 200)
two = Coordinate(300, 200)
add(one, two)
Coord: {'y': 400, 'x': 400}
```
如果不巧我们的加减函数同时也需要一些边界检查的行为那该怎么办呢？搞不好你只能够对正的坐标对象进行加减操作，任何返回的值也都应该是正的坐标。所以现在的期望是这样：
```
one = Coordinate(100, 200)
two = Coordinate(300, 200)
three = Coordinate(-100, -100)
sub(one, two)
Coord: {'y': 0, 'x': -200}
add(one, three)
Coord: {'y': 100, 'x': 0}
```
我们期望在不更改坐标对象one, two, three的前提下one减去two的值是{x: 0, y: 0}，one加上three的值是{x: 100, y: 200}。与其给每个方法都加上参数和返回值边界检查的逻辑，我们来写一个边界检查的装饰器！
```
def wrapper(func):
     def checker(a, b): # 1
         if a.x < 0 or a.y < 0:
             a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
         if b.x < 0 or b.y < 0:
             b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
         ret = func(a, b)
         if ret.x < 0 or ret.y < 0:
             ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
         return ret
     return checker
add = wrapper(add)
sub = wrapper(sub)
sub(one, two)
Coord: {'y': 0, 'x': 0}
add(one, three)
Coord: {'y': 200, 'x': 100}
```
### 4.使用 @ 标识符将装饰器应用到函数
使用标识符@将装饰器应用在函数上，只需要在函数的定义前加上@和装饰器的名称。在上一节的例子里我们是将原本的方法用装饰后的方法代替:
```
add = wrapper(add)
```
这种方式能够在任何时候对任意方法进行包装。但是如果我们自定义一个方法，我们可以使用@进行装饰：
```
@wrapper
 def add(a, b):
     return Coordinate(a.x + b.x, a.y + b.y)
```
需要明白的是，这样的做法和先前简单的用包装方法替代原有方法是一毛一样的， python只是加了一些语法糖让装饰的行为更加的直接明确和优雅一点

### 5.*args and **kwargs

我们已经完成了一个有用的装饰器，但是由于硬编码的原因它只能应用在一类具体的方法上，这类方法接收两个参数，传递给闭包捕获的函数。如果我们想实现一个能够应用在任何方法上的装饰器要怎么做呢？再比如，如果我们要实现一个能应用在任何方法上的类似于计数器的装饰器，不需要改变原有方法的任何逻辑。这意味着装饰器能够接受拥有任何签名的函数作为自己的被装饰方法，同时能够用传递给它的参数对被装饰的方法进行调用。

非常巧合的是Python正好有支持这个特性的语法。可以阅读 Python Tutorial 获取更多的细节。当定义函数的时候使用了*，意味着那些通过位置传递的参数将会被放在带有*前缀的变量中， 所以：

```

2
3
4
5
6
7
8
9
10
def one(*args):
     print args # 1
one()
()
one(1, 2, 3)
(1, 2, 3)
def two(x, y, *args): # 2
     print x, y, args
two('a', 'b', 'c')
a b ('c',)
```
第一个函数one只是简单地讲任何传递过来的位置参数全部打印出来而已，你们能够看到，在代码#1处我们只是引用了函数内的变量args, *args仅仅只是用在函数定义的时候用来表示位置参数应该存储在变量args里面。Python允许我们制定一些参数并且通过args捕获其他所有剩余的未被捕捉的位置参数，就像#2处所示的那样。
*操作符在函数被调用的时候也能使用。意义基本是一样的。当调用一个函数的时候，一个用*标志的变量意思是变量里面的内容需要被提取出来然后当做位置参数被使用。同样的，来看个例子：
```
def add(x, y):
     return x + y
lst = [1,2]
add(lst[0], lst[1]) # 1
3
add(*lst) # 2
3
```
#1处的代码和#2处的代码所做的事情其实是一样的，在#2处，python为我们所做的事其实也可以手动完成。这也不是什么坏事，*args要么是表示调用方法大的时候额外的参数可以从一个可迭代列表中取得，要么就是定义方法的时候标志这个方法能够接受任意的位置参数。
接下来提到的**会稍多更复杂一点，**代表着键值对的餐宿字典，和*所代表的意义相差无几，也很简单对不对：
```
def foo(**kwargs):
     print kwargs
foo()
{}
foo(x=1, y=2)
{'y': 2, 'x': 1}
1
2
3
4
5
6
def foo(**kwargs):
     print kwargs
foo()
{}
foo(x=1, y=2)
{'y': 2, 'x': 1}
```
当我们定义一个函数的时候，我们能够用**kwargs来表明，所有未被捕获的关键字参数都应该存储在kwargs的字典中。如前所诉，argshe kwargs并不是python语法的一部分，但在定义函数的时候，使用这样的变量名算是一个不成文的约定。和*一样，我们同样可以在定义或者调用函数的时候使用**。

```

dct = {'x': 1, 'y': 2}
def bar(x, y):
     return x + y
bar(**dct)
3
1
2
3
4
5
dct = {'x': 1, 'y': 2}
def bar(x, y):
     return x + y
bar(**dct)
3
```

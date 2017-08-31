---
title: Flask_Web开发
date: 2017.8.28
tag: python
---
## 程序基本结构
### 环境准备
官网  http://flask.pocoo.org/；实验环境python-virtualenv，安装 sudo yum install python-virtualenv 即可。用这个环境的好处，可在系统的python解释器中避免包的混乱和版本的冲突，为每个程序单独创建虚拟环境可以保证程序只能访问虚拟环境中的包，从而保持全局解释器的干净整洁，并且虚拟环境中不需要管理员权限。一旦安装完成，virtualenv实用工具就可以从常规账户中调用。
```
sudo yum install python-virtualenv
git clone https://github.com/miguelgrinberg/flasky.git
cd flasky/
git checkout 1a
virtualenv venv
source venv/bin/activate #启动
deactivate #退回全局
pip install flask
#查看一下flask的安装位置
In [3]: import sys
In [4]: sys.modules['flask']
Out[4]: <module 'flask' from '/tmp/flasky/venv/lib/python2.7/site-packages/flask/__init__.pyc'>
```
### 初始化
所有的Flask程序都需创建一个程序实例，web服务器使用一种名为web服务网关接口WSGI的协议，把接收自客户端的所有请求都转交给这个对象处理。程序实例是Flask类的对象，使用下面的代码创建
```
from flask import Flask
app = Flask(__name__)  #Flask类的构造函数只有一个必须指定的参数，即程序的主模块或包的名字，在大多数程序中，Python的__name__变量就是所需的值，Flask用这个参数决定程序的根目录，以便稍后稍后能够找到相对于程序根目录的资源文件位置。
```

### 一个完整的程序
```
#cat hello.py
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')  #name 为变量
def user(name):
  return '<h1>hello,%s!<h1>' % name

if __name__ == '__main__':
    app.run(debug=True)

#python hello.py运行进来后访问

[root@node1 ~]# curl http://localhost:5000
<h1>Hello World!</h1>
[root@node1 ~]# curl http://localhost:5000/user/kaiz
<h1>hello,kaiz!<h1>
```
### 程序和请求上下文
在Flask中有两种上下文：程序上下文和请求上下文，如下：

变量名       |上下文     |说明
---|---
current_app  |程序上下文 |当前激活的程序实例
g            |程序上下文 |处理请求时用作临时存储的对象，每次请求都会重设这个变量
request      |请求上下文 |请求对象，封装了客户端发出的HTTP请求中的内容
session      |请求上下文 |用户会话，用于存储请求之间需要“记住”的值的词典

Flask在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除，程序上下文被推送后，就可以在线程中使用current_app和g变量。类似地，请求上下文被推送后，就可以使用request和session变量。如果使用这些变量时我们没有激活程序上下文或请求上下文，就会导致报错。
```
In [1]: from hello import app
In [2]: from flask import current_app
In [3]: current_app.name  #在没有激活程序上下文之前就调用current_app.name会导致报错，但推送上下文之后就可以调用了
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
RuntimeError: Working outside of application context.
In [4]: app_ctx = app.app_context()  #注意：在程序实例上调用app.app_context()可获得一个程序上下文。
In [5]: app_ctx.push()
In [6]: current_app.name
Out[6]: 'hello'
In [7]: app_ctx.p
app_ctx.pop   app_ctx.push  
In [7]: app_ctx.pop()
```
### 请求调度
程序收到客户发来的请求后，要找到处理该请求的视图函数，为了完成这个任务，Flask会在程序的URL映射中查找请求的URL。URL映射是URL和视图函数之间的对应关系。Flask使用app.route修饰器或者非修饰器形式的app.add_url_rule()生成映射。要想查看Flask程序中URL映射是什么样子，可以在shell中检查hello.py生成的映射
```
#cat hello.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
  return '<h1>hello,%s!<h1>' % name

if __name__ == '__main__':
    app.run(debug=True)

In [1]: from hello import app
In [3]: app.url_map
Out[3]:
    Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
     <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
     <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```
/和/user/<name>路由在程序中使用app.route修饰器定义。/static/<filename>路由是Flask添加的特殊路由，用于访问静态文件。URL中的HEAD/OPTIONS/GET是请求方法，由路由进行处理。Flask为每个路由都指定了请求方法，这样不同的请求方法发送到相同的URL上时，会使用不同的视图函数进行处理。HEAD和OPTIONS方法由Flask自动处理，因此可以这么说，在这个程序中，URL映射中的3个路由都使用GET方法。
### 请求钩子
在请求之前或之后执行代码
### 响应
Flask调用视图函数后，会将基返回值作为响应的内容。大多数情况下，响应就是一个简单的字符串，作为HTML页面回送客户端。但HTTP协议需要的不仅是作为请求响应的字符串。HTTP响应中一个很重要的部份是状态码，Flask默认设为200，这个代码表明请求已经被成功处理。如果视图函数返回的响应需要使用不同的状态码，那么可以把数字代码作为第二个返回值，添加到响应文本之后，例如，下述视图函数返回一个400状态码，表示请求无效。
```
@app.route('/')
def index():
  return '<h1>Bad Request</h1>',400
```
视图返回的响应还可以接受第三个参数，这是一个由首部(header)组成的字典，可以添加到HTTP响应中。一般情况下并不需要这么做。如果不想返回由1个、2个或3个值组成的元组，Flask视图函数还可以返回Response对象。make_response()函数可接受1个、2个、3个参数（和视图函数的返回值一样），并返回一个Response对象。有时我们需要在视图函数中进行这种转换，然后在响应对象上调用各种方法，进一步设置响应。下例创建了一个响应对象，然后设置了cookie:
```
from flask import make_response
@app.route('/')
def index():
  response = make_response('<h1>This document carries a cookie!</h1>')
  response.set_cookie('answer','42')
  return response
```
有一种名为重定向的特殊响应类型。这种响应没有页面文档，只告诉浏览器一个新地址用以加载新页面。重定向经常在Web表单中使用。重定向常使用302状态码表示，指向的地址由Location首部提供。重定向响应可以使用3个值开式的返回值生成，也可在Response对象中设定。不过，由于使用频繁，Flask提供了redirect()辅助函数，用于生成这种响应。
```
from flask import redirect
@app.route('/')
def index():
  return redirect('http://www.example.com')
```
还有一种特殊的响应由abort函数生成，用于处理错误。
```
from flask import abort
@app.route('/user/<id>')
def get_user(id):
  user = load_user(id)
  if not user:
    abort(404)
  return '<h1>hello,%s</h1>' % user.name
```
### Flask扩展 flask-script
flask-script是Flask扩展，为Flask添加一个命令行解释器
```
pip install flask-script
#cat hello.py
from flask.ext.script import Manager
manager = Manager(app)
#...
if __name__ == "__main__":
  manager.run()
```
专为Flask开发的扩展都开暴露在flask.ext命名空间下。flask-script输出了一个名为Manager的类，可从flask.ext.script中引入。
```
#python hello.py
usage: hello.py [-h]{shell,runserver}...
```

## 模版
模版是一个包含响应文本的文体，其中包含用占位变量表示的动态部份，基具体值只在请求的上下文中才能知道，使用真实值替换变量，再返回最科得到的响应字符串，这一过程称为渲染。为了渲染模版，Flask使用jinja2。
### jinja2变量过滤器
可以使用过滤器修改变量，过滤器名添加在变量后之后，中间使用竖线分隔。如下
```
hello,{{ name|capitalize }}
```
过滤器名| 说明
---|---
safe | 渲染值时不转义
capitalize| 把值的首字母转换成大写，基他字母转换成小写
lower| 把值转换成小写形式
upper| 把值转换成大写形式
title| 把值中每个单词的首字母都转换成大写
trim| 把值的首尾空格去掉
striptags|渲染之前把值中所有的HTML标签都删掉

详见http://jinja.pocoo.org/docs/2.9/templates/#builtin-filters

### jinjia2控制结构

+ if语句
+ for语句
+ 宏，类似Python的继承
+ 为了重复使用宏，把其保存为单独的文件中，然后在需要使用的模版中导入：
+ 需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有的模版中，以避免重复：
+ 另一种重复使用代码的强大方式是模版继承，它类似于python代码中类继承。首先创建一个名为base.html的基模版
+ block标签定义的元素可在衍生模版中修改。本例中，我们定义了名为head、__title__和body块。注意，__title__包含在head中。下面是基版的衍生模板

### 使用bootstrap
官网http://getbootstrap.com
bootstrap是Twitter开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页，而且这些网页还能兼容所有现代web浏览器。bootstrap是客户端框架，因此不会直接涉及服务器。服务器需要做的只是提供引用了bootstrap层叠式表CSS和Javascript文件的HTML响应，并在HTML、css和JavaScript代码中实例化所需的组件。这些操作最理想的执行场就是模版。使用一个名为Flask-Bootstrap的Flask扩展，简化集成过程。pip安装
```
#pip install flask-bootstrap
from flask_bootstrap import Bootstrap
#...
bootstrap = Bootstrap(app)

#In [5]: !cat hello.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
  return '<h1>hello,%s!<h1>' % name

if __name__ == '__main__':
    app.run(debug=True)
```
### flask-moment插件
## web 表单
尽管flask的请求对象提供的信息足够用于处理web表单，但有些任务很单调，而且重复操作。比如，生成表单的HTML代码和验证提交的表单数据。Flask-WTF扩展可以把处理WEB表单的过程变成一种愉悦的体验。这个扩展对独立的WTForms包进行了包装，方便集成到Flask程序中。pip install flask-wtf即可安装。
### 跨站请求伪造保护
默认情况下，Flask-WTF能保护所有表单免受跨站请求伪造cross-site request forgery即CSRF的攻击。为了实现CSRF保护，Flask-WTF需要程序设置一个密钥。Flask-WTF利用这个密钥生成加密令牌，再用令牌验证请深圳市中表单数据的真伪。设置密钥的方法如下：
```
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```
app.config字典可用来存储框架、扩展和程序本身的配置变量。使用标准的字典句法就能把配置值添加到app.config对象中。这个对象还提供一些方法，可以从文件或环境中导入配置值。SECRET_KEY配置变量是通用密钥，可在Flask和多个第三方扩展中使用。
> 为了增强安全性，密钥不应该写入代码中，而要保存在环境变量中

### 表单类
使用Flask-WTF时，每个Web表单都有一个继承自Form的类表示。这个类定义表单中的一组字段，每个字段都用对象表示。字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。
```
#cat hello.py
from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

if __name__ == '__main__':
    manager.run()
```
这个表单中的字段都定义为类变量，类变量的值是相应字段类型的对象。StringField类表示属性为type="text"的```<input>```元素。SubmitField类表示属性为type="submit"的```<input>```元素。StringField构造函数中的可选参数validators指定一个由验证函数组成的列表，在接受用户提交的数据之前验证数据。验证函数Required()确保提交的字段不为空。
+ WTFomrs支持的HTML标准字段如下

字段类型|说明
---|---
StringField   | 文本字段
TextAreaField | 多行文本字段
PasswordField | 密码文本字段
HiddenField   | 隐藏文本字段
DateField     | 文本字段，值为datetime.date格式
DateTimeField | 文本字段，值为datetime.datetime格式
IntegerField  | 文本字段，值为整数
DecimalField  | 文本字段，值为decimal.Decimal(小数点)
FloatField    | 文本字段，值为浮点数
BooleanField  | 复选框，值为True和False
RadioField    | 一组单选框
SelectField   | 下拉列表
SelectMultipleField | 下拉列表，可选择多个值
FileField     | 文件上传字段
SubmitField   | 表单提交按钮
FormField     | 把表单作为字段嵌入另一个表单
FieldList     | 一组指定类型的字段
+ WTForms验证函数

验证函数| 说明
---|---
Email   | 验证电子邮件地址
EqualTo | 比较两个字段的值；常用于要求输入两次密码进行确认的情况
IPAddress| 验证IPv4网络地址
Length  | 验证输入的值在数字范围内
Optional| 无输入值时跳过其他验证函数
Required| 确保字段中有数据
Regexp  | 使用正则表达式验证输入值
URL     | 验证URL
AnyOf   | 确保输入值在可选值列表中
NoneOf  | 确保输入值不在可选值列表中

### 把表单渲染成HTML
表单字段是可调用的，在模版中调用后会渲染成HTML。假设视图函数把一个NameForm实例通过参数form传入模版，在模板中可以生成一个简单的表单，如下所示：

当然这个表单很简陋，若想改进表单的外观，可以把参数传入渲染字段的函数，传入的参数会被转换成字段的HTML属性。例如，可以为字段指定id或class属性，然后定义CSS样式。

即便能指定HTML属性，但按照这种方式渲染表单的工作量还是很大，所以在条件允许的情况下最好能使用Bootstrap中的表单样式。Flask-Bootstrap提供了一个非常高端的辅助函数，可以使用Bootstrap中预先定义好的表单样式渲染整个Flask-WTF表单，而这些操作只需一次调用即可完成。使用Flask-Bootstrap,上述表单可使用下面的方式渲染：


import 指令使用方法和普通Python代码一样，允许导入模板中的元素并用在多个模版中。导入的bootstrap/wtf.html文件中定义了一个使用Bootstrap渲染Flask-WTF表单对象的辅助函数。wtf.quick_form()函数的参数为Flask-WTF表单对象，使用Bootstrap的默认样式渲染传入的表单。

在index.html中，模板的内容现在有两部分，第一部份是页面头部，显示欢迎消息。这里用到一个模版条件语句。Jinja2中的条件语句格式为{% if condition %}...{% else %}...{% endif %}。如果条件计算结果为True,那么渲染if和else指令之间的值。反之，渲染else和endif之间的值。
### 在视图函数中处理表单
在新版hello.py中，视图函数index()不仅要渲染表单，还要接收表单中的数据。
```
#hello.py路由方法
@app.route('/',methods=['GET','POST'])
def index():
  name = None
  form = NameForm()
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
  return render_template('index.html',form=form,name=name)
```
app.route修饰器中添加的methods参数告诉Flask在URL映射中把这个视图函数注册为GET和POST请求的处理程序。如果没指定methods参数，就只把视图函数注册为GET请求的处理程序。
### 重定向和用户会话
用户输入名字后提交表单，然后点击浏览器的刷新按钮，会看到一个重复提交表单的警告，要求再次确认。之所以出现这个警告是因为在刷新页面时浏览器会重新发送之前发送过的最后一个请求。如果这个请求是一个包含表彰数据的POST请求，刷新页面后会再次提交表单。大多数情况下，这并不是想要的结果，基本这个原因，最好别让web程序把post请求作为浏览器发送的最后一个请求。这种请求的方式是，使用重定向作为POST请求的响应，而不是使用常规响应。重定向是一种特殊的响应，响应内容是URL，而不是包含HTML代码的字符串。浏览器收到这种响应时，会向重定向的URL发起GET请求，显示页面的内容。这种方式叫做Post/重定向/Get模式。
### Flash消息
请求完成后，有时需要让用户知道状态发生了变化。一个例子就是用户提交了有一项错误的登录表单后，服务器发回的响就重新渲染了登录表单，并在表单上面显示一个消息，提示用户名或密码错误。这种功能是是Flask的核心特性。flash()函数可实现这种效果。
```
from flash import Flask,render_template,session,redirect,url_for,flash
@app.route('/',methods=['GET','POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    return redirect(url_for('index'))
  return render_template('index.html',form = form,name = session.get('name'))
```
在这个例子中，每次提交的名字都会和存储在用户会话中的名字进行比较，而会话中存储的名字是前一次在这个表单中提交的数据。如果两个名字不一样，就会调用flash()函数，在发给客户端的下一个响应中显示一个消息。仅调用flash()函数并不能把消息显示出来，程序使用的模版要渲染这些消息。最好基模板中渲染Flash消息，因为这样所有页面都能使用这些消息。Flask把get_flashed_messages()函数开放给模板，用来获取并渲染消息。

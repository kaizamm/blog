---
title: git基本命令
date: 2017.1.13
---

### 概述
#### git三大区
+ 工作区、暂存区(stage)、版本库；

#### 文件状态
+ untracked:未加入版本控制的文件
+ tracker:已纳入版本控制管理的文件
+ unmodified:未做过修改，并且已经在版本控制管理中的文件
+ modified：做过修改的受版本控制管理的文件
+ staged:已放入暂存区的文件。untracked或者modified的文件，执行过git add后，就进入了暂存区。

> 输入gitk 打开图形化工具

### 提交至本地版本库
+ makdir project && cd project && git init project为工作区，.git为版本库
+ git add file.txt 把文件添加到暂存区；.gitignore文件里可用正则写被git忽略的文件
+ git rm --cached file.txt 删除已经git add 到暂存区的文件；git rm -f file.txt 删除暂存区及工作区文件
+ git commit -m "first commit" 提交更改到版本库，可多次git add file后，再git commit;git commit -a Git会自动把所有已经跟踪过的文件暂存起来一并提交，从而跳过git add步骤。[更多](http://askcuix.github.io/blog/2013/05/27/the-git-command/)
+ git checkout -- file.txt 可从版本库里把文件checkout出来
+ git status 查看工作区状态，可看到暂存区中是否有git add后未commit的文件

### 版本回退
+ git log 可查看3次历史提交日志，此时能看到版本库ID
#### 删除错误提交的commit
git rm 删除暂存区的文件，而错误提交到了版本库则需用git reset; 错误提交到版本库，此时工作区、暂存区、版本库都是一样的。git reset有三个选项， --hard 、 --mixed、 --soft。
##### git reset
+ git reset --soft 版本库ID: 只将版本库里的内容回滚至上个版本，即撤消已提交的版本库，不影响工作区及暂存区。
+ git reset --mixed 版本库ID： 撤消已提交的版本库和暂存区，不影响工作区
+ git reset --hard HEAD^  git中HEAD表示当版本，上一个版本是HEAD^，上上个版本是HEAD^^，也可写成HEAD~100，这个表示向上100个版本。该命令将版本库、暂存区、工作区全部恢复至指定版本。
+ git reset 仅仅从暂存区移除所有的没有提交的修改。
##### git revert
+ git revert 可以撤销某个之前的提交，但非删除那个提交，只是恢复那次提交的改动。改命令其实是产生一个新的提交。不会像git reset后，会提示版本落后的情况。

+ git reflog 可以用来记录你操作的每次命令，如当你回退到上上个版本后，又不知道最开始那个commit id，则可通过这个命令查看。

#### 修改最后一次提交
git commit --amend ,该参数可以直接修改最后的一次提交，若仅是修改注释，则无需修改暂存区。
> 注意，请不要修改已经发布的提交。

#### 撤消本地改动
+ 未被提交的文件，如工作区的文件有修改，发现修改有错误，想恢复到以前，则直接用git checkout \-\- file
+ 放弃工作区所有本地改动，让你的本地恢复到上次提交之后的版本，可以用git reset --hard HEAD ，或者用git checkout <SHA>
> 指针脱离(detached），如果想在在这种情况下提交，可通过创建新的分支来实现，即 git checkout -b <SHA>


### 远程仓库
在[github](https://github.com/)注册并创建一个private reposity

#### 提交至远程仓库
+ HTTPS
```
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/kaizamm/git.git #将远程主机命名为origin
git push -u origin master
```
+ SSH
```
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:kaizamm/git.git
git push -u origin master
```
#### git remote
+ git remote 列出远程主机；git remote -v 列出远程主机时带上网址
+ git remote show origin #查看远程主机的详细信息
+ git remote add：主机名 添加远程主机，删除:git remote rm，重命名:git remote rename

#### git Fetch
一旦远程主机版本库有了更新，需要将这些更新取回本地，则需要用到git fetch; git fetch命令通常用来查看其他人的进程，因为它取回的代码对你的本地开发代码没有影响。
```
git fetch origin master
git branch -a #查看所有分支，git brach -r 查看远程分支
git checkout -b newbranch origin/master #表示在origin/master的基础上，创建一个新的分支；或者用git merge命令或git rebase命令，在本地分支上合并远程分支。
```
#### git Pull
该命令是取回远程主机的某个分支的更新，再与本地指定分支合并
```
git pull <远程主机名> <远程分支名>:<本地分支名>
git pull origin next:master #若远程分支是与当前分支合并，则冒号后的部分可以省略 git pull origin next #取回origin/next分支后，再与当前分支合并，等同于先做git fetch,再做git merge
git fetch origin
git merge/rebase origin/next

git merge --allow-unrelated-histories a b (http://stackoverflow.com/questions/27641380/git-merge-commits-into-an-orphan-branch/36528527#36528527)
```

#### git checkout
##### git checkout 常用来创建分支和切换分支
+ 创建一个新分支，git branch newbranch;
+ 切换到新的分支，git checkout newbranch;
这两个命令可以合并成一个命令，git checkout -b newbranch;

##### 从本地版本库检出文件
+ git checkout \-\- file


#### 指针 HEAD
#### git branch
+ git branch -d <branchname> 删了一个分支
+ git merge/rebase <branchname>把该分支合并到当前分支，只能合并新增的文件，当该分支中有与主分支中有文件同名时会有冲突，若有冲突需要手动处理完该冲突后，才能继续合并
[更多](https://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6)

#### git pull
如果当前分支与远程分支存在追踪关系，git pull 就可以省略远程分支名，即可以直接git pull origin，同理git push，[更多详见](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)
#### 从远程仓克隆

git clone git@github.com:kaizamm/git.git

### git config
+ git config --global --list 列出当前的全局环境变量
+ git config --config user.name "kaiz" 设置git用户名
+ git config --config user.email "xxx@email.com" 设置邮箱

### 配置github ssh keys
```
$ssh-keygen -t rsa #三个回车
拷备id_rsa.pub内容，粘贴至github/setting/SSH and GPG keys
$ssh -T git@github.com
提示 Hi kaizamm! You've successfully authenticated, but GitHub does not provide shell access.则成功
```
### git 工作流程
git支持很多种工作流程，我们采用的一般是这样，远程创建一个主分支，本地每人创建功能分支，日常工作流程如下：

去自己的工作分支
```
$ git checkout work

工作
....

提交工作分支的修改
$ git commit -a

回到主分支
$ git checkout master

获取远程最新的修改，此时不会产生冲突
$ git pull

回到工作分支
$ git checkout work

用rebase合并主干的修改，如果有冲突在此时解决
$ git rebase master

回到主分支
$ git checkout master

合并工作分支的修改，此时不会产生冲突。
$ git merge work

提交到远程主干
$ git push
```
这样做的好处是，远程主干上的历史永远是线性的。每个人在本地分支解决冲突，不会在主干上产生冲突。

> 当出现history-not-related时，git merge --allow-unrelated-histories a b

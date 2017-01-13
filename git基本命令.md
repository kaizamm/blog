---
title: git基本命令
date: 2017.1.13
---

### 本地仓库 工作区 暂存区(stage)
+ makdir project && cd project && git init project为工作区，.git为版本库
+ git add file.txt 把文件添加到暂存区；
+ git rm file.txt 删除已经git add 到暂存区的文件
+ git commit -a "first commit" 提交更改到版本库，可多次git add file后，再git commit
+ git checkout -- file.txt 可从版本库里把文件checkout出来
+ git status 查看工作区状态，可看到暂存区中是否有git add后未commit的文件

### 版本回退
+ git log 可查看3次历史提交日志
+ git reset --hard HEAD^  git中HEAD表示当版本，上一个版本是HEAD^，上上个版本是HEAD^^，也可写成HEAD~100，这个表示向上100个版本。
+ git reflog 可以用来记录你操作的每次命令，如当你回退到上上个版本后，又不知道最开始那个commit id，则可通过这个命令查看。

### 远程库库
在[github](https://github.com/)注册并创建一个private reposity
#### 提交至远程仓库
+ HTTPS
```
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/kaizamm/git.git
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
#### 从远程仓克隆
git clone git@github.com:michaelliao/gitskills.git

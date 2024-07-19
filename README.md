![alt text](https://github.com/turkishviking/Python-Robocode/blob/master/Python-Robocode/robotImages/robotTitre.png?raw=true "Python-Robocode")
===============
 
Fork from https://github.com/turkishviking/Python-Robocode 

修复bug
代码添加中文注释

### A Fork of Robocode for python programming

This is the new and maintained version developed with PyQt

### Need help to start? Check the [wiki](https://github.com/turkishviking/Python-Robocode/wiki)

Any help is welcome! This is a beta version, tell me if you notice any bugs

### If you want to contribute, I do not have the time yet for developing some base robot( wall runner, coins camper, random move etc...). If you do this, I will be happy to include it into the source code. (Post an issue or make a pull request in this case).

### What's New & Task list:

  - [x]  move()
  - [x]  turn()
  - [x]  gunTurn()
  - [x]  radarTurn()
  - [x]  getPostion
  - [x]  radarDetection()
  - [x]  getTargetPosition()
  - [x]  getTargetName()
  - [x]  bulletPower
  - [x]  on_hit_by_bullet()  
  - [x]  bulletSize
  - [x]  WallCollision       
  - [x]  MapSize
  - [x]  Number_Of_Enmies_Left()
  - [x]  GameSpeed
  - [x]  on_Robot_Death()
  - [x]  reset()             --> too stop all move at any time
  - [x]  stop()              --> too allow to make moves sequences
  - [x]  RobotPrint()        --> too allow the robot to print in a textBox
  - [x] RobotMenu with lifeBar
  - [x]  Battle Series
  - [ ]  Batlles Statistics
  - [ ]  .exe
  - [ ]  .deb
  - [x]  Qt Integration
  - [ ]  Qt IDE (syntax highlighter, auto completion, Base Robot)    --> Not Done but I have an old project of IDE to do it
  - [ ]  Add Classe Reference in the wiki
  - [ ]  To prevent bot's to use Sockets, urllib2, and Sub/Multi Processing Module (more safe for users)
  - [x]  Window resizable 
  - [ ]  Write Calculus in cython (to speed up the code) 

## conf.py配置：
#### 配置extensions，修改source/conf.py文件内容：
```
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax'
]
```

配置项目路径：

```
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

```
这块路径使用../../是因为我们的demo是一个包，如果demo下面没有__init__.py文件，则可以路径为../../demo。
## 生成rst文件
使用sphinx-apidoc生成rst文件，-o 后面跟的是保存rst文件的路径，你的index.rst文件在哪个目录，就指定哪个目录，然后最后面是代码路径。

sphinx-apidoc -o C:\Python-Robocode\doc\source C:\Python-Robocode\Python-Robocode
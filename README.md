# SystemEverywhere

> 日拱一卒，功不唐捐

## 项目背景

本项目的设计目标是为了设计一个小型软件解决各种场景下的小需求．这些需求一般不容易被大型软件关注，
或者因为收益过少难以进行．对于这些零碎的需求，本软件希望能够方便特定人群的工作和日常生活，通过自己
日常的观察和感受设计功能，实现软件的价值

### 需求分析
- 通过大学三年的观察，我发现了老师这个用户群体在上课时所产生的需求，体现在:
  - 老师有时很担心自己走错教师，会进来询问同学某某课是不是在这里上，所以本软件的主界面显示了当前上课的课程信息，帮助老师和同学不要走错教室．
  - 有些老师上课喜欢签到，扫二维码固然方便，但是很多学生会才则铃声进入教室，往往无法及时签到，老师又不忍心立即关闭二维码，浪费了课堂的时间．而且，二维码虽然会定时更新，但依然可以异地扫码．因此，本软件设计了人脸识别签到的功能，只需要学生进入教室，就能自动完成签到．
  - 有时全部签到太耗费时间，老师喜欢抽点同学．但是随机选择还需要耗费精力，而且还会有不知道该怎么念的尴尬，
    因此，本软件增加了随机点名的功能，同时显示同学的拼音．
  - 上述功能通过excel表格记录．
  - 上网课期间，我的数学老师很喜欢用白板画图，或者输入数学公式，因此我在软件中实现了绘图和绘制数学函数的功能，相比于Windows白板，不仅仅是黑笔，本软件有各种颜色和贴图功能，绘制基本图形的功能，数学函数采用`Matlabplot`绘制方法，清晰可靠．
  - 有些老师上课会忘记时间而拖堂，所以本软件具有定时提醒老师时间的功能并具有进度条显示上课的时间进度，帮助老师合理安排课堂时间．
- 在家办公学习的过程中，我发现很多细小的功能需要打开各种软件才能分别完成，因此我选择将这些功能集成在本软件中，体现在：
- 集成小型浏览器功能，没有其他多余的插件和广告，十分简洁．
  - 集成计算器功能，不用寻找电脑的计算器或者寻找手边的计算器．
  - 集成文本编辑功能，采用富文本编辑器，能够编辑丰富的图文样式排版并保存．
  - 集成便笺功能，能够让便签始终浮于桌面上，起到备忘录的功能，这也是我认为最好用的功能．
  - 集成绘图功能，如果手边没有平板，可以打开绘图工具绘制画面，类似于画图工具．
  - 集成扫雷游戏，无聊的时候可以放松玩一玩，又不会沉迷的小游戏，很怀旧．
  - 集成音乐播放器给你，一边写代码一边听音乐是我们电院专业很多人的爱好，自然少不了这个功能．
  - 集成时间进度条的功能，从来没有一款软件会将每天的时间做成一个进度条，但身边的同学都很喜欢番茄中这种规划时间的工具，所以本软件将`24h`变成百分比，能够催促人们珍惜每一分钟的时间努力前进．



## 项目介绍

本项目基于生活中对老师，同学两类群体的观察，分析他们的需求，设计了符合其想法的实用小型集成软件．本软件设计计时器，人脸识别网络，签到系统，浏览器，计算器，文本编辑，便笺，提醒事项，绘图白板，音乐播放器，扫雷小游戏等使用工具，针对不同的应用场景引入不同的入口UI界面．本项目主要遵循软件开发的流程，从需求分析到建模设计到代码实现到迭代优化，尝试开发出一个有趣有用的应用软件．



## 环境依赖

本项目依赖于python环境，执行以下命令获得环境．建议使用conda新建虚拟环境后安装．

```bash
pip install -r requirements.txt
```

本项目尝试编译成二进制可执行文件供使用，但发生了环境文件的缺失未能成功．



## 使用手册及Demo

入口UI有两种模式，（预置了三种模式），并进行了界面的美化．

- 教室模式如下图：
  - <img src="./images/截屏2021-03-23 下午10.20.02.png" alt="截屏2021-03-23 下午10.20.02" style="zoom:50%;" />
  - 在该模式中，分为４块内容：
    - ．上侧是软件logo
    - 左侧是课程信息详情，包括课程名，课程时间和授课教师．其目的在于帮助进入教室的老师和同学确认上课信息．
    - 右侧是辅助功能，涵盖上课所需要的４－５种功能，包括人脸签到，点名，绘制函数，白板和控制面板，其中控制面板与教室的物联网搭建相关，暂时没能实现，主要用于控制灯，空调，窗帘等的开关和监控温度湿度等．
    - 下测主要是时间条，用于提醒老师把握上课的进度，避免拖堂或者讲不完当天的授课计划．
- 办公模式如下图：
  - <img src="./images/截屏2021-03-23 下午10.20.17.png" alt="截屏2021-03-23 下午10.20.17" style="zoom:50%;" />
  - 在该模式中，分为４块内容：
    - 上侧是软件logo．
    - 左侧是提醒事项，用来记录当日的工作安排．
    - 右侧是辅助功能，涵盖在个人使用电脑时的日常需求，包括：浏览器，计算器，文本编辑器，便笺，画图，扫雷和音乐播放器．
    - 下側是时间条，用来展示一天已经过去百分之多少，用来督促个人抓紧时间把握当下，合理安排当日的工作．

接下来对各种功能进行介绍展示：

- 签到界面
  - <img src="./images/截屏2021-03-23 下午10.20.37.png" alt="截屏2021-03-23 下午10.20.37" style="zoom:50%;" />
  - 用户使用签到界面能够导入学生名单，设置签到截至时间，展示实时检测效果并输出签到结果．实时界面如下（这里学生名单没有改成真名，所以是照片的文件名）：
    - <img src="./images/截屏2021-03-23 下午10.21.31.png" alt="截屏2021-03-23 下午10.21.31" style="zoom:50%;" />
- 随机点名界面
  - <img src="./images/截屏2021-03-23 下午10.30.56.png" alt="截屏2021-03-23 下午10.30.56" style="zoom:50%;" />
  - 用户使用该界面能够设置随机点名人数，确认人员是否到场，看到人员姓名及其拼音和签到情况．并将签到结果存入excel中．excel表格结果如下：
    - <img src="./images/截屏2021-03-23 下午10.32.07.png" alt="截屏2021-03-23 下午10.32.07" style="zoom:50%;" />
- 函数绘制界面
  - 函数绘制界面采用`Matplotlib`标准库进行绘制，符合一般论文绘制要求，简介清晰，效果如下：
    - <img src="./images/截屏2021-03-23 下午10.32.43.png" alt="截屏2021-03-23 下午10.32.43" style="zoom:50%;" />
- 白板界面
  - 白板主要用于板书，在触控屏或数控板上更有使用的价值．白板具有保存文件，读入文件，选择区域，擦除，涂色，取色器，贴图，铅笔，刷子，基本图形，选择颜色等功能，与windows自带画板的功能几乎一致．
    - <img src="./images/截屏2021-03-23 下午10.33.40.png" alt="截屏2021-03-23 下午10.33.40" style="zoom:50%;" />
- 浏览器界面
  - 浏览器界面采用早期浏览器的标准，实现了一个仅能浏览网页不具有插件广告的简洁界面．该浏览器支持SSL加密访问，并能够访问google首页搜索．
    - <img src="./images/截屏2021-03-23 下午10.34.16.png" alt="截屏2021-03-23 下午10.34.16" style="zoom:50%;" />
- 计算器
  - 计算器用于普通的加减乘除计算，不配备复杂的科学计算，因为本软件的目的在于满足日常小需求即可．
    - <img src="./images/截屏2021-03-23 下午10.34.30.png" alt="截屏2021-03-23 下午10.34.30" style="zoom:50%;" />
- 文本编辑器
  - 文本编辑器采用富文本的编辑形式，能够设置字体样式，大小，颜色，也能够插入图片等，是日常生活中写文档的好帮手．
    - <img src="./images/截屏2021-03-23 下午10.36.11.png" alt="截屏2021-03-23 下午10.36.11" style="zoom:50%;" />
- 便利贴
  - 便笺界面会永远浮于桌面的最上方，用来记录并提醒用户当日的备忘录，其后台引擎基于`sqlite`轻量级数据库，方便软件关闭后依然存储数据．
    - <img src="./images/截屏2021-03-23 下午10.37.33.png" alt="截屏2021-03-23 下午10.37.33" style="zoom:50%;" />
- 扫雷
  - 有时很无聊有不希望玩游戏沉迷浪费时间？单机的小游戏是一个很好的选择．扫雷界面区别与以往的扫雷图案，怀旧的同时，还能给用户一种全新的体验．
    - <img src="./images/截屏2021-03-23 下午10.44.07.png" alt="截屏2021-03-23 下午10.44.07" style="zoom:50%;" />
- 音乐播放器
  - 用户在这里可以加载音乐文件并播放，边听音乐边播放，内置曲目＜致爱丽丝＞．
    - <img src="./images/截屏2021-03-23 下午10.44.50.png" alt="截屏2021-03-23 下午10.44.50" style="zoom:50%;" />



## TODO

1. 出错处理程序还有待完善，目前，很多按钮如果不按照顺序点击会出现程序崩溃，考虑到用户可能以任何方式使用本软件，本软件还需要考虑各种非正常操作情况．
2. 场景有待加强和完善，部分功能需要软件以外的硬件支持，还需要结合其他系统例如`jaccount`才能发挥更好的作用．
3. 代码注释还有待完善，目前注释和代码比低于10%，难以维护．
4. 界面还有待美化，程序逻辑还有待完善，目前程序较为简洁且CPU占用率高．
5. 项目中有使用`os.system()`命令直接打开另一进程的操作，虽然当本程序正常退出时这些进程也会退出，但是如果发生异常错误，那么它们将会变成独立进程继续运行．因此，需要修改对应部分的UI代码，使之能够以类的方式直接调用．



## 备注

1. `opencv`和`pyqt`可能会发生冲突，降低`pyqt`版本或使用`opencv-headless`可以解决问题．



## 参考资料

1. https://github.com/learnpyqt/15-minute-apps.git




---

作者: Harry-hhj  主页: https://githubcom/Harry-hhj
# weather4u
一个简单的Windows天气预报程序  ~~年轻人的第一个程序~~

基于Python，使用高德开放平台的天气查询API

**觉得好用就点个star吧   [我的哔哩哔哩](https://space.bilibili.com/403373585)   欢迎为此项目贡献代码**


# 主要功能
调用Windows通知功能，定时弹窗提示今明两天的天气


# 如何使用
## 使用发布版本（不推荐）
- 转到项目的 [Releases界面](https://github.com/rtlnut/weather4u/releases)
- 下载最新发布的exe文件
- 运行

> [!IMPORTANT]
> 由于~~我不会修这个BUG了~~ 主程序运行的图标引用了weather_icon.ico
> 
> 所以无论你用发布版本还是自行编译都要**保证 weather4u.exe 和 weather_icon.ico 在同一目录下**
> 
> 直接运行py文件时同理，保证 win_weather.py 和 weather_icon.ico 在同一目录下
> 
> 否则会报错 FileNotFoundError: [Errno 2] No such file or directory

> [!CAUTION]
> 注意：理论上发布版本完全可用，但由于使用的是我个人的高德天气API密钥，故不保证其拥有长久可用性，如要日用请自行编译


## 自行编译
### 1. 准备API

详见高德开放平台 [成为开发者并创建 Key](https://lbs.amap.com/api/webservice/create-project-and-key)

### 2. 准备环境
- 确保你的电脑安装了Python，CMD中输入 `python -V` 查询
- 安装所需模块 `pip install requests pywin3 pyinstaller pystray`

### 3. 配置
- 从[这里](https://github.com/rtlnut/weather4u/archive/refs/heads/main.zip)下载源代码

- 将你从高德控制台获得的Key填入 win_weather.py 第16行
```
api_key = 'YOUR_AMAP_API_KEY'  # 替换为你的高德API密钥
```
最后应该是这样的
```
api_key = '3a8570xxxxxxxxxx'
```
- 保存并关闭文件

### 4. 打包并运行
- 确保 win_weather.py build_weather.py weather_icon.ico 三个文件在同一目录下
- 运行 build_weather.py
- 如果没有报错，目录下会生成weather4u.exe，运行即可

> [!IMPORTANT]
> 由于~~我不会修这个BUG了~~ 主程序运行的图标引用了weather_icon.ico
> 
> 所以无论你用发布版本还是自行编译都要**保证 weather4u.exe 和 weather_icon.ico 在同一目录下**
> 
> 直接运行py文件时同理，保证 win_weather.py 和 weather_icon.ico 在同一目录下
> 
> 否则会报错 FileNotFoundError: [Errno 2] No such file or directory


## 如何设置
- 初次运行时将打开设置界面
- 点击保存配置后，程序将自动最小化，可展开右下角托盘并右键单击程序图标，点击配置重新打开此界面
- 二次运行时，程序检测到存在配置文件也会自动最小化，配置方法同上

# 已知问题
- 开机自启失败，图标问题，我已经熬夜弄了一个半小时了，放弃了，不要使用此功能

# BUG解决
## 报错INVALID_USER_KEY
- 检查API密钥格式
## 其他有infocode的报错
- 详见高德开放平台 [错误码说明](https://lbs.amap.com/api/webservice/guide/tools/info/)
## 弹窗正常弹出，但弹窗内容是报错
- 任务管理器强制结束程序运行
- 删除用户目录 (如 C:\Users\114514) 下的weather_config.json文件
- 重新运行程序

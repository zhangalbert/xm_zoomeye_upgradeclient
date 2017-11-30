# xm_zoomeye_upgradeclient
#### 简单介绍:
>[xm_zoomeye_upgradeclient](https://github.com/xmdevops/xm_zoomeye_upgradeclient) 主要作为[xm_zoomeye_upgradeserver]()的自动升级检测客户端微框架.

***


#### 开发环境:
> SY_ENV: CentOS6.5+ \
> PY_ENV: Python2.6.6+ 

***

#### 安装部署:
`git clone https://github.com/xmdevops/xm_zoomeye_upgradeclient`

`cd xm_zoomeye_upgradeclient`

`pip install -r requirements.txt`

`python manage.py`

***


#### 管理界面:
`http://<ip>:<port>/, 默认监听端口8081,可通过修改xm_zoomeye_upgradeclient.yaml自定义`

****

#### 主要组件:
* check_service,主要用于检测数据源是否有文件更新
* download_service,主要用于从数据源下载文件
* upload_service,主要用于上传文件到多个目标
* alert_service,主要用于定时/周期报表发送
* webui_service,主要用于展示组件自身以及过程中产生的信息

***

#### 项目特色:
* 基于SpringPython的IOC/AOP方式组织代码架构,组件/处理器可以任意侵入式扩展
* 本地Cache作为缓存组件来保证多个组件之间异步交互
* 线程+队列实现本地Sqlit3数据库多线程/多进程同步或异步处理增删查改
* crontab+sched实现定时/周期任务调度

***

#### 软件流程:
![Flow Chart](https://github.com/xmdevops/xm_zoomeye_upgradeclient/docs/design/flow_chart.png)
#### 

***



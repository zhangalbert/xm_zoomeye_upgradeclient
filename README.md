# xm_zoomeye_upgradeclient
#### 简单介绍:
>[xm_zoomeye_upgradeclient](https://github.com/xmdevops/xm_zoomeye_upgradeclient) 主要作为[xm_zoomeye_upgradeserver]()的固件自动升级检测客户端.

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

#### 主要配置:
* xm_zoomeye_upgradeclient.yaml,作为整个程序入口配置
* /etc/xm_zoomeye_upgradeclient/check/xm_dvr.json
```json
{
  "name": "xm_dvr",
  "auth_user": "",
  "auth_pass": "",
  "_comments": "",
  "base_url": "",
  "proxy_host": "",
  "target_host": "",
  "revision_seconds": "",
  "summarize_interval": "",
  "check_filter": "default",
  "alert": {
    "medias": [
      {
        "relation_name": "default",
        "relation_type": "email",
        "to": [],
        "cc": []
      }
    ],
    "crontab": "0 23 * * *"
  },
  "upload": [
    {
      "relation_name": "default",
      "relation_type": "rsync"
    }
  ],
  "target_cache": "xm_upgradefiles"
}
```
* /etc/xm_zoomeye_upgradeclient/upload/upload.json
```json
{
  "default": {
    "rsync": {
      "_comments": "",
      "binpath": "",
      "username": "",
      "password": "",
      "serverip": "",
      "serverport": "",
      "localpath": "",
      "remotepath": ""
    }
  }
}
```
* /etc/xm_zoomeye_upgradeclient/alert/alert.json
```json
{
  "default": {
    "email": {
      "_comments": "",
      "smtp_host": "",
      "smtp_port": 25,
      "smtp_user": "",
      "smtp_pass": "",
      "debug_num": 1
    }
  }
}
```

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
* 本地Cache作为缓存组件来保证多个组件之间纯异步交互
* 线程+队列实现本地Sqlit3数据库多线程/多进程同步或异步处理增删查改
* crontab+sched实现定时/周期任务调度

***

#### 未完待续
* SQLite3未提供SQL转义,暂未转义对于有些包含特殊字符的异常信息可能会导致独立SQLite线程异常,后期需要转义log_message
  * 方案一. 通过web.register_database注册除SQLite3外的其它引擎,来安全处理增删查改.

***

#### 软件流程:
![Flow Chart](https://raw.githubusercontent.com/xmdevops/xm_zoomeye_upgradeclient/master/docs/design/flow_chart.png)
#### 

***

#### 功能展示:
* ##### webui-index
![Flow Chart](https://raw.githubusercontent.com/xmdevops/xm_zoomeye_upgradeclient/master/docs/design/webui_index.png)

***

* ##### webui-list
![Flow Chart](https://raw.githubusercontent.com/xmdevops/xm_zoomeye_upgradeclient/master/docs/design/web_list.png)

***

* #### webui-detail
![Flow Chart](https://raw.githubusercontent.com/xmdevops/xm_zoomeye_upgradeclient/master/docs/design/web-detail.png)

***
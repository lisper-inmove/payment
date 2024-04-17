#!/bin/bash

# 项目名称
export APPNAME=Demo
# 是否开启终端显示日志
export LOGGER_ENABLE_CONSOLE=true
# 是否开启syslog日志
export LOGGER_ENABLE_SYSLOG=false
# syslog日志服务器地址
export LOGGER_SYSLOG_HOST=logger.server
# syslog日志服务端口
export LOGGER_SYSLOG_PORT=514
# syslog日志设备
export LOGGER_SYSLOG_FACILITY=local7
# MongoDB数据库ip
export MONGODB_SERVER_ADDRESS=192.168.3.124
export MONGODB_PORT=27018
# 服务启动环境
export RUNTIME_ENVIRONMENT=test
export APP_PRIVATE_KEY_FILE=app-private-key.txt
export ALIPAY_PUBLIC_KEY_FILE=alipay-public-key.RSA2.txt
export ALIPAY_APPID=2021001102655667

export PYTHONPATH=`pwd`/src
export APPROOT=`pwd`/src

function get_available_port() {
    port=6003
    while true
    do
        declare -i flag
        flag=`lsof -i:$port | wc -l`
        if [ $((flag)) -eq 0 ];then
           break
        else
           ((port++))
        fi
    done
    echo $((port+0))
}

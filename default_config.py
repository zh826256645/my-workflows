# -*- coding: utf-8 -*-
"""
默认的配置文件
可复制该文件命名为 config.py
当 config.py 存在时，将默认使用 config.py 的配置
"""
# info/my_info.py 需要的配置文件
MY_INFO = {
    '手机-主号': '188xxxxxxxx',
    '手机-副号': '180xxxxxxxx',
    'qq': '82xxxxxxx',
    'qq邮箱': '82xxxxxxx@qq.com',
    '谷歌邮箱': '82xxxxxxx@gmail.com',
    '身份证号': '44xxxxxxxxxxxxxxxX',
    '家庭地址': '广东省 xx市 xx区 xxxxxxxxxxxxx x 栋 xxx',
    '公司地址': '广东省 xx市 xx区 xxxxxxxxxxxxx x 栋 xxx',
}

# info/my_bookmarks.py 需要的配置文件
MY_BOOKMARKS = {
    '斗鱼': [
        ('yyf', 'https://www.douyu.com/9999')
    ],
    'b站': [
        ('首页', 'https://www.bilibili.com/')
    ],
}

# tools/ip_tools.py 需要的配置
# 从 IP 138 网站获取 api token
IP_138 = {
    'token': ''
}

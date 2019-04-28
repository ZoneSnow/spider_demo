#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import sys

if __name__ == '__main__':
    print('Access Denied.')
    sys.exit()

import os, datetime, logging
from logging.handlers import RotatingFileHandler

DEBUG = True
APP_ROOT = getattr(sys, '__APP_ROOT__', os.path.split(os.path.realpath(__file__))[0])

APP_PATH = getattr(sys, '__APP_PATH__', os.path.join(APP_ROOT, 'packages'))

APP_PATH and sys.path.insert(0, APP_PATH)
'''
消息队列相关
'''

# 队列主机
AMQP_URL = 'amqp://guest:guest@192.168.2.171:5672'  # 本地测试

# 抓取代理待处理队列
PROXY_QUEUE = 'search_proxy'
# 默认队列
UPDATE_QUEUE = 'default_lotto_goods'
# 已更新待同步
WAIT_UPDATE_QUEUE = 'wait_post_goods'
# 等待在各个网站搜索的关键词队列
WAIT_ADD_QUEUE = 'wait_post_new_goods'
# 错误数据
DELETE_QUEUE = 'delete_goods'
# 等待发送的email
SEND_EMAIL = 'send_email'
# 队列每次推送数量
QUEUE_LIMIT = 50

'''
数据采集相关
'''
DATA_CACHE_TIME = 172800  # 抓取数据缓存时间,2天
USE_PROXY = True  # 是否使用代理

'''
数据库相关
'''
DATABASES = {
    'mysql': (
        {  # 开发数据库
            'host': '192.168.2.22',
            'user': 'root',
            'passwd': 'root',
            'port': 3306,
            'charset': 'utf8',
            'db': 'lottery_info',
            'tablepre': '',
            'db_fields_cache': False,
        },
        {  # 19测试数据库
            'host': '192.168.2.19',
            'user': 'root',
            'passwd': 'root',
            'port': 3306,
            'charset': 'utf8',
            'db': 'lottery_info',
            'tablepre': '',
            'db_fields_cache': False,
        },
        {  # 本地测试数据库
            'user': 'root',
            'passwd': 'root',
            'host': '192.168.2.171',
            'port': 3306,
            'charset': 'utf8',
            'db': 'lottery_info',
            'tablepre': '',
            'db_fields_cache': False,
        },
    ),
    'localhost': {
        # localhost 本地跑数据使用
        'host': 'localhost',
        'user': 'root',
        'passwd': 'root',
        'port': 3306,
        'charset': 'utf8',
        'db': 'test',
        'tablepre': '',
        'db_fields_cache': False,
        'data_type': 'dict',
    },
    'sqlite': 'database.db',
    # mongodb://[username:password@]host1[:port1][,host2[:port2],…[,hostN[:portN]]][/[database][?options]]
    # 本地测试数据库
    'mongo': (
        'mongodb://localhost:27017/spider_',
    ),
}

DB_KEY = {
    # 10: 'cpyzwl',
    11: 'cpsll',  # https://cp.360.cn/
    12: 'cpaicai',  # http://www.aicai.com/
    13: 'cp5ll',  # http://datachart.500.com/
    14: 'cpcwl',  # http://www.cwl.gov.cn/
    15: 'cpjsh',  # https://www.jsh365.com/
    16: 'pks',  # https://www.jsh365.com/

}
URL_KEY = {
    # 10: 'cpyzwl',
    11: 'jsh',
    12: 'sll',
    13: 'aicai',
    14: 'cwl',
    15: 'five',
    16: 'pks',
    17: 'gov',  # 体彩
    18: 'cpyzj',  # 彩票易中奖
    19: 'xjfc',  # 新疆福彩
    20: 'gxfc',  # 广西福彩
    21: 'zjfc',  # 浙江福彩
    22: 'gdfc',  # 广东福彩
    23: 'bjfc',  # 北京福彩
    24: 'tjfc',  # 天津福彩
    25: 'cjcp',  # 彩票财经
    26: 'hjcsj',  # 皇家彩世界
}

# 更新数据时使用
QNAME_KEY = {
    # 1: 'ALL',  # 对所有的队列进行更新
    2: 'high_lotto_goods',  # 高频彩彩种
    3: 'local_lotto_goods',  # 地方彩彩种
    4: 'global_lotto_goods',  # 全国彩彩种
    5: 'sports_lotto_goods',  # 体育
    6: 'jc_lotto_goods',  # 竞彩

}
# 7: 'default_lotto_goods',  # 默认队列
# 'DEFAULT': 'default_lotto_goods',  # 默认队列,可将所有开奖结果推送至该队列   default队列单独使用
# 提交更新队列时使用
QNAME_DICT = {
    'HIGH_RATE': 'high_lotto_goods',
    'LOCAL': 'local_lotto_goods',
    'NATIONWIDE': 'global_lotto_goods',
    'SPORTS': 'sports_lotto_goods',
    'JC': 'jc_lotto_goods',
}

# API数据缓存时间
DEAFULT_API_DATA_CHCHE_TIME = 1200 * 86400  # 默认值，下面没有配置的将使用这个值

API_DATA_CACHE_TIMES = {
    20: 365 * 5 * 86400,
    22: 5 * 86400,
}

'''
浏览器信息
'''
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/530.9',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/530.6',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/530.5',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36',
    # Ubuntu
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',  # IE10
    'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0))',  # IE9
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    # IE8
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    # IE7
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER',
    # 猎豹浏览器
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) '  # qq浏览器 ie 6
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ',  # qq 浏览器 ie7
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',  # firefox
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',  # firefox ubuntu
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',  # firefox mac
    'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',  # Opera windows
    # 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',# Google蜘蛛
    # 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)', #Bing蜘蛛
    # 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)', #Yahoo蜘蛛
]

'''
日志配置
'''
APP_LOG = getattr(sys, '__APP_LOG__', True)
level = logging.DEBUG if DEBUG else logging.ERROR
LOGDIR = os.path.join(APP_ROOT, "logs")

# 仅应用日志
if APP_LOG:
    # 每小时一个日志
    _handler = RotatingFileHandler(
        filename=os.path.join(LOGDIR, 'spider_' + datetime.datetime.now().strftime("%Y-%m-%d_%H") + ".log"), mode='a+',
        maxBytes=1024 * 1024 * 5, backupCount=10)
    _handler.setFormatter(
        logging.Formatter(fmt='>>> %(asctime)-10s %(name)-12s %(levelname)-8s %(message)s', datefmt='%H:%M:%S'))
    LOG = logging.getLogger('yzwl_spider')
    LOG.setLevel(level)
    LOG.addHandler(_handler)
    # 在控制台打印
    _console = logging.StreamHandler()
    LOG.addHandler(_console)

'''
邮件配置
'''
EMAIL = {
    'SMTP_HOST': 'smtp.163.com',
    'SMTP_PORT': 25,
    'SMTP_USER': '18878554519@163.com',
    'SMTP_PASSWORD': '',
    'SMTP_DEBUG': True,
    'SMTP_FROM': '18878554519@163.com',
}

EMAIL_NOTICE = {
    # 接收人员邮箱地址列表
    'accept_list': (
        # 'qaulau@qq.com',
        # 'qaulau@139.com',
        # '373799302@qq.com',
        '306333914@qq.com',
    )
}

'''
微信通知
'''
WEIXIN_NOTICE = {
    'accept_list': (
        '',
    ),
    'server': ''
}

SMT_DOMAIN = ''
SMT_API_KEY = ''

'''
全国性彩种 奖项内容
'''

LOTTO_RESULT = {
    4: {"rolling": "0", "nationalSales": "0", "currentAward": "0", "bonusSituationDtoList": [
        {"numberOfWinners": "0", "singleNoteBonus": "0", "additionNumber": "0", "additionBonus": "0",
         "winningConditions": "5+2", "prize": "一等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "0", "additionNumber": "0", "additionBonus": "0",
         "winningConditions": "5+1", "prize": "二等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "10000", "additionNumber": "0", "additionBonus": "0",
         "winningConditions": "5+0", "prize": "三等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "3000", "additionNumber": "0", "additionBonus": "0",
         "winningConditions": "4+2", "prize": "四等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "300", "additionNumber": "0", "additionBonus": "0",
         "winningConditions": "4+1", "prize": "五等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "200", "winningConditions": "3+2", "prize": "六等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "100", "winningConditions": "4+0", "prize": "七等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "15", "winningConditions": "3+1,2+2", "prize": "八等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "5", "winningConditions": "3+0,1+2,2+1,0+2", "prize": "九等奖"}]},
    5: {"rolling": "0", "bonusSituationDtoList": [
        {"winningConditions": "号码按位相符", "numberOfWinners": "0", "singleNoteBonus": "1,040", "prize": "直选"},
        {"winningConditions": "号码按位相符", "numberOfWinners": "0", "singleNoteBonus": "346", "prize": "组选3"},
        {"winningConditions": "号码相符(无同号)", "numberOfWinners": "0", "singleNoteBonus": "173", "prize": "组选6"}],
        "nationalSales": "0", "currentAward": "0"},
    6: {"rolling": "0", "bonusSituationDtoList": [
        {"winningConditions": "号码按位相符", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "直选"}],
        "nationalSales": "0", "currentAward": "0"},
    8: {"rolling": "0", "bonusSituationDtoList": [
        {"winningConditions": "定位中7码", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "一等奖"},
        {"winningConditions": "定位中连续6码", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "二等奖"},
        {"winningConditions": "定位中连续5码", "numberOfWinners": "0", "singleNoteBonus": "1800", "prize": "三等奖"},
        {"winningConditions": "定位中连续4码", "numberOfWinners": "0", "singleNoteBonus": "300", "prize": "四等奖"},
        {"winningConditions": "定位中连续3码", "numberOfWinners": "0", "singleNoteBonus": "20", "prize": "五等奖"},
        {"winningConditions": "定位中连续2码", "numberOfWinners": "0", "singleNoteBonus": "5", "prize": "六等奖"}],
        "nationalSales": "13652.343万", "currentAward": "15620.114万"},
    9: {"rolling": "0", "nationalSales": "0", "currentAward": "0", "bonusSituationDtoList": [
        {"numberOfWinners": "0", "singleNoteBonus": "0", "additionNumber": "0",
         "additionBonus": "0", "winningConditions": "14场比赛的胜平负结果全中", "prize": "一等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "0", "additionNumber": "0",
         "additionBonus": "0", "winningConditions": "13场比赛的胜平负结果全中", "prize": "二等奖"},
        {"numberOfWinners": "0", "singleNoteBonus": "10000", "additionNumber": "0",
         "additionBonus": "0", "winningConditions": "14场选9场比赛胜平负结果全中", "prize": "任9"},

    ],
        'matchResults': [
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
            {"awayTeamView": "0", "homeTeamView": "0", "results": "0", "score": "--"},
        ],
        },
    'SSQ': {"rolling": "0", "bonusSituationDtoList": [
        {"winningConditions": "6+1", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "一等奖"},
        {"winningConditions": "6+0", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "二等奖"},
        {"winningConditions": "5+1", "numberOfWinners": "0", "singleNoteBonus": "3000", "prize": "三等奖"},
        {"winningConditions": "5+0,4+1", "numberOfWinners": "0", "singleNoteBonus": "200", "prize": "四等奖"},
        {"winningConditions": "4+0,3+1", "numberOfWinners": "0", "singleNoteBonus": "10", "prize": "五等奖"},
        {"winningConditions": "2+1,1+1,0+1", "numberOfWinners": "0", "singleNoteBonus": "5", "prize": "六等奖"}],
            "nationalSales": "0", "currentAward": "0"},
    'SD': {"rolling": "0", "bonusSituationDtoList": [
        {"winningConditions": "与开奖号相同且顺序一致", "numberOfWinners": "0", "singleNoteBonus": "1040", "prize": "直选"},
        {"winningConditions": "与开奖号相同，顺序不限", "numberOfWinners": "0", "singleNoteBonus": "346", "prize": "组三"},
        {"winningConditions": "与开奖号相同，顺序不限", "numberOfWinners": "0", "singleNoteBonus": "173", "prize": "组六"}],
           "nationalSales": "0", "currentAward": "0"},
    'QLC': {"rolling": "0", "bonusSituationDtoList": [
        {"winningConditions": "7+0", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "一等奖"},
        {"winningConditions": "6+1", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "二等奖"},
        {"winningConditions": "6+0", "numberOfWinners": "0", "singleNoteBonus": "0", "prize": "三等奖"},
        {"winningConditions": "5+1", "numberOfWinners": "0", "singleNoteBonus": "200", "prize": "四等奖"},
        {"winningConditions": "5+0", "numberOfWinners": "0", "singleNoteBonus": "50", "prize": "五等奖"},
        {"winningConditions": "4+1", "numberOfWinners": "0", "singleNoteBonus": "10", "prize": "六等奖"},
        {"winningConditions": "4+0", "numberOfWinners": "0", "singleNoteBonus": "5", "prize": "七等奖"}],
            "nationalSales": "0", "currentAward": "0"},
}

# data = json.dumps(LOTTO_RESULT['QLC'], ensure_ascii=False)
# print('data', data)


LOTTO_DICT = {
    'gd11x5': 10006,
    'jsk3': 10007,
    'bjkl8': 10014,
    'jx11x5': 10015,
    'js11x5': 10016,
    'ah11x5': 10017,
    'sh11x5': 10018,
    'ln11x5': 10019,
    'hb11x5': 10020,
    'gx11x5': 10022,
    'jl11x5': 10023,
    'nmg11x5': 10024,
    'zj11x5': 10025,
    'gxk3': 10026,
    'jlk3': 10027,
    'hebk3': 10028,
    'nmgk3': 10029,
    'ahk3': 10030,
    'fjk3': 10031,
    'hbk3': 10032,
    # 'bjk3': 10033,
    'tjklsf': 10034,
    # 'bjpks': 10001,
    # 'cqssc': 10002,
    # 'tjssc': 10003,
    # 'xjssc': 10004,
    'gdklsf': 10005,
    # 'sd11x5': 10008,
    'cqklsf': 10009,
    'gxklsf': 10038
}

# 网站彩种 对应  数据库中的彩种
JSH_KEY_DICT = {'bjscpks': 'game_pk10_result', 'gdsyxu': 'game_gd11x5_result', 'ahfceswxw': 'game_aheswxw_result',
                'zjtcesxw': 'game_zjesxw_result', 'fjtcsslxq': 'game_fjsslxq_result',
                'gdnyfcsnxq': 'game_gdfcsslxq_result', 'jsklsc': 'game_gxklsc_result',
                'hbyzfcesxw': 'game_hbfcesxw_result', 'hnzyfceexw': 'game_hnfceexw_result',
                'hljljfceexw': 'game_hljeexw_result', 'hdswxw': 'game_hdswxw_result', 'jstc': 'game_jsqws_result',
                'lnfcswxq': 'game_lnsswxq_result', 'shttcxs': 'game_shttcx4_result', 'gdszfc': 'game_czfc_result',
                'xjfcewxq': 'game_xjfceswxq_result', 'gssyxw': 'game_gssyxw_result', 'gdklsf': 'game_gdklsf_result',
                'gxklsf': 'game_gxklsf_result', 'hbsyxw': 'game_hebsyxw_result', 'hljklmj': 'game_hljklsfmj_result',
                'hubeissyw': 'game_hbsyxw_result', 'jxsyxw': 'game_jxsyxw_result', 'lnklse': 'game_lnklse_result',
                'nmgssc': 'game_nmgssc_result', 'nmgsyxw': 'game_nmgsyxw_result', 'lnsyxw': 'game_lnsyxw_result',
                'jlsyxw': 'game_jlsyxw_result', 'xjsyxw': 'game_xjsyxw_result', 'ynsyxw': 'game_ynsyxw_result',
                'sxsyxw': 'game_shxsyxw_result', 'shanxisyxw': 'game_sxsyxw_result', 'gzssxw': 'game_gzsyxw_result',
                'sxklsf': 'game_shxklsf_result', 'shanxiklsf': 'game_sxklsf_result', 'cqklsf': 'game_cqxync_result',
                'hnklsf': 'game_hnklsf_result', 'hljklsf': 'game_hljklsf_result', 'tjklsf': 'game_tjklsf_result',
                'xjssc': 'game_xjssc_result', 'ynssc': 'game_ynssc_result', 'cqssc': 'game_cqssc_result',
                'tjssc': 'game_tjssc_result', 'gsks': 'game_gsks_result', 'gzks': 'game_gzks_result',
                'gxks': 'game_gxks_result', 'hbks': 'game_hubks_result', 'jxks': 'game_jxks_result',
                'fjks': 'game_fjks_result', 'ahks': 'game_ahks_result', 'jsks': 'game_jsks_result',
                'shks': 'game_shks_result', 'jlks': 'game_jlks_result', 'nmgks': 'game_nmks_result',
                'hebeiks': 'game_hbks_result', 'bjks': 'game_bjks_result', 'hljsyxw': 'game_hljsyxw_result',
                'shsyxw': 'game_shsyxw_result', 'jssyxw': 'game_jssyxw_result', 'zjsyxw': 'game_zjsyxw_result',
                'ahsyxw': 'game_ahsyxw_result', 'fjsyxw': 'game_fjsyxw_result', 'zjklse': 'game_zjklse_result',
                'scklse': 'game_scklse_result', 'shssl': 'game_shssl_result', 'xjxlc': 'game_xjxlc_result',
                'hnxysc': 'game_hnxysc_result', 'sdqyh': 'game_sdqyh_result', 'gxssxw': 'game_gxsyxw_result',
                'sdc': 'game_sdc_result', 'jssc': 'game_jssc_result', 'sgft': 'game_sgft_result',
                'jsssc': 'game_jsssc_result', 'jsft': 'game_jsft_result', 'metxyft': 'game_xyft_result',
                'xyssc': 'game_xyssc_result', 'mssc': 'game_mssc_result', 'msssc': 'game_msssc_result',
                'msft': 'game_msft_result', 'klsc': 'game_klsc_result', 'klft': 'game_klft_result',
                'klssc': 'game_klssc_result', 'ynklsf': 'game_ynklsf_result', 'bjsyxw': 'game_bjsyxw_result',
                'tjsyxw': 'game_tjsyxw_result', 'sdxyxw': 'game_sdsyxw_result', 'hljssc': 'game_hljssc_result',
                'dfljy': 'game_dfljy_result', 'gdnyfchc': 'game_gdnyfchc_result',
                'gdnyfcenxw': 'game_gdnyfcenxw_result', 'xjfcsswxq': 'game_xjfcsswxq_result',
                'xjfcsbxq': 'game_xjfcsbxq_result', 'hbyzfchyce': 'game_hbyzfchyce_result',
                'hbyzfcplw': 'game_hbyzfcplw_result', 'hbyzfcplq': 'game_hbyzfcplq_result',
                'heyzfchycs': 'game_heyzfchycs_result', 'zjtcljy': 'game_zjtcljy_result',
                'fjtceexw': 'game_fjtceexw_result', 'hljtcljy': 'game_hljtcljy_result',
                'hljljfcsnxq': 'game_hljljfcsnxq_result', 'hljfcpne': 'game_hljfcpne_result'}

PKS_KEY_DICT = {'pk10': 'game_pk10_result', 'jspk10': 'game_jssc_result', 'jsft': 'game_jsft_result',
                'sgft': 'game_sgft_result', 'jsssc': 'game_jsssc_result', 'cqssc': 'game_cqssc_result',
                'xyft': 'game_xyft_result', 'xyssc': 'game_xyssc_result', 'tjssc': 'game_tjssc_result',
                'xjssc': 'game_xjssc_result', 'mspk10': 'game_mssc_result', 'klpk10': 'game_klsc_result',
                'klft': 'game_klft_result', 'msft': 'game_msft_result', 'msssc': 'game_msssc_result',
                'klssc': 'game_klssc_result', 'gdkl10': 'game_gdklsf_result', 'xync': 'game_xync_result',
                'jsk3': 'game_jsks_result'}

# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 11:25
# @Author  : TianZe
# @Email   : tianze@86cp.com
# @File    : site_cpyzj.py
# @Software: PyCharm
# @Remarks : 热度数据抓取
import datetime
import os
import sys
import json
import time
import execjs
import logging
import requests
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from packages import yzwl

db = yzwl.DbSession()
mysql = db.yzwl
_logger = logging.getLogger('yzwl_spider')
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
})


def save_to_db(item, db_name):
    info = mysql.select(db_name, condition=[('expect', '=', item['expect']), ('lottery_id', '=', item['lottery_id'])], limit=1)
    if not info:
        # 插入数据
        mysql.insert(db_name, data=item)
        _logger.info('INFO:  DB:%s 数据保存成功, 期号%s ,彩种id：%s;' % (db_name, item['expect'], item['lottery_id']))
    else:
        # 更新热度信息
        mysql.update(db_name, condition=[('expect', '=', item['expect']), ('lottery_id', '=', item['lottery_id'])], data={'hot_data': item['hot_data']})
        _logger.info('INFO:  DB:%s 数据已存在 更新成功, 期号: %s ,彩种id：%s; ' % (db_name, item['expect'], item['lottery_id']))


def save_to_db2(item, db_name):
    info = mysql.select(db_name, condition=[('expect', '=', item['expect'])], limit=1)
    if not info:
        # 插入数据
        mysql.insert(db_name, data=item)
        _logger.info('INFO:  DB:%s 数据保存成功, 期号%s' % (db_name, item['expect']))
    else:
        # 更新热度信息
        # mysql.update(db_name, condition=[('expect', '=', item['expect']), ('lottery_id', '=', item['lottery_id'])], data={'hot_data': item['hot_data']})
        _logger.info('INFO:  DB:%s 数据已存在 不做录入, 期号: %s' % (db_name, item['expect']))


def get_sign(key):
    with open('../scripts/md5.js') as f:
        js_data = f.read()
    ctx = execjs.compile(js_data)
    sign = ctx.call('md5', key)
    return sign


def get_data(lot_code):
    plan_url = 'https://www.cpyzj.com/req/cpyzj/funnyWin/getHotPlanByLotCode'
    hot_url = 'https://www.cpyzj.com/req/cpyzj/funnyWin/getHotNumbers'
    time_stamp = int(time.time()*1000)
    plan_key = 'lotCode={}&timestamp={}&token=noget&key=cC0mEYrCmWTNdr1BW1plT6GZoWdls9b&'.format(lot_code, time_stamp)
    plan_sign = get_sign(plan_key)
    plan_post_data = {
        'token': 'noget',
        'timestamp': time_stamp,
        'lotCode': lot_code,
        'sign': plan_sign.upper()
    }
    plan_r = session.post(plan_url, plan_post_data)
    issue = ''
    lottery_name = ''
    hot_list = []
    if plan_r.status_code == 200:
        content = plan_r.content.decode('utf8')
        plan_dict = json.loads(content)
        for plan_code_dict in plan_dict['data']:
            plan_name = plan_code_dict.get('planName')
            hot_key = 'lotCode={}&planCode={}&timestamp={}&token=noget&key=cC0mEYrCmWTNdr1BW1plT6GZoWdls9b&'.format(
                lot_code, plan_code_dict.get('planCode'), time_stamp)
            hot_sign = get_sign(hot_key)
            post_data = {
                'token': 'noget',
                'timestamp': time_stamp,
                'lotCode': lot_code,
                'planCode': plan_code_dict.get('planCode'),
                'sign': hot_sign.upper()
            }
            hot_r = session.post(hot_url, post_data)
            if hot_r.status_code == 200:
                time.sleep(1)
                content = hot_r.content.decode('utf8')
                hot_dict = json.loads(content)
                request_result = hot_dict.get('msg')
                if request_result == '请求成功':
                    issue = hot_dict['data']['issueNo']
                    lottery_name = hot_dict['data']['lotShortName']
                    hot_result = []
                    for hot_data in hot_dict['data']['lotDvnCont']:
                        num = hot_data['number']
                        hot = hot_data['hot']
                        hot_result.append({
                            'hot_num': num,
                            'hot_count': hot
                        })
                    hot_list.append({
                        'plan_name': plan_name,
                        'lotDvnCont': hot_result
                    })
                else:
                    # 暂无数据，稍后再次请求
                    time.sleep(10)
    result = {
        'lottery_name': lottery_name,
        'hot': hot_list,
    }
    if issue and lottery_name and hot_list:
        return result, issue
    else:
        return


def get_hot_data(lottery_id, lot_code):
    for retry_time in range(1, 4):
        hot_data = get_data(lot_code)
        if hot_data:
            item = {
                'lottery_id': lottery_id,
                'expect': hot_data[1],
                'hot_data': json.dumps(hot_data[0], ensure_ascii=True)
            }
            save_to_db(item, 't_lottery_hot')
            return
        else:
            _logger.warning('彩种id: %s，no data, request time: %d' % (lottery_id, retry_time))


def main(lottery_type, dpc_type=None):
    type_dict = {
        # 低频彩
        'dpc': {
            '1': 'SU_DLT',
            '4': 'CN_PL3',
            '8': 'CN_F2B',
            '11': 'CN_F3D',
            '12': 'CN_7LC',
            '13': 'CN_PL5',
            '14': 'TC_7XC'
        },
        # 11选5
        'x5': {
            '86': 'SH_11C5',
            '89': 'AH_11C5',
            '46': 'JX_11C5',
            '54': 'JL_11C5',
            '7': 'GD_11C5',
            '42': 'HB_11C5',
            '87': 'JS_11C5',
            '52': 'NMG_11C5',
            '112': 'GX_11C5',
            '53': 'LN_11C5',
            '88': 'ZJ_11C5'
        },
        # 时时彩
        'ssc': {
            '68': 'CQ_SSC',
            '66': 'XJ_SSC',
            '69': 'TJ_SSC'
        },
        # 快乐10分
        'h10': {
            '62': 'CQ_HF',
            '35': 'GD_H10',
            '36': 'GX_H10',
            '65': 'TJ_H10'
        },
        # 快3
        'k3': {
            '81': 'JL_K3',
            '78': 'AH_K3',
            '83': 'HEB_K3',
            '74': 'HUB_K3',
            '79': 'JS_K3',
            '82': 'NMG_K3',
            '77': 'FJ_K3',
            '73': 'GX_K3',
            '84': 'BJ_K3'
        }
    }
    if dpc_type:
        get_hot_data(dpc_type, type_dict.get('dpc').get(dpc_type))
    else:
        for key, value in type_dict.get(lottery_type).items():
            get_hot_data(key, value)


def get_open_data(url, post_data):
    r = session.post(url, post_data)
    if r.status_code == 200:
        data = r.json()
        return data


def get_newest_data():
    url = 'https://www.cpyzj.com/req/cpyzj/lotHistory/queryNewestLotByCode'
    time_stamp = int(time.time()*1000)
    key = 'lotCode={}&lotGroupCode={}&timestamp={}&token=noget&key=cC0mEYrCmWTNdr1BW1plT6GZoWdls9b&'.format(10014, 0,
                                                                                                            time_stamp)
    sign = get_sign(key)
    post_data = {
        'token': 'noget',
        'timestamp': time_stamp,
        'lotGroupCode': 0,
        'lotCode': 10014,
        'sign': sign.upper()
    }
    data = get_open_data(url, post_data)


def get_history_data():
    begin_date = datetime.date(2018, 8, 1)
    end_date = datetime.date(2019, 3, 25)
    for i in range((end_date - begin_date).days + 1):
        day = begin_date + datetime.timedelta(days=i)
        date = day.strftime('%Y-%m-%d')
        url = 'https://www.cpyzj.com/req/cpyzj/lotHistory/getLotHistorys'
        time_stamp = int(time.time()*1000)
        key = 'lotCode={}&lotGroupCode={}&pageNo=1&pageSize=100&queryPreDrawTime={}&timestamp={}&token=noget&' \
              'key=cC0mEYrCmWTNdr1BW1plT6GZoWdls9b&'.format(10014, 0, date, time_stamp)
        sign = get_sign(key)
        post_data = {
            'token': 'noget',
            'timestamp': time_stamp,
            'lotCode': 10014,
            'lotGroupCode': 0,
            'queryPreDrawTime': date,
            'pageNo': 1,
            'planSize': 100,
            'sign': sign.upper()
        }
        data = get_open_data(url, post_data)
        results = data['data']
        page_count = data['totalPages']
        for page in range(2, page_count+1):
            key = 'lotCode={}&lotGroupCode={}&pageNo={}&pageSize=100&queryPreDrawTime={}&timestamp={}&token=noget&' \
                  'key=cC0mEYrCmWTNdr1BW1plT6GZoWdls9b&'.format(10014, 0, page, date, time_stamp)
            sign = get_sign(key)
            post_data = {
                'token': 'noget',
                'timestamp': time_stamp,
                'lotCode': 10014,
                'lotGroupCode': 0,
                'queryPreDrawTime': date,
                'pageNo': page,
                'planSize': 100,
                'sign': sign.upper()
            }
            data = get_open_data(url, post_data)
            results += data['data']
        for result in results:
            issue = result['preDrawIssue']
            open_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result['preDrawTime']/1000))
            open_code = result['preDrawCode']
            cp_id = open_code.replace(',', '')
            open_url = 'https://www.cpyzj.com/open-awards-detail.html?lotCode=10014&lotGroupCode=1'
            item = {
                'cp_id': cp_id,
                'expect': issue,
                'open_time': open_time,
                'open_code': open_code,
                'open_url': open_url,
            }
            save_to_db2(item, 'game_bjklb_result')


def cmd():
    lo_type = sys.argv[1]
    if lo_type not in ['dpc', 'x5', 'ssc', 'h10', 'k3']:
        print('请输入正确的参数，如 python site_cpyzj.py x5'
              '对应关系: dpc:低频彩, x5: 11选5, ssc:时时彩, h10:快乐十分, k3:快三')
        sys.exit()
    else:
        if lo_type == 'dpc':
            d_type = sys.argv[2]
            if d_type not in ['dlt', 'ssq', 'fc3d', 'pl3', 'pl5', 'qlc', 'qxc']:
                print('请输入低频彩具体种类，如 python site_cpyzj.py dpc dlt'
                      '对应关系: dlt:大乐透, ssq: 双色球, fc3d:福彩3d, pl3:排列3, pl5:排列5, qlc:七乐彩, qxc:七星彩')
                sys.exit()
            else:
                dpc_dict = {
                    'dlt': '1',
                    'pl3': '4',
                    'pl5': '13',
                    'ssq': '8',
                    'fc3d': '11',
                    'qlc': '12',
                    'qxc': '14'
                }
                main(lo_type, dpc_dict.get(d_type))
        else:
            main(lo_type)


if __name__ == '__main__':
    cmd()

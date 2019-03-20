# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 11:25
# @Author  : TianZe
# @Email   : tianze@86cp.com
# @File    : site_cpyzj.py
# @Software: PyCharm
# @Remarks : 热度数据抓取
import sys
import json
import time
import execjs
import logging
import requests

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


def get_data(lot_code):
    with open('../scripts/md5.js') as f:
        js_data = f.read()
    ctx = execjs.compile(js_data)
    plan_url = 'https://www.cpyzj.com/req/cpyzj/funnyWin/getHotPlanByLotCode'
    hot_url = 'https://www.cpyzj.com/req/cpyzj/funnyWin/getHotNumbers'
    time_stamp = int(time.time()*1000)
    plan_key = 'lotCode={}&timestamp={}&token=noget&key=cC0mEYrCmWTNdr1BW1plT6GZoWdls9b&'.format(lot_code, time_stamp)
    plan_sign = ctx.call('md5', plan_key)
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
            hot_sign = ctx.call('md5', hot_key)
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
                    time.sleep(5)
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


def main(lottery_type):
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
    for key, value in type_dict.get(lottery_type).items():
        get_hot_data(key, value)


if __name__ == '__main__':
    lo_type = sys.argv[1]
    if lo_type not in ['dpc', 'x5', 'ssc', 'h10', 'k3']:
        print('请输入正确的参数，如 python site_cpyzj.py dpc'
              '对应关系: dpc:低频彩, x5: 11选5, ssc:时时彩, h10:快乐十分, k3:快三')
        sys.exit()
    else:
        main(lo_type)

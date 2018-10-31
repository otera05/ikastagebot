import requests
import os
from datetime import datetime

URL = 'https://spla2.yuu26.com/'


def get_schedule(body, query):
    resp = requests.get(URL + query + '/schedule')
    results = resp.json()['result']

    for i, result in enumerate(results):
        body += '```'
        body += '開始日時：' + str(datetime.strptime(result['start'], '%Y-%m-%dT%H:%M:%S').strftime('%Y年%m月%d日%H時%M分～')) + '\n'
        body += 'ルール　：' + result['rule_ex']['name'] + '\n'
        body += 'ステージ：' + result['maps_ex'][0]['name'] + ' と ' + result['maps_ex'][1]['name'] + '\n'
        body += '```'
        body += '\n'
        if i == 2:
            break

    return body


def lambda_handler(event, context):
    # TODO implement
    token = os.environ['TOKEN']

    if event['token'] != token:
        return {
            'statusCode': 200,
            'text': 'トークンエラーです'
        }

    else:
        text = event['text']
        if 'ガチ' in text:
            body = '今後のガチマッチのルールとステージはこれだっ！\n'
            query = 'gachi'
            msg = get_schedule(body, query)

        elif 'ナワバリ' in text:
            body = '今後のナワバリバトルのステージはこれだっ！\n'
            query = 'regular'
            msg = get_schedule(body, query)

        elif 'リグマ' in text:
            body = '今後のリーグマッチのルールとステージはこれだっ！\n'
            query = 'league'
            msg = get_schedule(body, query)

        else:
            msg = 'トリガーワードのあとに「ガチマッチ」「ナワバリ」「リグマ」のいずれかを入力してくれ！'

        return {
            'statusCode': 200,
            'text': msg
        }

import requests
import os
from datetime import datetime

# スプラトゥーン2のステージ情報を提供しているAPI
URL = 'https://spla2.yuu26.com/'

# ヘッダーで User Agent を明記する
HEADERS = {
    'User-Agent': 'ikastagebot(Twitter@otera05)'
}


def get_schedule(body, query):
    """
    ステージAPIにアクセスしてルール・ステージ情報を成形するメソッド
    :param body: Slack で応答させるメッセージ
    :param query: gachi / league / regular のいずれか
    :return: 成形したメッセージ
    """

    try:
        resp = requests.get(URL + query + '/schedule', headers=HEADERS)

        if resp.status_code == 200:
            results = resp.json()['result']

            for i, result in enumerate(results):
                body += '```'
                body += '開始日時：' + str(
                    datetime.strptime(result['start'], '%Y-%m-%dT%H:%M:%S').strftime('%Y年%m月%d日%H時%M分～')) + '\n'
                body += 'ルール　：' + result['rule_ex']['name'] + '\n'
                body += 'ステージ：' + result['maps_ex'][0]['name'] + ' と ' + result['maps_ex'][1]['name'] + '\n'
                body += '```'
                body += '\n'
                if i == 2:
                    break
        else:
            body = 'ステージAPIへのアクセスに失敗しました。\n' \
                   '時間をおいて再度試してください。'

    except requests.exceptions.RequestException as e:
        body = 'ステージAPIへのアクセス時に例外が発生しました。\n' \
               '時間をおいて再度試してください。'

    return body


def lambda_handler(event, context):
    token = os.environ['TOKEN']

    # Outgoing Webhooks のトークンを参照し、
    # 想定している Slack チームからのアクセスかを判別する
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

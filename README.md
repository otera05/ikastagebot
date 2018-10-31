# ikastagebot

### 概要
SlackのIncoming Webhooksを利用したスプラトゥーン2のステージ情報を答えてくれるBotスクリプト。  
実行環境はAWS Lambdaを想定しています。


### 使い方
1. `git clone [URL]`  
2. `pip install -r requirements.txt`
3.  Slack で Incoming Webhooks を作成する  
4. プロジェクトをzip圧縮してLambdaにデプロイ  
5. API Gatewayを作成してLambdaと連携
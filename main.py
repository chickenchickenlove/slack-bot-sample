from slack_bolt.adapter.sanic import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp
from sanic import Sanic
BOT_TOKEN = ''
SINGING_SECRET = ''


# Bolt App 생성
app = AsyncApp(token=BOT_TOKEN,
               signing_secret=SINGING_SECRET)
CLIENT = app.client
# Sanic 서버로 들어온 요청 → Bolt 요청으로 바꿔주는 핸들러
handler = AsyncSlackRequestHandler(app)

# sanice 서버 생성
sanic_server = Sanic(name='bot')


# bolt에 데코레이터로 처리할 것 추가.
@app.message("hello")
async def message_hello(message, say):
    # CLIENT를 불러와서 메세지 가능함.
    await CLIENT.chat_postMessage(channel=message['channel'], text="hello200002")

    # 응답을 say() 펑션으로 처리함.
    await say(f'Hey there <@{message["user"]}>!')


# sanic 서버에 라우팅 경로 추가.
@sanic_server.route('/slack/events', methods=["POST"])
async def slack_event(request):
    return await handler.handle(request)

# sanic 서버가 들어오면, port 이쪽으로 요청이 들어온다.
if __name__ == "__main__":
    sanic_server.run(port=12000)

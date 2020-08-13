from .main import get_app

import aio_pika
import asyncio

from email_service.models.templates import Templates
from . import config

from email.message import EmailMessage
import aiosmtplib

app = get_app()


async def send_email(message: aio_pika.IncomingMessage):
    async with message.process():
        # default
        data2_default = {"from" : "ssnk@le-memese.com",
                        "to" : "ssnk@le-memese.com",
                        "sub" : ""}

        # from message in bytes
        data_from_mes_b = message.info()["headers"]
        data_from_mes = {}
        for item in data_from_mes_b.keys():
            data_from_mes[item] = data_from_mes_b[item].decode("utf8")

        # merge
        data = {**data2_default, **data_from_mes}

        # get template
        tmplt = await Templates.query.where(Templates.name == data["template"]).gino.first()

        # create email
        em = EmailMessage()
        em["From"] = data["from"]  # "ssnk@le-memese.com"
        em["To"] = data["to"]  # "ssnk@le-memese.com"
        em["Subject"] = data["sub"]  # "Hello World!"
        em.set_content(tmplt.body.format(**data))

        # send
        await aiosmtplib.send(
            em,
            hostname="smtp.yandex.ru",
            port=465,
            username=str(config.EMAIL_LOGIN),
            password=str(config.EMAIL_PASS),
            use_tls=True)


async def consuming(loop):
    connection = await aio_pika.connect_robust(
        "amqp://test:test@rabbit/", loop=loop, port=5672,
    )

    queue_name = "send_email"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be
    # processing at the same time.
    await channel.set_qos(prefetch_count=100)

    queue = await channel.declare_queue(queue_name)

    await queue.consume(send_email)

    print("end consuming")


# async def pp():
#     print("tick")
#     asyncio.sleep(1000)
#
#
# async def testing(loop):
#
#     while True:
#         await pp()
#
#     print("end consuming")


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    asyncio.create_task(consuming(loop))

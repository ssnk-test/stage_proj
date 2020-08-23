import aio_pika
import asyncio
from email.message import EmailMessage
import aiosmtplib

from email_service.models.templates import Templates
from email_service import config
from email_service.main import get_app
app = get_app()


async def send_email(message: aio_pika.IncomingMessage):
    async with message.process():
        # default
        data2_default = {"from": "ssnk@le-memese.com",
                         "to": "ssnk@le-memese.com",
                         "sub": ""}

        # from message in bytes
        data_from_mes_b = message.info()["headers"]
        data_from_mes = {}
        for item in data_from_mes_b.keys():
            data_from_mes[item] = data_from_mes_b[item].decode("utf8")

        # merge
        data = {**data2_default, **data_from_mes}

        # get template
        tmplt = await Templates.query.where(
            Templates.name == data["template"]).gino.first()

        # create email
        em = EmailMessage()
        em["From"] = data["from"]
        em["To"] = data["to"]
        em["Subject"] = data["sub"]
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
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(queue_name)
    await queue.consume(send_email)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    asyncio.create_task(consuming(loop))

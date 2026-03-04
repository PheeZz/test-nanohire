from aio_pika import connect_robust
from aio_pika.patterns import RPC

from core import settings


async def remote_method(string: str):
    # DO SOMETHING
    # Move this method along with others to another place e.g. app/rpc_methods
    # I put it here for simplicity
    return f"It works! {string}"


async def consume(loop):
    connection = await connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
        loop=loop,
    )
    channel = await connection.channel()
    rpc = await RPC.create(channel)

    await rpc.register("remote_method", remote_method, auto_delete=True)
    return connection

import asyncio
from scheduler import notification_scheduler
from notification_service import notification_service
from loguru import logger
from asyncio.exceptions import CancelledError


async def run_manual_test():
    logger.debug("🧪 Запуск тестовой рассылки уведомлений...")
    await notification_service.process_notifications()


async def main():
    logger.debug("Запуск сервиса уведомлений")

    # await run_manual_test()

    notification_scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit, CancelledError):
        notification_scheduler.stop()
        logger.debug("Сервис уведомлений остановлен")


if __name__ == "__main__":
    asyncio.run(main())

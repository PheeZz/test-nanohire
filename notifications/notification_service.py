"""
В целом можно было бы реализовать чуть более устойчиво/распределенно.
Я бы предложил следующую механику:
1. Шедулер запускает задачу по получению данных для рассылки
2. Кладет эти данные в rmq в N сообщений. 1 уведомление = 1 сообщение.
В сообщении указывается имя менеджера и количество новых откликов.
3. В этом же репозитории есть consumer, который слушает очередь и обрабатывает эти сообщения.
Он может быть запущен в нескольких экземплярах для горизонтального масштабирования.
 Дедупликация по id сообщения, там может быть id менеждера
"""

import asyncio

from api_client import api_client
from loguru import logger

from config import settings
from exceptions import SomeSendNotificationException
import itertools


class NotificationService:
    @staticmethod
    def format_notification_message(manager_name: str, count: int) -> str:
        return f"Здравствуйте, {manager_name}! У вас {count} новых откликов, требующих обработки."

    @staticmethod
    async def send_notification(manager_name: str, message: str) -> None:
        logger.debug(f"Отправка письма для {manager_name}:")
        logger.success(message)

    async def process_notifications(self) -> None:
        logger.info("Запуск задачи рассылки уведомлений...")

        notifications = await api_client.get_manager_notifications()

        if not notifications:
            logger.warning("Нет данных для отправки уведомлений.")
            return

        logger.info(f"Получено данных о {len(notifications)} менеджерах.")

        coros = [
            self.send_notification(manager_name, notification)
            for manager_name, notification in notifications
        ]
        for batch in itertools.batched(coros, settings.NOTIFICATION_BATCH_SIZE):
            await asyncio.gather(*batch)

        logger.debug("Задача рассылки уведомлений завершена.")

    async def process_single_notification(self, manager_name: str, count: int) -> None:
        """Process a single notification for testing purposes."""
        if count > 0:
            message = self.format_notification_message(manager_name, count)
            try:
                await self.send_notification(manager_name, message)
            except SomeSendNotificationException as e:
                logger.error(f"Ошибка при отправке уведомления для {manager_name}:")
                logger.exception(e)
                # тут на самом деле можно вернуть статус ошибки для подведения статистики
                # сколько успшных, сколько неудачных отправок
                # по результатам записать в бд, сделать отдельную задачу,
                # которая бы пробовала повторно отправить неудачные уведомления
        else:
            logger.warning(f"У менеджера {manager_name} нет новых откликов.")

        return None


notification_service = NotificationService()

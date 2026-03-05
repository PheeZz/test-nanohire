from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import settings
from notification_service import notification_service
from loguru import logger


class NotificationScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=settings.SCHEDULER_TIMEZONE)

    def start(self):
        trigger = CronTrigger(
            day_of_week="mon-fri",
            hour=settings.SCHEDULER_HOUR,
            minute=settings.SCHEDULER_MINUTE,
            timezone=settings.SCHEDULER_TIMEZONE,
        )

        self.scheduler.add_job(
            self._run_notification_task,
            trigger=trigger,
            id="daily_notifications",
            name="Ежедневная рассылка уведомлений",
            replace_existing=True,
        )

        logger.debug("Планировщик запущен.")
        logger.info(
            f"Задача будет выполняться: Пн-Пт в "
            f"{settings.SCHEDULER_HOUR}:{settings.SCHEDULER_MINUTE:02d}"
            f" ({settings.SCHEDULER_TIMEZONE})"
        )

        self.scheduler.start()

    @staticmethod
    async def _run_notification_task():
        await notification_service.process_notifications()

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()


notification_scheduler = NotificationScheduler()

from pydantic import BaseModel


class NotificationManagerInfo(BaseModel):
    manager_name: int
    notifications_count: int


class NotificationPerManagerResponse(BaseModel):
    notifications: list[NotificationManagerInfo]

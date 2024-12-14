import datetime as DT
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy.util import await_only

from database import requests as rq
import asyncio
from threading import Timer

from filter.filter_group import parse_time


async def repeater(interval, function):
    Timer(interval, repeater[interval, function]).start()
    function()


async def verification_sum_warn(tg_id: int):
    user = await rq.get_user_tg_id(tg_id = tg_id)
    elements = []
    warn =  user.warn
    elements = warn.split()
    for i, element in enumerate(elements):
        if element == "warn" and i + 1 < len(elements):  # Сравниваем с 'warn' и проверяем следующий элемент
            elements.append(elements[i])
    return len(elements)


async  def pruf_sum_warn(tg_id: int):
    sum_warn = await verification_sum_warn(tg_id=tg_id)
    if sum_warn == 5:
        return 0
    else :
        return 1


async  def parse_warn_time():
    users = await rq.get_users()
    elements = []
    for user in users:
        warn = user.warn
        elements = warn.split()
        for i, element in enumerate(elements):
            if element == "warn" and i + 1 < len(elements):  # Сравниваем с 'warn' и проверяем следующий элемент
                elements.append(elements[i+1])
                elements.append(elements[i + 2])
        current_time = DT.now()
        for i in range(0, len(elements), 2):
                # Получаем дату и время как строку
                date_str = elements[i]
                time_str = elements[i + 1]
                # Формируем целое значение даты и времени
                datetime_str = f"{date_str} {time_str}"
                event_time = DT.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")  # Замените формат на ваш

                # Сравниваем с текущим временем
                if current_time > event_time:
                    print(1)  # Текущее время больше
                else:
                    print(0)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(minute="*/15")
    scheduler.start()
    await parse_time()
import asyncio
import time

async_mode = True  # Режим работы: True - асинхронно, False - синхронно


def showjob(jobname): # текущая задача
    curtime = time.perf_counter() - start_time
    print(f"{curtime:.2f}:\t{jobname}")


async def PackClothes(): # сбор вещей в рюкзак
    showjob("РЮКЗАК: Достаём рюкзак")
    await asyncio.sleep(0.5) if async_mode else time.sleep(0.5)
    showjob("РЮКЗАК: Складываем одежду и вещи")
    await asyncio.sleep(1) if async_mode else time.sleep(1)
    showjob("РЮКЗАК: Проверяем список вещей")
    await asyncio.sleep(1) if async_mode else time.sleep(1)


async def PackFood(): # сбор контейнеров с едой
    showjob("ЕДА: Достаём контейнеры и продукты")
    await asyncio.sleep(0.5) if async_mode else time.sleep(0.5)
    showjob("ЕДА: Готовим бутерброды")
    await asyncio.sleep(1) if async_mode else time.sleep(1)
    showjob("ЕДА: Упаковываем продукты в контейнеры")
    await asyncio.sleep(1.5) if async_mode else time.sleep(1.5)
    showjob("ЕДА: Складываем контейнеры в рюкзак")
    await asyncio.sleep(0.5)


async def CheckEquipment(): # проверка снаряжения
    showjob("СНАРЯЖЕНИЕ: Проверяем палатку")
    await asyncio.sleep(0.5) if async_mode else time.sleep(0.5)
    showjob("СНАРЯЖЕНИЕ: Проверяем спальник")
    await asyncio.sleep(0.5) if async_mode else time.sleep(0.5)
    showjob("СНАРЯЖЕНИЕ: Проверяем фонарик")
    await asyncio.sleep(1) if async_mode else time.sleep(1)
    showjob("СНАРЯЖЕНИЕ: Складываем всё в рюкзак")


async def CloseBackpack(): # конечный этап, закрытие рюкзака
    showjob("РЮКЗАК: Закрываем рюкзак")
    await asyncio.sleep(0.5) if async_mode else time.sleep(0.5)


async def main():
    task_clothes = asyncio.create_task(PackClothes())
    task_food = asyncio.create_task(PackFood())
    task_equipment = asyncio.create_task(CheckEquipment())

    await asyncio.gather(task_clothes, task_equipment) # завершение упаковки
    await task_food # проверка еды

    await CloseBackpack() # после всего можно закрыть рюкзак


start_time = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - start_time

print(f"Подготовка к походу завершена за {round(elapsed, 2)} минут") # время подготовки

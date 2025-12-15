# data_management.py

"""
Модуль для управления вводом и генерацией исходных массивов данных.
Содержит функции для ручного ввода чисел пользователем и автоматической
генерации случайных массивов для тестирования.
"""

import random
import logging
# Импортируем настройку логирования, чтобы она выполнилась при запуске
try:
    from logging_setup import setup_logging
except ImportError:
    # Если logging_setup.py не найден (например, при прямом запуске этого файла),
    # логирование будет использовать базовую конфигурацию.
    pass

logger = logging.getLogger(__name__) # Инициализация логгера для этого модуля

def manual_input():
    """
    Запрашивает у пользователя ввод трех массивов чисел через консоль.
    ...
    """
    logger.info("Действие сервера: Вызвана функция manual_input для ручного ввода данных.")
    print("--- Ручной ввод массивов (числа через запятую) ---")
    try:
        arr1_str = input("Введите числа для массива 1: ")
        arr2_str = input("Введите числа для массива 2: ")
        arr3_str = input("Введите числа для массива 3: ")

        # Попытка преобразования в float может вызвать ValueError
        arr1 = [float(x.strip()) for x in arr1_str.split(',') if x.strip()]
        arr2 = [float(x.strip()) for x in arr2_str.split(',') if x.strip()]
        arr3 = [float(x.strip()) for x in arr3_str.split(',') if x.strip()]

        # Проверка, что массивы одинаковой длины 
        if not (len(arr1) == len(arr2) == len(arr3)) or not arr1:
            # Генерация пользовательского исключения, которое будет перехвачено ниже
            raise ValueError("Массивы должны быть непустыми и одинаковой длины.") 

        logger.info(f"Действие сервера: Успешно введены массивы, длина: {len(arr1)}")
        return arr1, arr2, arr3
        
    except ValueError as e:
        # Перехват ошибки преобразования или сгенерированного исключения
        logger.error(f"Действие сервера: Ошибка при вводе данных. {e}") 
        print(f"\n❌ Ошибка ввода: {e}. Пожалуйста, используйте только числа, разделенные запятыми, и убедитесь, что все три массива одинаковой длины.")
        return None, None, None
    except Exception as e:
        # Перехват любых других неожиданных ошибок
        logger.error(f"Действие сервера: Непредвиденная ошибка при вводе данных: {e}")
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")
        return None, None, None


def generate_random_arrays(size=5, min_val=1, max_val=10):
    """
    Генерирует три массива заданной длины со случайными целыми числами.

    Args:
        size (int): Длина каждого из трех массивов. По умолчанию 5.
        min_val (int): Минимальное возможное значение числа. По умолчанию 1.
        max_val (int): Максимальное возможное значение числа. По умолчанию 10.

    Returns:
        tuple[list[int], list[int], list[int]]: Кортеж из трех списков случайных чисел (arr1, arr2, arr3).
    """
    logger.info(f"Действие сервера: Вызвана функция generate_random_arrays. Генерация {size} элементов.")
    print(f"--- Генерация {size} случайных массивов ({min_val} до {max_val}) ---")
    arr1 = [random.randint(min_val, max_val) for _ in range(size)]
    arr2 = [random.randint(min_val, max_val) for _ in range(size)]
    arr3 = [random.randint(min_val, max_val) for _ in range(size)]
    logger.info("Действие сервера: Случайные массивы успешно сгенерированы.")
    return arr1, arr2, arr3


if __name__ == '__main__':
    # Тестирование ручного ввода
    # Примечание: При запуске через __main__ логирование будет использовать базовую/консольную конфигурацию.
    # Для полной конфигурации с файлом, запускайте через main.py
    a1, a2, a3 = manual_input()
    if a1:
        print(f"Ручной ввод: {a1}, {a2}, {a3}")

    print("-" * 20)

    # Тестирование генерации
    g1, g2, g3 = generate_random_arrays(size=4)
    print(f"Генерация: {g1}, {g2}, {g3}")
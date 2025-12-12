# data_management.py

"""
Модуль для управления вводом и генерацией исходных массивов данных.
Содержит функции для ручного ввода чисел пользователем и автоматической
генерации случайных массивов для тестирования.
"""

import random

def manual_input():
    """
    Запрашивает у пользователя ввод трех массивов чисел через консоль.
    
    Массивы должны быть непустыми и иметь одинаковую длину, чтобы соответствовать
    требованиям основного алгоритма (последовательная проверка элементов).

    Returns:
        tuple[list[float], list[float], list[float]]: Кортеж из трех списков чисел (arr1, arr2, arr3).
        Если ввод некорректен (разная длина, нечисловые значения или пустые массивы), 
        возвращает (None, None, None).
    """
    print("--- Ручной ввод массивов (числа через запятую) ---")
    try:
        arr1_str = input("Введите числа для массива 1: ")
        arr2_str = input("Введите числа для массива 2: ")
        arr3_str = input("Введите числа для массива 3: ")

        arr1 = [float(x.strip()) for x in arr1_str.split(',') if x.strip()]
        arr2 = [float(x.strip()) for x in arr2_str.split(',') if x.strip()]
        arr3 = [float(x.strip()) for x in arr3_str.split(',') if x.strip()]

        # Проверка, что массивы одинаковой длины (требование задания)
        if not (len(arr1) == len(arr2) == len(arr3)) or not arr1:
            print("Ошибка: Массивы должны быть непустыми и одинаковой длины.")
            return None, None, None

        return arr1, arr2, arr3
    except ValueError:
        print("Ошибка: Введенные данные содержат нечисловые значения.")
        return None, None, None


def generate_random_arrays(size=5, min_val=1, max_val=10):
    """
    Генерирует три массива одинаковой длины со случайными целыми числами.

    Args:
        size (int): Длина каждого из трех массивов. По умолчанию 5.
        min_val (int): Минимальное возможное значение числа (включительно). По умолчанию 1.
        max_val (int): Максимальное возможное значение числа (включительно). По умолчанию 10.

    Returns:
        tuple[list[int], list[int], list[int]]: Кортеж из трех списков случайных чисел (arr1, arr2, arr3).
    """
    print(f"--- Генерация {size} случайных массивов ({min_val} до {max_val}) ---")
    arr1 = [random.randint(min_val, max_val) for _ in range(size)]
    arr2 = [random.randint(min_val, max_val) for _ in range(size)]
    arr3 = [random.randint(min_val, max_val) for _ in range(size)]
    return arr1, arr2, arr3


if __name__ == '__main__':
    # Тестирование ручного ввода
    a1, a2, a3 = manual_input()
    if a1:
        print(f"Ручной ввод: {a1}, {a2}, {a3}")

    print("-" * 20)

    # Тестирование генерации
    g1, g2, g3 = generate_random_arrays(size=4)
    print(f"Генерация: {g1}, {g2}, {g3}")
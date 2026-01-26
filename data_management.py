import random
import logging

logger = logging.getLogger(__name__)

def manual_input():
    print("\n--- Ручной ввод (числа через запятую) ---")
    try:
        # Применение ФП: Лямбда-функция для парсинга строки в список чисел
        # Использует strip() и проверку на пустоту внутри спискового включения
        parse_line = lambda s: [float(x.strip()) for x in s.split(',') if x.strip()]
        
        arr1 = parse_line(input("Введите массив 1: "))
        arr2 = parse_line(input("Введите массив 2: "))
        arr3 = parse_line(input("Введите массив 3: "))

        if not (len(arr1) == len(arr2) == len(arr3)) or not arr1:
            raise ValueError("Массивы должны быть непустыми и одинаковой длины.") 

        return arr1, arr2, arr3
    except ValueError as e:
        print(f"❌ Ошибка ввода: {e}")
        return None, None, None

def generate_random_arrays(size=3):
    """
    Применение ФП: Использование лямбды для инкапсуляции логики генерации.
    """
    gen = lambda: [random.randint(1, 10) for _ in range(size)]
    return gen(), gen(), gen()
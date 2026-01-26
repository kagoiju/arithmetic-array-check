import logging

logger = logging.getLogger(__name__)

def check_arithmetic_possibility(a, b, target):
    """
    Применение ФП: Использование списка анонимных функций (лямбд).
    Каждая лямбда — это чистая функция, выполняющая одну операцию.
    """
    # Список кортежей: (лямбда-функция, строковое описание операции)
    operations = [
        (lambda x, y: x + y, f"{a} + {b}"),
        (lambda x, y: x - y, f"{a} - {b}"),
        (lambda x, y: y - x, f"{b} - {a}"),
        (lambda x, y: x * y, f"{a} * {b}"),
        # Для деления используем тернарный оператор внутри лямбды для безопасности
        (lambda x, y: x / y if y != 0 else None, f"{a} / {b}"),
        (lambda x, y: y / x if x != 0 else None, f"{b} / {a}")
    ]

    # Функциональный перебор: применяем каждую функцию к аргументам
    for op_func, explanation in operations:
        try:
            result = op_func(a, b)
            if result is not None and result == target:
                return True, explanation
        except (ZeroDivisionError, TypeError):
            continue
            
    return False, None

def process_arrays(arr1, arr2, arr3):
    """
    Применение ФП: Использование zip() для параллельной итерации 
    и спискового включения (list comprehension) для формирования результата.
    """
    if not (len(arr1) == len(arr2) == len(arr3)):
        logger.error("Массивы разной длины.")
        return "Ошибка: Массивы должны быть одинаковой длины."

    # Декларативное создание списка результатов
    results = [
        {
            'target': t, 'a': a, 'b': b,
            'found': res[0], 'explanation': res[1]
        }
        for a, b, t in zip(arr1, arr2, arr3)
        # Вызываем функцию один раз для каждого набора данных
        for res in [check_arithmetic_possibility(a, b, t)]
    ]
    
    return results
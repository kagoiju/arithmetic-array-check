# core_algorithm.py

"""
Модуль, содержащий основную логику проверки арифметической возможности.
Функции проверяют, можно ли получить число из третьего массива, 
используя арифметические операции (+, -, *, /) с соответствующими числами из первых двух,
проверяя их последовательно.
"""

import logging
# Импортируем настройку логирования
try:
    from logging_setup import setup_logging
except ImportError:
    pass

logger = logging.getLogger(__name__)

def check_arithmetic_possibility(a, b, target):
    """
    Проверяет, можно ли получить 'target' из чисел 'a' и 'b' с помощью 
    основных арифметических операций (+, -, *, /). 
    
    Учитывает перестановку операндов для вычитания и деления.
    Исключает деление на ноль.

    Args:
        a (float): Первое исходное число.
        b (float): Второе исходное число.
        target (float): Целевое число, которое нужно получить.

    Returns:
        tuple[bool, str | None]: Кортеж, содержащий: 
                                1. bool: True, если 'target' может быть получен; False в противном случае.
                                2. str: Строка-объяснение операции (напр., "5 + 3"), если найдена, или None.
    """
    # Сложение
    if a + b == target:
        return True, f"{a} + {b}"
    
    # Вычитание
    if a - b == target:
        return True, f"{a} - {b}"
    if b - a == target:
        return True, f"{b} - {a}"
        
    # Умножение
    if a * b == target:
        return True, f"{a} * {b}"

    # Деление (с проверкой на ноль)
    # Используем DEBUG для логирования внутренних проверок
    if b != 0:
        if a / b == target:
            return True, f"{a} / {b}"
    else:
        logger.debug(f"Проверка деления: Пропущено деление {a} / {b} (деление на ноль).")
        
    if a != 0:
        if b / a == target:
            return True, f"{b} / {a}"
    else:
        logger.debug(f"Проверка деления: Пропущено деление {b} / {a} (деление на ноль).")

    return False, None

def process_arrays(arr1, arr2, arr3):
    """
    Последовательно обрабатывает элементы трех массивов и применяет 
    функцию check_arithmetic_possibility к каждой тройке чисел.

    Требует, чтобы массивы arr1, arr2 и arr3 были одинаковой длины.

    Args:
        arr1 (list[float]): Первый массив чисел.
        arr2 (list[float]): Второй массив чисел.
        arr3 (list[float]): Третий (целевой) массив чисел.

    Returns:
        list[dict] | str: Список словарей с результатами проверки для каждой тройки чисел
                          или строка с сообщением об ошибке, если массивы разной длины.
    """
    logger.info("Действие сервера: Вызвана функция process_arrays для выполнения алгоритма.")
    
    if not (len(arr1) == len(arr2) == len(arr3)):
        logger.error("Действие сервера: Сбой алгоритма. Массивы разной длины.")
        return "Ошибка: Массивы должны быть одинаковой длины."

    results = []
    logger.info(f"Действие сервера: Начинается последовательная проверка {len(arr1)} пар чисел.")
    
    for i, (a, b, target) in enumerate(zip(arr1, arr2, arr3)):
        found, explanation = check_arithmetic_possibility(a, b, target)
        
        # Логирование на уровне DEBUG для детального отслеживания каждой итерации
        if found:
            logger.debug(f"Действие сервера: Проверка #{i+1} ({a}, {b}) -> {target}. Успех: {explanation}")
        else:
            logger.debug(f"Действие сервера: Проверка #{i+1} ({a}, {b}) -> {target}. Неудача.")
            
        results.append({
            'target': target,
            'a': a,
            'b': b,
            'found': found,
            'explanation': explanation
        })
        
    logger.info("Действие сервера: Алгоритм проверки успешно завершен.")
    return results


if __name__ == '__main__':
    # Тестирование основного алгоритма
    A = [5, 10, 20]
    B = [3, 2, 4]
    C = [8, 5, 80] 

    logger.warning("Запуск модуля core_algorithm.py в режиме тестирования (через __main__).")

    print(f"Массивы для теста: A={A}, B={B}, C={C}")
    test_results = process_arrays(A, B, C)

    for res in test_results:
        if res['found']:
            print(f"✅ {res['target']} можно получить из {res['a']} и {res['b']}: {res['explanation']} = {res['target']}")
        else:
            print(f"❌ {res['target']} НЕЛЬЗЯ получить из {res['a']} и {res['b']}")
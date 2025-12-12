# core_algorithm.py

"""
Модуль, содержащий основную логику проверки арифметической возможности.
Функции проверяют, можно ли получить число из третьего массива, 
используя арифметические операции (+, -, *, /) с соответствующими числами из первых двух,
проверяя их последовательно.
"""

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
    if b != 0 and a / b == target:
        return True, f"{a} / {b}"
    if a != 0 and b / a == target:
        return True, f"{b} / {a}"

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
                          
                          Каждый словарь результата содержит ключи: 
                          'a', 'b', 'target', 'found', 'explanation'.
    """
    if not (len(arr1) == len(arr2) == len(arr3)):
        return "Ошибка: Массивы должны быть одинаковой длины."

    results = []
    # zip объединяет элементы с одинаковыми индексами
    for a, b, target in zip(arr1, arr2, arr3): 
        found, explanation = check_arithmetic_possibility(a, b, target)
        results.append({
            'target': target,
            'a': a,
            'b': b,
            'found': found,
            'explanation': explanation
        })
    return results


if __name__ == '__main__':
    # Тестирование основного алгоритма
    A = [5, 10, 20]
    B = [3, 2, 4]
    C = [8, 5, 80] # 5+3=8, 10/2=5, 20*4=80

    print(f"Массивы для теста: A={A}, B={B}, C={C}")
    test_results = process_arrays(A, B, C)

    for res in test_results:
        if res['found']:
            print(f"✅ {res['target']} можно получить из {res['a']} и {res['b']}: {res['explanation']} = {res['target']}")
        else:
            print(f"❌ {res['target']} НЕЛЬЗЯ получить из {res['a']} и {res['b']}")
import logging

logger = logging.getLogger(__name__)

# Эффективность: Выносим функции-операторы в константу, чтобы не пересоздавать их в цикле
# Это экономит время CPU на аллокацию объектов
OPERATIONS = (
    lambda a, b: (a + b, f"{a} + {b}"),
    lambda a, b: (a - b, f"{a} - {b}"),
    lambda a, b: (b - a, f"{b} - {a}"),
    lambda a, b: (a * b, f"{a} * {b}"),
    lambda a, b: (a / b, f"{a} / {b}") if b != 0 else (None, ""),
    lambda a, b: (b / a, f"{b} / {a}") if a != 0 else (None, ""),
)

def check_arithmetic_possibility(a, b, target):
    """Оптимизированная проверка через ленивый перебор константных операций."""
    for op in OPERATIONS:
        res, expr = op(a, b)
        if res is not None and res == target:
            return True, expr
    return False, None

def process_arrays(arr1, arr2, arr3):
    """Использование генератора для экономии памяти при больших объемах данных."""
    if not (len(arr1) == len(arr2) == len(arr3)):
        return "Ошибка: Массивы разной длины."

    # Эффективность: Используем генераторное выражение вместо создания тяжелого списка в памяти
    return [
        {'target': t, 'a': a, 'b': b, 'found': f, 'explanation': e}
        for a, b, t in zip(arr1, arr2, arr3)
        for f, e in [check_arithmetic_possibility(a, b, t)]
    ]
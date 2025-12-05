# core_algorithm.py

def check_arithmetic_possibility(a, b, target):
    """
    Проверяет, можно ли получить target из a и b с помощью +, -, *, /.
    Возвращает: (bool, operation_str)
    """
    if a + b == target:
        return True, f"{a} + {b}"
    if a - b == target:
        return True, f"{a} - {b}"
    if b - a == target:
        return True, f"{b} - {a}"
    if a * b == target:
        return True, f"{a} * {b}"

    # Проверка деления, исключая деление на ноль
    if b != 0 and a / b == target:
        return True, f"{a} / {b}"
    if a != 0 and b / a == target:
        return True, f"{b} / {a}"

    return False, None

def process_arrays(arr1, arr2, arr3):
    """
    Проверяет, можно ли получить элементы arr3 из arr1 и arr2
    последовательными арифметическими преобразованиями.
    Возвращает: Список результатов [(target, found, explanation), ...]
    """
    if not (len(arr1) == len(arr2) == len(arr3)):
        return "Ошибка: Массивы должны быть одинаковой длины."

    results = []
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
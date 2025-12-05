# main.py

from data_management import manual_input, generate_random_arrays
from core_algorithm import process_arrays

# Глобальные переменные для хранения состояния
current_data = None  # (arr1, arr2, arr3)
current_results = None

def display_menu():
    print("\n" + "="*40)
    print("🔢 Консольное приложение для проверки массивов")
    print("="*40)
    print("1. Ввод исходных данных (вручную/генерация)")
    print("2. Выполнение алгоритма по заданию")
    print("3. Вывод результата")
    print("4. Завершение работы программы")
    print("-" * 40)

def handle_data_input():
    global current_data, current_results

    print("\n--- Выбор метода ввода данных ---")
    print("1. Ручной ввод")
    print("2. Случайная генерация (размер 5)")

    choice = input("Выберите (1 или 2): ")

    new_data = None
    if choice == '1':
        new_data = manual_input()
    elif choice == '2':
        new_data = generate_random_arrays(size=5)
    else:
        print("Некорректный выбор.")
        return

    if new_data and all(new_data):
        current_data = new_data
        current_results = None  # Сброс результатов при вводе новых данных

        arr1, arr2, arr3 = current_data
        print("\n✅ Данные успешно введены.")
        print(f"Массив 1: {arr1}")
        print(f"Массив 2: {arr2}")
        print(f"Массив 3: {arr3}")
    else:
        print("\n❌ Ввод данных не удался. Пожалуйста, попробуйте снова.")


def handle_algorithm_execution():
    global current_data, current_results

    if current_data is None:
        print("\n❌ Алгоритм не может быть выполнен без введенных данных. Сначала введите данные (Пункт 1).")
        return

    arr1, arr2, arr3 = current_data
    print("\n--- Запуск алгоритма ---")
    current_results = process_arrays(arr1, arr2, arr3)

    if isinstance(current_results, str):
        print(f"❌ Ошибка при обработке: {current_results}")
        current_results = None
    else:
        print("✅ Алгоритм успешно выполнен. Результаты готовы к выводу (Пункт 3).")


def handle_output():
    global current_results

    if current_results is None:
        print("\n❌ Результат не может быть выведен без обработки введенных данных. Сначала выполните алгоритм (Пункт 2).")
        return

    print("\n" + "="*40)
    print("📈 РЕЗУЛЬТАТЫ ПРОВЕРКИ АРИФМЕТИЧЕСКИХ ПРЕОБРАЗОВАНИЙ")
    print("="*40)

    for res in current_results:
        a, b, target = res['a'], res['b'], res['target']
        if res['found']:
            print(f"✅ Target {target} (из {a}, {b}): Можно получить. Пример: {res['explanation']} = {target}")
        else:
            print(f"❌ Target {target} (из {a}, {b}): НЕЛЬЗЯ получить арифметически.")
    print("-" * 40)


def main():
    while True:
        display_menu()
        choice = input("Введите номер пункта меню: ")

        if choice == '1':
            handle_data_input()
        elif choice == '2':
            handle_algorithm_execution()
        elif choice == '3':
            handle_output()
        elif choice == '4':
            print("\n👋 Завершение работы программы. До свидания!")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите пункт от 1 до 4.")


if __name__ == '__main__':
    main()
# main.py

"""
Основной модуль консольного приложения. 
Реализует текстовое меню и управляет состоянием программы (введенные данные и результаты).
Обеспечивает выполнение операций в правильной последовательности и логирование активности.
"""

from data_management import manual_input, generate_random_arrays
from core_algorithm import process_arrays
import logging
import sys

# Импортируем настройку логирования для переключения уровней
from logging_setup import setup_logging 

logger = logging.getLogger(__name__)

# Глобальные переменные для хранения состояния
current_data = None  # (arr1, arr2, arr3) - Хранит данные после ввода.
current_results = None # Хранит результаты после выполнения алгоритма.

def display_menu():
    """
    Выводит на консоль главное меню приложения, предоставляя пользователю выбор действий.
    """
    print("\n" + "="*40)
    print("🔢 Консольное приложение для проверки массивов")
    print("="*40)
    print("1. Ввод исходных данных (вручную/генерация)")
    print("2. Выполнение алгоритма по заданию")
    print("3. Вывод результата")
    print("4. Завершение работы программы")
    print("-" * 40)

def handle_data_input():
    """
    Обрабатывает выбор пользователя для ввода данных (ручной или генерация).
    При успешном вводе новых данных: сбрасывает текущие результаты.
    """
    global current_data, current_results
    
    print("\n--- Выбор метода ввода данных ---")
    print("1. Ручной ввод")
    print("2. Случайная генерация (размер 5)")
    
    choice = input("Выберите (1 или 2): ")
    logger.info(f"Действие пользователя: Выбран пункт меню 1 (Ввод данных). Подпункт: {choice}")
    
    new_data = None
    if choice == '1':
        new_data = manual_input()
    elif choice == '2':
        new_data = generate_random_arrays(size=5)
    else:
        logger.warning("Действие пользователя: Некорректный подпункт ввода данных.")
        print("Некорректный выбор.")
        return

    if new_data and all(new_data):
        current_data = new_data
        current_results = None  # Сброс результатов
        logger.info("Действие сервера: Результаты сброшены после ввода новых данных.")
        
        arr1, arr2, arr3 = current_data
        print("\n✅ Данные успешно введены.")
        print(f"Массив 1: {arr1}")
        print(f"Массив 2: {arr2}")
        print(f"Массив 3: {arr3}")
    else:
        print("\n❌ Ввод данных не удался. Пожалуйста, попробуйте снова.")


def handle_algorithm_execution():
    """
    Выполняет основной алгоритм проверки арифметической возможности.
    Проверяет зависимость: "Алгоритм не может быть выполнен без введенных данных".
    """
    global current_data, current_results
    
    logger.info("Действие пользователя: Выбран пункт меню 2 (Выполнение алгоритма).")

    if current_data is None:
        logger.warning("Действие сервера: Попытка выполнить алгоритм без данных.")
        print("\n❌ Алгоритм не может быть выполнен без введенных данных. Сначала введите данные (Пункт 1).")
        return
    
    arr1, arr2, arr3 = current_data
    print("\n--- Запуск алгоритма ---")
    current_results = process_arrays(arr1, arr2, arr3)
    
    if isinstance(current_results, str):
        logger.error(f"Действие сервера: Ошибка при обработке данных в алгоритме: {current_results}")
        current_results = None
    else:
        logger.info("Действие сервера: Алгоритм успешно завершен, результаты сохранены.")
        print("✅ Алгоритм успешно выполнен. Результаты готовы к выводу (Пункт 3).")


def handle_output():
    """
    Выводит результаты выполнения алгоритма на консоль.
    Проверяет зависимость: "Вывод результата не может быть осуществлен без выполнения алгоритма".
    """
    global current_results
    
    logger.info("Действие пользователя: Выбран пункт меню 3 (Вывод результата).")
    
    if current_results is None:
        logger.warning("Действие сервера: Попытка вывести результат до выполнения алгоритма.")
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
    logger.info("Действие сервера: Вывод результатов на консоль завершен.")


def main(logging_level=logging.INFO):
    """
    Основная функция программы, реализующая главный цикл меню.
    
    Args:
        logging_level (int): Уровень логирования, передаваемый для демонстрации переключения.
    """
    # Перенастройка логгера для демонстрации выбранного уровня
    setup_logging(logging_level) 
    
    if logging_level == logging.CRITICAL:
        print("\n--- ВНИМАНИЕ: Логирование установлено на уровень CRITICAL. В файл будут записаны только критические ошибки. ---")
    
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
            logger.info("Действие пользователя: Выбран пункт меню 4 (Завершение работы).")
            print("\n👋 Завершение работы программы. До свидания!")
            break
        else:
            logger.warning(f"Действие пользователя: Некорректный выбор меню: {choice}")
            print("Некорректный ввод. Пожалуйста, выберите пункт от 1 до 4.")


if __name__ == '__main__':
    main(logging.INFO)
import sys
import logging
from client_logic import console_lock, get_now
from data_management import manual_input, generate_random_arrays
from core_algorithm import process_arrays

# Состояния автомата
STATE_MAIN = "MAIN"
STATE_INPUT = "INPUT"
STATE_RUN = "RUN"
STATE_SHOW = "SHOW"
STATE_EXIT = "EXIT"

class MenuAutomaton:
    def __init__(self, request_queue):
        self.current_state = STATE_MAIN
        self.request_queue = request_queue
        self.data = None
        self.results = None
        self.is_running = True

        # Таблица переходов и действий (Логика автомата)
        self.states = {
            STATE_MAIN: self.show_main_menu,
            STATE_INPUT: self.handle_input,
            STATE_RUN: self.handle_run,
            STATE_SHOW: self.handle_show,
            STATE_EXIT: self.handle_exit
        }

    def show_main_menu(self):
        with console_lock:
            print(f"\n[{get_now()}] === ГЛАВНОЕ МЕНЮ ===")
            print("1. Ввод данных (Вспомогательное меню)")
            print("2. Выполнить расчет (Сервер)")
            print("3. Показать результат")
            print("4. Выход")
        
        choice = input("Выберите действие: ")
        
        transitions = {
            "1": STATE_INPUT,
            "2": STATE_RUN,
            "3": STATE_SHOW,
            "4": STATE_EXIT
        }
        self.current_state = transitions.get(choice, STATE_MAIN)

    def handle_input(self):
        with console_lock:
            print(f"\n[{get_now()}] --- МЕНЮ ВВОДА ---")
            print("1. Ручной ввод")
            print("2. Генерация")
            print("3. Назад")
        
        choice = input("Выберите метод: ")
        if choice == "1":
            self.data = manual_input()
            self.current_state = STATE_MAIN
        elif choice == "2":
            self.data = generate_random_arrays(size=3)
            self.current_state = STATE_MAIN
        elif choice == "3":
            self.current_state = STATE_MAIN
        else:
            print("Ошибка выбора.")

    def handle_run(self):
        if not self.data:
            print("❌ Сначала введите данные (Пункт 1).")
        else:
            print("⏳ Запрос отправлен на сервер...")
            # Здесь логика отправки в очередь, которую мы писали ранее
            # В рамках автомата просто имитируем переход после действия
            # (Для клиента здесь будет отправка в request_queue)
            self.results = "Данные в обработке..." 
        self.current_state = STATE_MAIN

    def handle_show(self):
        if not self.results:
            print("❌ Нет результатов для отображения.")
        else:
            print(f"✅ Результаты: {self.results}")
        self.current_state = STATE_MAIN

    def handle_exit(self):
        print("Завершение работы...")
        self.is_running = False

    def run(self):
        """Запуск цикла автомата"""
        while self.is_running:
            handler = self.states.get(self.current_state)
            if handler:
                handler()
            else:
                self.current_state = STATE_MAIN

# Пример запуска
if __name__ == "__main__":
    # Предположим, очередь создана в main
    import queue
    q = queue.Queue()
    automaton = MenuAutomaton(q)
    automaton.run()
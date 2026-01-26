import queue
import threading
from client_logic import console_lock, get_now
from data_management import manual_input, generate_random_arrays
from server_logic import server_worker

STATE_MAIN = "MAIN"
STATE_INPUT = "INPUT"

class MenuAutomaton:
    def __init__(self, request_queue):
        self.request_queue = request_queue
        self.data = None      # Исходные данные
        self.results = None   # Результаты (сбрасываются при новом вводе)
        self.state = STATE_MAIN
        self.stopped = False

    def run(self):
        """Главный цикл управления состояниями."""
        while not self.stopped:
            if self.state == STATE_MAIN:
                self._main_menu()
            elif self.state == STATE_INPUT:
                self._input_menu()

    def _main_menu(self):
        with console_lock:
            print(f"\n[{get_now()}] === ГЛАВНОЕ МЕНЮ ===")
            print("1. Ввод исходных данных")
            print("2. Выполнить алгоритм по заданию")
            print("3. Вывод результата")
            print("4. Завершение работы программы")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            self.state = STATE_INPUT
        elif choice == "2":
            self._execute_algorithm()
        elif choice == "3":
            self._show_results()
        elif choice == "4":
            self.stopped = True
        else:
            print("❌ Неверный выбор.")

    def _input_menu(self):
        with console_lock:
            print(f"\n[{get_now()}] --- ВВОД ДАННЫХ ---")
            print("1. Ввести вручную")
            print("2. Сгенерировать случайно")
            print("3. Назад")
        
        choice = input("Выберите пункт: ")
        new_data = None
        
        if choice == "1":
            new_data = manual_input()
        elif choice == "2":
            new_data = generate_random_arrays()
            print(f"✅ Данные сгенерированы: {new_data}")
        elif choice == "3":
            self.state = STATE_MAIN
            return

        if new_data and new_data[0] is not None:
            self.data = new_data
            self.results = None # СБРОС: Результаты сбрасываются при вводе новых данных
            print("✅ Данные приняты. Результаты прошлых расчетов сброшены.")
            self.state = STATE_MAIN

    def _execute_algorithm(self):
        # Алгоритм не может быть выполнен без введенных данных
        if not self.data:
            print("❌ ОШИБКА: Сначала введите данные (Пункт 1).")
            return
        
        event = threading.Event()
        request = {
            'client_id': 'LocalUser',
            'data': self.data,
            'event': event,
            'result': None
        }
        
        print("⏳ Запрос отправлен на сервер...")
        self.request_queue.put(request)
        event.wait() # Ждем завершения расчета на сервере
        self.results = request['result']
        print("✅ Алгоритм успешно выполнен.")

    def _show_results(self):
        # Вывод результата не может быть осуществлен без выполнения алгоритма
        if not self.results:
            print("❌ ОШИБКА: Сначала выполните алгоритм (Пункт 2).")
            return
        
        print("\n=== РЕЗУЛЬТАТЫ РАСЧЕТА ===")
        for res in self.results:
            status = f"МОЖНО ({res['explanation']})" if res['found'] else "НЕЛЬЗЯ"
            print(f"Для {res['target']} (из {res['a']} и {res['b']}): {status}")

if __name__ == "__main__":
    q = queue.Queue()
    # Запуск сервера в фоновом потоке
    threading.Thread(target=server_worker, args=(q,), daemon=True).start()
    
    automaton = MenuAutomaton(q)
    automaton.run()
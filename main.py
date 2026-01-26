import queue
import threading
import time
from client_logic import console_lock, get_now
from data_management import manual_input, generate_random_arrays
from server_logic import server_worker

class MenuAutomaton:
    def __init__(self, request_queue):
        self.request_queue = request_queue
        self.data = None
        self.results = None
        self.state = "MAIN"
        self.stopped = False

    def run(self):
        while not self.stopped:
            if self.state == "MAIN":
                self._main_menu()
            elif self.state == "INPUT":
                self._input_menu()
            # Эффективность: небольшая пауза предотвращает 100% нагрузку на ядро CPU в пустом цикле
            time.sleep(0.01) 

    def _main_menu(self):
        print(f"\n[{get_now()}] === МЕНЮ (ЭФФЕКТИВНОЕ) ===")
        print("1. Ввод / 2. Алгоритм / 3. Результат / 4. Выход")
        choice = input(">> ")
        
        if choice == "1": self.state = "INPUT"
        elif choice == "2": self._execute_algorithm()
        elif choice == "3": self._show_results()
        elif choice == "4": self.stopped = True

    def _execute_algorithm(self):
        if not self.data:
            print("❌ Нет данных.")
            return
        
        event = threading.Event()
        request = {'client_id': 'AsusUser', 'data': self.data, 'event': event, 'result': None}
        
        # Эффективность: Очередь (Queue) в Python потокобезопасна и не требует дополнительных Lock
        self.request_queue.put(request)
        
        # Эффективность: event.wait() усыпляет поток, освобождая ресурсы Windows 10 для других задач
        event.wait() 
        self.results = request['result']
        print("✅ Готово.")

    def _show_results(self):
        if not self.results:
            print("❌ Выполните алгоритм.")
            return
        # Оптимизированный вывод через join (быстрее для больших строк)
        output = "\n".join([f"{r['target']} <- {r['explanation'] if r['found'] else 'НЕТ'}" for r in self.results])
        print(output)

    def _input_menu(self):
        print("\n1. Ручной / 2. Генерация / 3. Назад")
        c = input(">> ")
        if c == "1": self.data = manual_input(); self.results = None
        elif c == "2": self.data = generate_random_arrays(size=1000); self.results = None
        self.state = "MAIN"

if __name__ == "__main__":
    q = queue.Queue()
    threading.Thread(target=server_worker, args=(q,), daemon=True).start()
    MenuAutomaton(q).run()
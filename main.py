import sys
import logging
import queue
from client_logic import console_lock, get_now
from data_management import manual_input, generate_random_arrays
from core_algorithm import process_arrays

# Состояния автомата. Состояния автомата — это фиксированные фазы, в которых может находиться программа
STATE_MAIN = "MAIN"   # Главное меню
STATE_INPUT = "INPUT" # Вспомогательное меню ввода данных
STATE_RUN = "RUN"     # Логика запуска обработки
STATE_SHOW = "SHOW"    # Отображение результатов
STATE_EXIT = "EXIT"    # Состояние выхода

class MenuAutomaton:
    """
    Класс, реализующий конечный автомат (FSM) через корутины Python.
    Каждое состояние представлено независимой функцией-генератором.
    """
    def __init__(self, request_queue):
        self.request_queue = request_queue # Очередь для взаимодействия с сервером
        self.data = None # Хранилище введенных пользователем данных
        self.results = None # Хранилище результатов расчета
        self.stopped = False # Флаг для обозначения завершения работы. Флаг остановки цикла автомата

        # Инициализация состояний как корутин. Каждое значение — это объект корутины
        self.states = {
            STATE_MAIN: self._create_main_menu(),
            STATE_INPUT: self._create_input_menu(),
            STATE_RUN: self._create_run_logic(),
            STATE_SHOW: self._create_show_results()
        }
        
      # [cite_start]current_state_name определяет, какая корутина будет обрабатывать следующий ввод
        self.current_state_name = STATE_MAIN
        self.current_state_coro = self.states[STATE_MAIN]
        # ПРАЙМИНГ (Priming): Вызов next() подготавливает корутины, доводя их до первого yield.
        # Без этого шага корутина не сможет принять данные через метод send().
        for coro in self.states.values():
            next(coro)

    def _create_main_menu(self):
        """Корутина состояния 'Главное меню'. Работает в бесконечном цикле."""
        while True:
            with console_lock:
                print(f"\n[{get_now()}] === ГЛАВНОЕ МЕНЮ ===")
                print("1. Ввод данных (Вспомогательное меню)")
                print("2. Выполнить расчет (Сервер)")
                print("3. Показать результат")
                print("4. Выход")
            
            # Оператор yield приостанавливает корутину и ждет получения данных извне
            choice = yield
            
            # Логика переходов: на основе ввода меняется имя текущего состояния
            if choice == "1":
                self.current_state_name = STATE_INPUT
            elif choice == "2":
                self.current_state_name = STATE_RUN
            elif choice == "3":
                self.current_state_name = STATE_SHOW
            elif choice == "4":
                self.stopped = True # Сигнал к завершению работы автомата
            else:
                with console_lock:
                    print("Ошибка: неверный выбор.")
                self.current_state_name = STATE_MAIN # Остаемся в главном меню

    def _create_input_menu(self):
        """Корутина состояния 'Меню ввода'. Пример вспомогательного меню. """
        while True:
            with console_lock:
                print(f"\n[{get_now()}] --- МЕНЮ ВВОДА ---")
                print("1. Ручной ввод")
                print("2. Генерация")
                print("3. Назад")
            
            # Корутина "засыпает" здесь до вызова метода .send(user_input)
            choice = yield 
            if choice == "1":
                self.data = manual_input() # Синхронный вызов функции ввода
                self.current_state_name = STATE_MAIN # Возврат в родительское состояние
            elif choice == "2":
                self.data = generate_random_arrays(size=3)
                self.current_state_name = STATE_MAIN
            elif choice == "3":
                self.current_state_name = STATE_MAIN
            else:
                with console_lock:
                    print("Ошибка выбора.")
                    # При неверном вводе остаемся в этом же состоянии
                self.current_state_name = STATE_INPUT

    def _create_run_logic(self):
        """Корутина состояния 'Запуск расчета'. Обрабатывает действие без сложного ветвления."""
        while True:
            yield # Ожидание сигнала к действию
            if not self.data:
                with console_lock:
                    print("❌ Сначала введите данные (Пункт 1).")
            else:
                with console_lock:
                    print("⏳ Запрос отправлен на сервер...")
                    # Эмуляция постановки задачи в очередь
                self.results = "Данные в обработке..." 
            self.current_state_name = STATE_MAIN

    def _create_show_results(self):
        """Корутина состояния 'Просмотр результатов'."""
        while True:
            yield # Пауза до получения сигнала (ввода пользователя)
            if not self.results:
                with console_lock:
                    print("❌ Нет результатов для отображения.")
            else:
                with console_lock:
                    print(f"✅ Результаты: {self.results}")
            self.current_state_name = STATE_MAIN

    def send(self, user_input):
        """Интерфейс для передачи внешних сигналов (ввода) в активное состояние автомата.
        Использует метод генератора .send(). """
        try:
            # Находим нужную корутину по имени и отправляем ей ввод пользователя
            self.states[self.current_state_name].send(user_input)
        except StopIteration:
            self.stopped = True # Если корутина завершилась (что не предусмотрено циклом while True), останавливаем автомат

    def run(self):
        """Главный управляющий цикл (эстафета управления).
        Опрашивает пользователя и передает управление в машину состояний."""
        while not self.stopped:
            # В этой реализации ввод запрашивается здесь и отправляется в активную корутину
            # Состояние STATE_RUN и STATE_SHOW не требуют сложного ввода, поэтому 'Enter' достаточно
            user_input = input("Выберите действие/Нажмите Enter: ")
            self.send(user_input)

# Точка входа в программу
if __name__ == "__main__":
    # Создание системной очереди (для будущей интеграции с сервером)
    q = queue.Queue()
    # Инстанцирование объекта автомата
    automaton = MenuAutomaton(q)
    # Запуск бесконечного цикла обработки
    automaton.run()
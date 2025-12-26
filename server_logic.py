import time
import random
import logging
import queue
from core_algorithm import process_arrays
from client_logic import console_lock, get_now # Используем общий лок и формат времени

# Настройка логирования сервера в файл
server_logger = logging.getLogger("ServerLogger")
server_logger.setLevel(logging.INFO)

# Режим 'w' перезаписывает лог при каждом запуске сервера
file_handler = logging.FileHandler('server_activity.log', mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - SERVER - %(message)s', datefmt='%H:%M:%S')
file_handler.setFormatter(formatter)
server_logger.addHandler(file_handler)

def server_worker(request_queue):
    """
    Основная функция сервера. Работает в ОДНОМ потоке.
    """
    server_logger.info("Статус: Сервер запущен и ожидает запросы в очереди.")
    
    while True:
        # Получаем задачу из очереди (блокирует поток сервера, если очередь пуста)
        request = request_queue.get()
        
        if request is None: # Специальный сигнал для остановки сервера
            break
        
        client_id = request['client_id']
        data = request['data']
        
        server_logger.info(f"Начата обработка задачи от {client_id}")

        # === Эмуляция длительных расчетов ===
        # Если хотите убрать паузу, закомментируйте две строки ниже
        pause = random.uniform(1, 3) # Случайная задержка от 1 до 3 секунд
        time.sleep(pause)
        
        # Выполнение реального алгоритма из core_algorithm.py
        try:
            results = process_arrays(data[0], data[1], data[2])
            request['result'] = results
            status_msg = f"успешно обработал запрос от {client_id} (пауза {pause:.2f}с)"
        except Exception as e:
            status_msg = f"ОШИБКА при расчете для {client_id}: {e}"
            server_logger.error(status_msg)

        # Логирование в файл
        server_logger.info(f"Завершено: {status_msg}")
        
        # Безопасный вывод в консоль (с использованием Lock)
        with console_lock:
            print(f"{get_now()} [СЕРВЕР] {client_id}: расчеты ВЫПОЛНЕНЫ.")
        
        # Уведомляем поток клиента, что данные готовы
        request['event'].set()
        
        # Помечаем задачу в очереди как выполненную
        request_queue.task_done()
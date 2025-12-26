import threading
import time
from datetime import datetime
# Импортируем функцию генерации из вашего существующего модуля
from data_management import generate_random_arrays

# Глобальный объект блокировки. Гарантирует, что строки в консоли 
# от разных клиентов и сервера не будут перемешиваться.
console_lock = threading.Lock()

def get_now():
    """Возвращает текущее системное время для логов в консоли."""
    return datetime.now().strftime("%H:%M:%S")

class Client(threading.Thread):
    """
    Класс Клиента, наследуемый от Thread.
    Каждый экземпляр этого класса — это отдельный пользователь со своим меню.
    """
    def __init__(self, client_id, request_queue):
        # ИСПРАВЛЕНИЕ: super().__init__() вызывается БЕЗ аргументов.
        # Это предотвращает ошибку "group argument must be None".
        super().__init__()
        
        # Сохраняем переданные данные в атрибуты экземпляра
        self.client_id = client_id
        self.request_queue = request_queue
        
        # Указываем, что поток является фоновым (завершится вместе с программой)
        self.daemon = True

    def run(self):
        """
        Основной цикл работы потока клиента.
        """
        # Блокируем консоль для вывода приветствия
        with console_lock:
            print(f"{get_now()} [КЛИЕНТ] {self.client_id}: поток запущен, доступ к меню открыт.")
        
        # --- ШАГ 1: Генерация данных ---
        # Эмулируем выбор пользователя в меню (например, пункт "Сгенерировать данные")
        data = generate_random_arrays(size=3)
        
        with console_lock:
            print(f"{get_now()} [КЛИЕНТ] {self.client_id}: сгенерированы данные.")
        
        # --- ШАГ 2: Создание и отправка запроса ---
        # Event() — это "сигнальный флажок". Клиент будет ждать, пока сервер его поднимет.
        completion_event = threading.Event()
        
        request = {
            'client_id': self.client_id,
            'data': data,
            'event': completion_event,
            'result': None
        }
        
        with console_lock:
            print(f"{get_now()} [КЛИЕНТ] {self.client_id}: ОТПРАВИЛ запрос на сервер.")
        
        # Кладем словарь запроса в общую очередь сервера
        self.request_queue.put(request)
        
        # --- ШАГ 3: Ожидание ответа ---
        # Поток клиента здесь "замирает" и не тратит ресурсы процессора, пока сервер занят.
        completion_event.wait()
        
        # --- ШАГ 4: Результат получен ---
        with console_lock:
            print(f"{get_now()} [КЛИЕНТ] {self.client_id}: ПОЛУЧИЛ ответ от сервера. Операция завершена успешно.")
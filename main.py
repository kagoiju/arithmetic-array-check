import threading
import queue
import time
from server_logic import server_worker
from client_logic import Client

def main():
    # Создаем общую очередь запросов
    request_queue = queue.Queue()

    # 1. Запускаем СЕРВЕР в единственном потоке
    server_thread = threading.Thread(
        target=server_worker, 
        args=(request_queue,), 
        daemon=True
    )
    server_thread.start()

    # 2. Запускаем группу КЛИЕНТОВ (каждый в своем потоке)
    num_clients = 5
    clients = []
    
    for i in range(1, num_clients + 1):
        client_name = f"Клиент_{i}"
        c = Client(client_name, request_queue)
        clients.append(c)
        c.start()
        # Если хотите "взрывную" нагрузку, уберите time.sleep ниже
        time.sleep(0.2) 

    # Даем клиентам и серверу время поработать
    time.sleep(15)
    print("\n[СИСТЕМА] Основной цикл завершен. Все запросы обработаны.")

if __name__ == "__main__":
    main()
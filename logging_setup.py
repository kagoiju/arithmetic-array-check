# logging_setup.py

import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Настраивает логирование для всего приложения.
    Логи записываются в файл 'app_activity.log'.
    
    Args:
        level (int): Уровень логирования (например, logging.INFO, logging.CRITICAL).
    """
    
    logger = logging.getLogger()
    
    # === ИСПРАВЛЕНИЕ: Удаление существующих обработчиков ===
    # Это предотвращает дублирование логов и конфликты уровней при повторном вызове setup_logging.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # ========================================================
        
    logger.setLevel(level)
    
    # 2. Формат записи логов
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 3. Обработчик для записи в файл (FileHandler)
    file_handler = logging.FileHandler('app_activity.log', mode='w', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # (Опционально) Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING) # В консоль выводим только WARNING и выше
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("--- Система логирования инициализирована. ---")
    
# Инициализация логирования с уровнем INFO по умолчанию при импорте
setup_logging(logging.INFO)
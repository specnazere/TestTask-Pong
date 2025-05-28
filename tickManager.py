import time
import threading

class TickManager:
    _initialized = False
    _lock = threading.Lock()

    # Внутренние данные
    _real_time = 0.0           # Накопленное реальное время
    _time_scale = 1.0          # Множитель времени (например: 2.0 — ускорение в 2 раза)
    _last_tick_real_time = 0.0 # Время начала последнего тика
    _previous_tick_length = 0.0

    @staticmethod
    def initialize():
        """Инициализирует менеджер тиков."""
        with TickManager._lock:
            TickManager._initialized = True
            TickManager._real_time = 0.0
            TickManager._time_scale = 1.0
            TickManager._last_tick_real_time = time.time()
            TickManager._previous_tick_length = 0.0
        print("TickManager инициализирован.")

    @staticmethod
    def set_time_scale(scale):
        """Устанавливает множитель времени."""
        if not isinstance(scale, (int, float)) or scale <= 0:
            raise ValueError("Множитель времени должен быть положительным числом.")
        with TickManager._lock:
            TickManager._time_scale = scale

    @staticmethod
    def get_time_scale():
        """Возвращает текущий множитель времени."""
        return TickManager._time_scale

    @staticmethod
    def tick():
        """Вызывается при каждом тике. Обновляет прошедшее время и сохраняет предыдущий тик."""
        with TickManager._lock:
            current_time = time.time()
            elapsed_real_time = current_time - TickManager._last_tick_real_time
            TickManager._real_time += elapsed_real_time * TickManager._time_scale
            TickManager._previous_tick_length = elapsed_real_time * TickManager._time_scale
            TickManager._last_tick_real_time = current_time

    @staticmethod
    def reset_current_tick():
        """Обнуляет текущий тик, сохраняя предыдущий."""
        with TickManager._lock:
            TickManager._last_tick_real_time = time.time()

    @staticmethod
    def get_previous_tick_length():
        """Возвращает длину предыдущего тика."""
        return TickManager._previous_tick_length

    @staticmethod
    def get_real_time():
        """Возвращает накопленное реальное время."""
        return TickManager._real_time
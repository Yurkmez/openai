# Ф-ция для организации форматирования вывода в терминале
def object_to_dict(obj):
    if isinstance(obj, list):
        # Рекурсивная обработка списка
        return [object_to_dict(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        # Конвертация объека с аттрибутом __dict__
        return {key: object_to_dict(value) for key, value in obj.__dict__.items()}
    else:
        # Возвращает объект как есть
        return obj

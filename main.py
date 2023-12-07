import pytz
from datetime import datetime


def convert_time(moscow_time_str: str) -> str:
    """Функция для конвертирования Московского времни в Новосибирское"""
    moscow_timezone = pytz.timezone("Europe/Moscow")
    novosibirsk_timezone = pytz.timezone("Asia/Novosibirsk")

    # Парсим время из файла и локалезуем как Московское
    moscow_time = datetime.strptime(moscow_time_str.strip(), "%m/%d/%Y %I:%M:%S %p")
    moscow_time = moscow_timezone.localize(moscow_time)

    # Конвертируем в Новосибирское
    novosibirsk_time = moscow_time.astimezone(novosibirsk_timezone)
    return novosibirsk_time.strftime("%m-%d-%Y %H:%M:%S")


def generate_curl() -> list[str]:
    """Основная функиця для генерации ссылок для обращения к видеорегистратору"""
    curls = []
    with open("report for domination (TXT).txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

        for line in lines[9:]:  # Пропускаем шапку в файле
            if line.strip():
                data = line.split("\t")
                order_number = data[0]  # Номер заказа
                computer_name = data[2]  # Имя компа
                camera_number = computer_name.split("-")[1]  # Номер канала в регистраторе
                event_time = data[4]  # Время упаковки

                # Конвертируем время упаковки из Мск в Нск
                event_time_novosibirsk = convert_time(event_time)

                # Генерируем curl для обращения к видеорегистратору
                curl = (f'curl -v "http://192.168.0.100:7004/getarch?camera={camera_number}'
                        f'&date={event_time_novosibirsk[:10]}&from={event_time_novosibirsk[11:]}'
                        f'&duration=120" --digest -u guest:guest --output "{order_number}.mp4"')
                curls.append(curl)

    return curls


def write_in_list(list_of_curls):
    """Функция для записи curl в txt файл"""
    with open("list_of_curls.txt", "w", encoding="utf-8") as write_file:
        write_file.writelines(f"{curl}\n" for curl in list_of_curls)
    print("Файл создан")


write_in_list(generate_curl())

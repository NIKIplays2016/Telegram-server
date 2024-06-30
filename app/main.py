
import telebot
import json
from os import system, popen
import os
from config import token

with open(r"data\base.json", "r") as file:
    base = json.load(file)
    base['pwd'] = base["pwd"].replace("/", "\\")
print(base)
bot = telebot.TeleBot(token)


def registrate(message_json, message):
    global base
    id = message_json['json']['from']['id']
    path = base["pwd"]
    system(f"cd {path} & mkdir {id}")
    base["users"]["name"].append(message_json['json']['from']["username"])
    base["users"]["id"].append(id)
    base["users"]["root"].append(False)
    base["users"]["space"].append(1024000000)
    base["users"]["max_space"].append(1024000000)
    base["users"]["now_directory"].append("id")

    base["users"]["path"].append(f"{id}")
    with open("data/base.json", "w") as file:
        json.dump(base, file)
    with open("data/base.json", "r") as file:
        base = json.load(file)
    bot.reply_to(message, f"Вы успешно зарегестрировались, ваша директория: {id}")

def save():
    global base
    base['pwd'] = base['pwd'].replace("\\", "/")
    with open(r"data\base.json", "w") as file:
        json.dump(base, file)



def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size






bool_action = [False, False, False, False, False, False, False]

def take_id(message):
    global base
    index = base["users"]["id"].index(message.chat.id)
    return index

@bot.message_handler(commands=['command1'])
def handle_start(message):
    # Запуск файла
    bool_action[0] = True
    index = take_id(message)
    bot.reply_to(message, f"Введите имя файла\n\nТекущая директория: {base['users']['path'][index]}")

@bot.message_handler(commands=['command2'])
def handle_start(message):
    # Создание папки
    bool_action[1] = True
    index = take_id(message)
    bot.reply_to(message, f"Введите название папки\n\nТекущая директория: {base['users']['path'][index]}")

@bot.message_handler(commands=['command3'])
def handle_start(message):
    # Удаление папки
    bool_action[2] = True
    index = take_id(message)
    bot.reply_to(message, f"Введите название папки\n\nТекущая директория: {base['users']['path'][index]}")

@bot.message_handler(commands=['command4'])
def handle_start(message):
    # Загрузка файлов
    bool_action[3] = True
    index = take_id(message)
    bot.reply_to(message, f"Скиньте файлы в следующем смс. \n\nПримечания\n-не более 4гб \n\nЧтобы выключить режим загрузки введите \stop \n\nПримечание: фото лучше скидывать документом\n\nТекущая директория: {base['users']['path'][index]} \n\n Оставшееся пространство: {int(base['users']['space'][index]/1000000)} мб ")

@bot.message_handler(commands=['command5'])
def handle_start(message):
    # написать команду
    index = take_id(message)
    root = base["users"]["root"][index]

    if root:
        bool_action[4] = True
        bot.reply_to(message, "Напишите команду(-ы) в одну строку")
    else:
        bot.reply_to(message, "У вас недостаточно прав")


@bot.message_handler(commands=['command6'])
def handle_start(message):
    # Выбор директории
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)

    index = take_id(message)

    path = base["pwd"] + base['users']['path'][index]
    files = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]


    directory = base['users']['path'][index]
    root = base['users']['root'][base['users']['id'].index(message.chat.id)]
    if (not directory == base['users']['id'][index]) or root:
        keyboard1.row("..")

    for i in files:
        keyboard1.row(i)
    bot.send_message(message.chat.id, 'Выберите директорию', reply_markup=keyboard1)
    bool_action[5] = True

@bot.message_handler(commands=['command7'])
def handle_start(message):
    # Вывод файлов в дир
    index = take_id(message)

    path = base["pwd"] + base['users']['path'][index]
    files = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    sms = f"В директории {base['users']['path'][index]}:\n"

    if len(files) < 15:
        for i in files:
            sms += "\n" + i
    else:
        for i in range(15):
            sms += "\n" + files[i]
        sms += "\n....."

    sms += f"\n\nОставшееся пространство: {int(base['users']['space'][index] / 1000000)} мб"

    bot.reply_to(message, sms)


@bot.message_handler(commands=['command8'])
def handle_start(message):
    global bool_action
    for i in range(len(bool_action)):
        bool_action[i] = False


@bot.message_handler(commands=['command9', 'info'])
def handle_start(message):
    sms = (
        "Бот для управления мини сервером.\n\n" +
        "Команды: \n" +
        "1. Запуск файла - команда запускает файл с расширением .py . ||Пример: для файла main.py, после ввода команды нужно написать main.py||\n" +
        "2. Создание папки/директории - Команда создает папку в директории, с названием указаным после ввода команты ||примечания: пробелы заменяются на _ ||.\n" +
        "3. Удаление папки - Удаляет папку/файл в директории в которой вы находитесь.\n" +
        "4. Загрузка файлов - загружает файлы в текущую директорию. Нет ограничений на количество файлов отправленных за раз. Для остановки режима загрузки файлов надо ввести комманду /stop или в командном меню внажать на команду Stop.\n" +
        "5. Написать команду - Прямая работа с cmd, но для работы с ней нужны права администратора.\n" +
        "6. Выбор директории - Команды выводит список директорий в которые можно перейти из текущей. Чтобы подняться на уровень выше нужно выбрать '..' .\n" +
        "7. Просмотр директории - Команда выводит все файлы и директории в текущей.\n" +
        "8. Stop - команда обнуляет все активные команды.\n\n\n"+
        "Конфигурация сервера:\n" +
        "   Процессор: Ryzen FX 5800\n" +
        "   Оперативная память: 16Gb 1600MGh\n" +
        "   Видеокарта: GTX 550Ti\n" +
        "   Скорость интернет соединения: 1-6 мб/cек \n" +
        "\n"
    )
    bot.reply_to(message, sms)


########################################################################################################################
@bot.message_handler(content_types=['text', 'document', 'audio', 'photo', 'video'])
def get_text_messages(message):
    global bool_action
    message_json = message.__dict__
    print(message_json['message_id'])
    try:
        index = base["users"]["id"].index(message_json['json']['from']['id'])
        root = base["users"]["root"][index]
    except:
        registrate(message_json, message)
        return 0

    full_path = base["pwd"]+str(base['users']['path'][index])

    if bool_action[0]:
        bool_action[0] = False
        system(f"cd {full_path} & python {message_json['json']['text']}")

    elif bool_action[1]:
        bool_action[1] = False
        system(f"cd {full_path} & mkdir {message_json['json']['text'].replace(' ', '_')}")

    elif bool_action[2]:
        bool_action[2] = False
        try:
            system(f"cd {full_path} & rm -r {message_json['json']['text']}")
        except:
            bot.reply_to(message, "Произошла ошибка в удалении")

    elif bool_action[3]:

        folder_path = base["pwd"]+rf"{base['users']['id'][index]}"
        folder_size = get_folder_size(folder_path)
        if folder_size > base['users']['max_space'][index]:
            bot.reply_to(message,f"У вас недостаточно места.")
            return 0


        try:
            file_id = message.document.file_id if message.document else message.audio.file_id if message.audio else \
            message.photo[
                0].file_id if message.photo else message.video.file_id if message.video else message.voice.file_id if message.voice else message.sticker.file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = bot.download_file(file_path)


            try:
                file_name = message.document.file_name
            except:
                file_name = file_id + "." + file_info.file_path.split('.')[-1]

            file_name = rf"{full_path}/{file_name}."
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)

            base['users']['space'][index] = base['users']['max_space'][index] - folder_size
            save()

        except Exception as e:
            bot.reply_to(message, f'Произошла ошибка при сохранении файла: {str(e)}')


    elif bool_action[4]:
        bool_action[4] = False
        system(message_json['json']['text'])

    elif bool_action[5]:
        bool_action[5] = False
        path = message_json['json']['text']
        if path == ".." and (not base['users']['id'][index] == base['users']['path'][index] or base['users']['root'][index]):
            x=len(base['users']['path'][index])
            for i in range(len(base['users']['path'][index])):
                if base['users']['path'][index][i] == "/":
                    x = i

            base['users']['path'][index] = (base['users']['path'][index])[slice(0, x)]
        else:
            base['users']['path'][index] += rf"/{path}"

        save()
bot.polling(none_stop=True, interval=0)

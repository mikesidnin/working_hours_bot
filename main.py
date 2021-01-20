import telebot
import config
import re
from datetime import datetime
from telebot.types import Message
from collections import Counter

bot = telebot.TeleBot(config.token)
write_log_file = open('daily.log', 'w')


@bot.message_handler(content_types=['text'])
def daily(message: Message):
    # определяем дату и автора сообщения
    input_message = str(message.text)
    message_date = str(message.date)
    message_time = message_date

    user = str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)

    # проверяем заканчиваем работу или начинаем
    check_plus = input_message.find(config.plus)
    if check_plus != -1:
        work = True
    else:
        work = False

    check_minus = input_message.find(config.minus)
    if check_minus != -1:
        end_work = True
    else:
        end_work = False

    # если работаем, то определяем где
    if work:
        if len(input_message) > 4:
            message_time = input_message[3: len(input_message)]

        check_office = any(i in input_message for i in config.office)
        check_home = any(i in input_message for i in config.home)
        if check_office is True and check_home is False or input_message == config.plus:
            tag = config.office_tag
        else:
            tag = config.home_tag

        f = open('daily.log', 'a')
        f.write('name: ' + user + ', date: ' + message_date + ', time: ' + message_time + ', tag: ' + tag + ', s' + '\n')
        f.close()

    # если закончили работать, то фиксируем время
    if end_work:
        if len(input_message) > 4:
            message_time = input_message[3: len(input_message)]

        check_office = any(i in input_message for i in config.office)
        check_home = any(i in input_message for i in config.home)
        if check_office is True and check_home is False or input_message == config.minus:
            tag = config.office_tag
        else:
            tag = config.home_tag
        f = open('daily.log', 'a')
        f.write('name: ' + user + ', date: ' + message_date + ', time: ' + message_time + ', tag: ' + tag + ', e' + '\n')
        f.close()


    if input_message == '123':
        read_log_file = open('daily.log')
        log_file_lines = [line.strip() for line in read_log_file]

    # Определяем количество строк
        max_line = len(log_file_lines) - 1
        info_list = [[0 for x in range(6)] for y in range(max_line)]

    # Цикл обработки всех загруженных строк
        for i in range(0, max_line):
            log_line = str(log_file_lines[i])

            find_name = re.findall(r"name: ?([ \w.]+)", log_line)
            info_list[i][0] = find_name[0]

            find_date = re.findall(r"date: ?([ \w.]+)", log_line)
            info_list[i][1] = datetime.utcfromtimestamp(int(find_date[0])).strftime('%Y-%m-%d')

            find_time = re.findall(r"time: ?([ \w.]+)", log_line)
            if find_time[0] != find_date[0]:
                info_list[i][2] = find_time[0]
            else:
                info_list[i][2] = datetime.utcfromtimestamp(int(find_time[0])).strftime('%H:%M:%S')

            find_tag = re.findall(r"tag: ?([ \w.]+)", log_line)
            info_list[i][3] = find_tag[0]

            info_list[i][4] = log_line[-1]

            if info_list[i][4] == 'e':
                find_end_time = re.findall(r"time: ?([ \w.]+)", log_line)
                if find_end_time[0] != find_date[0]:
                    info_list[i][5] = find_end_time[0]
                else:
                    info_list[i][5] = datetime.utcfromtimestamp(int(find_end_time[0])).strftime('%H:%M:%S')
            else:
                info_list[i][5] = '-'
        print(info_list)

        result = [[0 for x in range(5)] for y in range(max_line)]
        for i in range(0, max_line-1):
            for j in range(i+1, max_line):
                if info_list[i][0] == info_list[j][0] and info_list[i][1] == info_list[j][1]:
                    result[i][0] = info_list[i][0]
                    result[i][1] = info_list[i][1]
                    result[i][2] = info_list[i][2]
                    result[i][3] = info_list[j][5]
                    result[i][4] = info_list[j][3]
                else:
                    result[i][0] = info_list[i][0]
                    result[i][1] = info_list[i][1]
                    result[i][2] = info_list[i][2]
                    result[i][3] = info_list[i][5]
                    result[i][4] = info_list[i][3]

        
        print(result)
        
bot.polling(none_stop=True)

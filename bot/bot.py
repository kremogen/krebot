# -*- coding: utf-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
import time
import datetime

conn = sqlite3.connect("players.db")
cursor = conn.cursor()

vk_session = vk_api.VkApi(token='your token')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        message = event.text
        player = event.user_id
        cursor.execute('SELECT * FROM players WHERE id = %s' % player)
        if cursor.fetchall() and event.text == 'Начать' or event.text == 'начать' or event.text == '🏠Главная' or event.text == 'Главная' or event.text == 'главная' and event.from_user:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message='Выбери, что-то из предложенного\n\n🎁Бонус\n📄Помощь',
                random_id=event.random_id
            )
        elif event.text == 'Начать' or event.text == 'начать' and event.from_user:
            hour = time.localtime()
            now = time.mktime(hour)
            now = int(now)
            date = datetime.datetime.now()
            date = date.strftime("%d-%m-%Y %H:%M")
            insert = [event.user_id, 0, 0, date, 0, now, 0, 0, 0, 0, 0]
            cursor.execute("INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?)", insert)
            conn.commit()
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message='Приветствуем тебя в нашем боте!😁\nЗдесь, ты можешь:\n  Поиграть в игры🕹(в будущем)\n\n  Узнать онлайн сервера🖥\n\n Скоротать время, получив классные бонусы😁',
                random_id=event.random_id
            )
        if event.text == '🎁Бонус' or event.text == 'Бонус' or event.text == 'бонус' and event.from_user:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            hour = time.localtime()
            now = time.mktime(hour)
            now = int(now)
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            [bonus], = cursor.execute("SELECT bonus FROM players WHERE id = %s" % player)
            bonus = now - bonus
            if bonus >= 86400:
                money = 1000
                balance = 1000 + balance
                insert = [balance, player]
                activity = [now, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                cursor.execute("UPDATE players SET bonus = ? WHERE id = ?", activity)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Ты получил 1000 бонусных долларов!💰',
                    random_id=event.random_id,
                )
            elif bonus < 86400:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Извини, но сутки ещё не прошли☹',
                    random_id=event.random_id,
                )
        if event.text == '📄Помощь' or event.text == 'Помощь' or event.text == 'помощь' and event.from_user:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('💼Профиль', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('💳Баланс', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('💸Донат', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('💎Магазин', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('💰Купить', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🧱Фермы', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🏠Главная', color=VkKeyboardColor.NEGATIVE)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message='🗃Информация\n&#12288;💼 Профиль\n&#12288;💳 Баланс\n&#12288;💸 Донат\n&#12288;💎 Магазин\n🧰Недвижимость\n&#12288;💰Купить\n&#12288;🧱Фермы',
                random_id=event.random_id,
            )
        if event.text == '💼Профиль' or event.text == 'Профиль' or event.text == 'профиль' and event.from_user:
            [date], = cursor.execute("SELECT date FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            player = str(player)
            date = str(date)
            mes = ['Ваш профиль💼\n\n🔑Идентификатор:', player, '\n🕓Дата регистрации:\n', date]
            mes = ' '.join(mes)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message=mes,
                random_id=event.random_id,
            )
        if event.text == '💳Баланс' or event.text == 'Баланс' or event.text == 'баланс' and event.from_user:
            [activity], = cursor.execute("SELECT activity FROM players WHERE id = %s" % player)
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            hour = time.localtime()
            now = time.mktime(hour)
            now = int(now)
            duration = now - activity
            factor = duration / 3600
            factor = int(factor)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if duration >= 3600:
                [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
                new_balance = profit * factor
                new_balance = new_balance + balance
                insert = [new_balance, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                activity = [now, player]
                cursor.execute("UPDATE players SET activity = ? WHERE id = ?", activity)
                conn.commit()
                new_balance = str(new_balance)
                mes = ['💳Ваш баланс:', new_balance, '💵']
                mes = ' '.join(mes)
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message=mes,
                    random_id=event.random_id,
                )
            elif duration < 3600:
                [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
                balance = str(balance)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
                keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
                mes = ['💳Ваш баланс:', balance, '💵']
                mes = ' '.join(mes)
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message=mes,
                    random_id=event.random_id,
                )
        if event.text == '💸Донат' or event.text == 'Донат' or event.text == 'донат' and event.from_user:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            player = str(player)
            mes = ['Ваш игрвоой 🔑идентификатор:\n', player, '\n\nПриобрести доллары💵 для бота, ты можешь тут\nbot.p-land.ru\n\n⚠При покупке вместо ника указывайте ваш игровой идентификатор⚠']
            mes = ' '.join(mes)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message=mes,
                random_id=event.random_id,
            )
        if event.text == '💎Магазин' or event.text == 'Магазин' or event.text == 'магазин' and event.from_user:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('10✅', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('15✅', color=VkKeyboardColor.POSITIVE)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message='Скидки доступные для покупки:\n\n&#12288;10% - 10000💵\n&#12288;15% - 15000💵\n\nНапиши ту скидку✅, которую хочешь приобрести.\nЕсли не хочешь ничего покупать напиши Помощь',
                random_id=event.random_id,
            )
        elif event.text == '10✅' or event.text == '10' or event.text == '10%' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 10000:
                balance = balance - 10000
                insert = [balance, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\n\nВаш купон - bot10\n\n⚠Осторожно, у купона тоько одно использование⚠',
                    random_id=event.random_id,
                )
            elif balance < 10000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        elif event.text == '15✅' or event.text == '15' or event.text == '15%' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 15000:
                balance = balance - 15000
                insert = [balance, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\n\nВаш купон - bot15\n\n⚠Осторожно, у купона тоько одно использование⚠',
                    random_id=event.random_id,
                )
            elif balance < 10000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        if event.text == '💰Купить' or event.text == 'Купить' or event.text == 'купить' and event.from_user:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('ФермаB889', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('ФермаG431', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('ФермаI279', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('ФермаL093', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('ФермаQ228', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('🏠Главная', color=VkKeyboardColor.NEGATIVE)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message='Фермы доступные для покупки(Выбери цифру):\nНазвание - стоимость - прибыль в час\n\n1. ФермаB889🔋 - 1000 - 50\n\n2. ФермаG431🔌 - 5000 - 300\n\n3. ФермаI279📡 - 25000 - 1600\n\n4. ФермаL093💿 - 100000 - 7000\n\n5. ФермаQ228📀 - 500000 - 40000\n\nЕсли не хочешь ничего покупать - гапиши Главная.',
                random_id=event.random_id,
            )
        elif event.text == 'ФермаB889' or event.text == '1' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 1000:
                balance = balance - 1000
                insert = [balance, player]
                profit = profit + 50
                profit = [profit, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                cursor.execute("UPDATE players SET profit = ? WHERE id = ?", profit)
                farm = [1, player]
                cursor.execute("UPDATE players SET farm_b = ? WHERE id = ?", farm)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\nТы стал обладателем ФермыB889🔋',
                    random_id=event.random_id,
                )
            elif balance < 1000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        elif event.text == 'ФермаG431' or event.text == '2' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 5000:
                balance = balance - 5000
                insert = [balance, player]
                profit = profit + 300
                profit = [profit, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                cursor.execute("UPDATE players SET profit = ? WHERE id = ?", profit)
                farm = [1, player]
                cursor.execute("UPDATE players SET farm_g = ? WHERE id = ?", farm)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\nТы стал обладателем ФермыG431🔌',
                    random_id=event.random_id,
                )
            elif balance < 5000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        elif event.text == 'ФермаI279' or event.text == '3' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 25000:
                balance = balance - 25000
                insert = [balance, player]
                profit = profit + 1600
                profit = [profit, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                cursor.execute("UPDATE players SET profit = ? WHERE id = ?", profit)
                farm = [1, player]
                cursor.execute("UPDATE players SET farm_i = ? WHERE id = ?", farm)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\nТы стал обладателем ФермыI279📡',
                    random_id=event.random_id,
                )
            elif balance < 25000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        elif event.text == 'ФермаL093' or event.text == '4' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 100000:
                balance = balance - 100000
                insert = [balance, player]
                profit = profit + 7000
                profit = [profit, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                cursor.execute("UPDATE players SET profit = ? WHERE id = ?", profit)
                farm = [1, player]
                cursor.execute("UPDATE players SET farm_l = ? WHERE id = ?", farm)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\nТы стал обладателем ФермыL093💿',
                    random_id=event.random_id,
                )
            elif balance < 100000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        elif event.text == 'ФермаQ228' or event.text == '5' and event.from_user:
            [balance], = cursor.execute("SELECT balance FROM players WHERE id = %s" % player)
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            if balance >= 500000:
                balance = balance - 500000
                insert = [balance, player]
                profit = profit + 40000
                profit = [profit, player]
                cursor.execute("UPDATE players SET balance = ? WHERE id = ?", insert)
                cursor.execute("UPDATE players SET profit = ? WHERE id = ?", profit)
                farm = [1, player]
                cursor.execute("UPDATE players SET farm_q = ? WHERE id = ?", farm)
                conn.commit()
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Поздравляем с покупкой😁!\nТы стал обладателем ФермыQ228📀',
                    random_id=event.random_id,
                )
            elif balance < 500000:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    user_id=event.user_id,
                    message='Упс, кажется у тебя недостатачно средств😔',
                    random_id=event.random_id,
                )
        if event.text == '🧱Фермы' or event.text == 'Фермы' or event.text == 'фермы' and event.from_user:
            [profit], = cursor.execute("SELECT profit FROM players WHERE id = %s" % player)
            [farm_q], = cursor.execute("SELECT farm_q FROM players WHERE id = %s" % player)
            [farm_l], = cursor.execute("SELECT farm_l FROM players WHERE id = %s" % player)
            [farm_i], = cursor.execute("SELECT farm_i FROM players WHERE id = %s" % player)
            [farm_g], = cursor.execute("SELECT farm_g FROM players WHERE id = %s" % player)
            [farm_b], = cursor.execute("SELECT farm_b FROM players WHERE id = %s" % player)
            profit = str(profit)
            farm_q = str(farm_q)
            farm_l = str(farm_l)
            farm_i = str(farm_i)
            farm_g = str(farm_g)
            farm_b = str(farm_b)
            mes = ['Твои фермы🧱\n\nФермB889:', farm_b, '🔋', '\nФермG431:', farm_g, '🔌', '\nФермI279:', farm_i, '📡', '\nФермL093:', farm_l, '💿', '\nФермQ228', farm_q, '📀', '\n\nВаша прибыль в час:', profit, '💵']
            mes = ' '.join(mes)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('🎁Бонус', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('📄Помощь', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                user_id=event.user_id,
                message=mes,
                random_id=event.random_id,
            )
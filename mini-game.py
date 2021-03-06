"""
импортируем библиотеки:
import discord (pip install discord.py)
import random (встроенная)
import asyncio (встроенная)
from discord.ext import commands (идёт вместе с discord.py)
from discord.ext.commands import Bot (идёт вместе с discord.py)
import json (встроенная)
"""

@commands.command() # создаём команду
async def флаги(self, ctx): # функцию
	event_members = {} # создаём словарь, он нужен для того, чтобы подсчитывать баллы каждого участника игры
	with open('flags.json','r',encoding='utf8') as f: # открываем файл с кодировкой utf8, чтобы всё было ок
		flags = json.load(f) # превращаем в словарь
		count = 1 # подсчёт раундов
		while count <= 10: # всего 10 раундов, Вы можете изменить это значение
			otvet = random.choice(flags['Флаги']) # выбираем рандомный флаг, который скинет бот и будет ожидать ответа к нему (всё из файла flags.json)
			e = discord.Embed(title = f"Флаг {count}") # создаём эмбед, с названием "Флаг №", на месте номера будет число раунда
			e.set_image(url = otvet['url']) # ставит изображение, взяв ссылку из файла flags.json
			await ctx.send(embed = e) # отправляет эмбед
			def check(m):
			"""создаёт проверку, то есть бот будет реагировать на сообщение
				с содержимым названия флага, в последнем обновлении я добавил чтобы 
				оно реагировало на содержимое, а также чтобы реагировало на ответ с
				маленькой буквы, с большой и даже если написано КАПСОМ"""
				return otvet['answer'] in m.content or otvet['answer'].capitalize() in m.content or otvet['answer'].lower() in m.content or otvet['answer'].upper() in m.content and ctx.channel == ctx.channel

			msg = await self.client.wait_for('message', check=check) # ожидает ответа
			if str(msg.author.id) not in event_members: # проверка на то, есть ли автор ответа в нашем созданном ранее словаре, если нет то заносит и даёт количество очков 1
				event_members[str(msg.author.id)] = {} # заносим в словарь
				event_members[str(msg.author.id)]["score"] = 1 # количество очков задаём
			elif str(msg.author.id) in event_members: # если автор ответа уже есть в ранее созданном словаре - срабатывает эта проверка
				event_members[str(msg.author.id)]["score"] += 1 # добавляет 1 очко
			em = discord.Embed(title = "Правильный ответ!") # создаём эмбед, который говорит о том что был правильный ответ
			em.add_field(name = "Ответил:", value = f"{msg.author.mention}") # кто ответил
			em.add_field(name = "Правильный ответ:",value = f"{otvet['answer']}") # какой правильный ответ
			await ctx.channel.send(embed = em) # отправляет
			count = count + 1 # следующий раунд
			await asyncio.sleep(1) # ждём, чтобы всё слишком быстро не было
			if count == 11: # если так называемый 11 раунд (конец по умолчанию) то эта проверка срабатывает
				e = discord.Embed(title = "Конец игры!", description = f"Таблица лидеров:") # создаёт эмбед с таблицой участников, и их баллами
				leaders = sorted(event_members, key=lambda score: event_members[score]['score'], reverse=True) # сортирует словарь по ключу score (очки)
				position = 1 # начинаем с 1 чела в таблице
				for leader in leaders: # создаём цикл для перебора словаря
					leader = self.client.get_user(int(leaders[position-1])) # получаем человека
					leader_score = event_members[str(leader.id)]['score'] # получаем очки этого человека
					e.add_field(name=f"{position} место:", value=f"{leader.mention} | очки: **{leader_score}**",inline=False) # заносим в его нашу таблицу
					position += 1 # строчка, чтобы далее перебирать всех
				await ctx.send(embed = e) # отправляет эмбед объявляя конец
				return # конец, ценок!

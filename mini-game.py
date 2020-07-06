"""
импортируем библиотеки:
import discord (pip install discord.py)
import random (встроенная)
import asyncio (встроенная)
from discord.ext import commands (идёт вместе с discord.py)
from discord.ext.commands import Bot (идёт вместе с discord.py)
import json (встроенная)
"""

@commands.command()
@commands.has_permissions(administrator = True)
async def флаги(self, ctx):
	with open('flags.json','r',encoding='utf8') as f: #файл с флагами открываем ага
		flags = json.load(f)
		count = 1 # подсчёт раундов
		while count <= 15: # цикл с раундами
			otvet = random.choice(flags['Флаги']) # выбирает рандомный флаг с ответом
			e = discord.Embed(title = f"Флаг {count}") # название
			e.set_image(url = otvet['url']) # картинка
			await ctx.send(embed = e) # отправляет
			def check(m): # проверка на ответ в канале команды
				return m.content == otvet['answer'] and ctx.channel == ctx.channel

			msg = await client.wait_for('message', check=check) # ждёт ответ
			em = discord.Embed(title = "Правильный ответ!")
			em.add_field(name = "Ответил:", value = f"{msg.author.mention}")
			em.add_field(name = "Правильный ответ:",value = f"{otvet['answer']}")
			await ctx.channel.send(embed = em) # отправляет сообщение шо какой-то чел прав
			count = count + 1 # следующий раунд
			await asyncio.sleep(1) # перерыв
			if count == 16: # проверка на конец игры
				e = discord.Embed(title = "Конец игры!", description = f"Ивент был проведён {ctx.author.mention}, и мы всем желаем удачи! Спасибо за участие!")
				await ctx.send(embed = e) # конец игры объявлен, всё!

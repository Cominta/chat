#NerChat 
#Импорт
import socket
import threading
import sys
import os
import time
import requests
from pid import PidFile

from tkinter import *
from tkinter import scrolledtext  
from tkinter import messagebox as mb

with PidFile():
	global server
	global onlinePeople

	server = ("195.138.84.212", 11719)
	alias = "Guest"
	onlinePeople = []
	rool = False
	exc = False

	#Параметры загрузочного окна
	screenMain = Tk()
	screenMain.geometry("300x300")
	screenMain.title("Load Screen")
	screenMain["bg"] = "#2C2F33"

	#Создание надписей
	labelLoad = Label(screenMain, text = "Loading...", bg = "#2C2F33", fg = "#FFFFFF", font = ("Whitney Bold", 20))
	labelLoadProc = Label(screenMain, text = "", bg = "#2C2F33", fg = "#FFFFFF", font = ("Whitney Medium", 10))

	#Вывод надписей
	labelLoad.pack(pady = (50, 0))
	labelLoadProc.pack()

	#Канва для загрузочной полоски
	canva = Canvas(screenMain, height = "15", width = "250", bg = "#2C2F33")
	canva.pack(side = "bottom", pady = (0, 60))

	def rec():
		global rool
		global alias
		alias = entry.get()
		f = open("name.txt", "w")
		f.write(alias)
		f.close()
		nickEntry.insert(0, alias)

		rool = True

	#Инициализация 
	def Init():
		global sock
		global screenMain
		global exc
		try:
			startLoad = canva.create_rectangle(3, 3, 0, 16, fill = "#614db3") #Создание загрузочной полоски

			labelLoadProc.configure(text = "Connecting to server...") #Измена надписи
			sock = ConnectToServer() #Подключенее к серверу

			#Удаление и создание новой полоски загрузки
			canva.delete(startLoad)
			connLoadSucc = canva.create_rectangle(3, 3, 80, 16, fill = "#614db3")

			labelLoadProc.configure(text = "Initing main screen...")
			screenMain = InitMainScreen(connLoadSucc) #Создание нового экрана

		except ConnectionRefusedError: #Если не удалось подключиться к серверу
			canva.delete(startLoad)
			exc = True
			errorLoad = canva.create_rectangle(3, 3, 250, 16, fill = "#941919")
			labelLoad.configure(text = "Unable to connect to server", font = ("Whitney Bold", 15))
			labelLoadProc.configure(text = "Shutdown")
			time.sleep(2)
			os.kill(os.getpid(), 9)

	def ConnectToServer(): #Подключение к серверу
		sock = socket.socket()
		sock.connect(server)
		
		return sock

	def InitMainScreen(connLoadSucc): #Создание главного окна
		#Создание главного окна
		global nickEntry
		global messageEntry
		global alias
		global logChat
		global rool
		global entry
		global onlinePerson
		global ipp
		#Создание интерфейса 
		messageEntry = Text(screenMain, width = 30, font = ("Whitney Medium", 10), bg = "#2C2F33", fg = "#FFFFFF")

		#Изминение загрузочной полоски
		canva.delete(connLoadSucc)
		messageLoadSucc = canva.create_rectangle(3, 3, 100, 16, fill = "#614db3")

		#Кнопка отправки
		buttonSend = Button(screenMain, text = "Send", bg = "#2C2F33", fg = "#FFFFFF", width = 6, font = ("Whitney Bold", 10), 
			activebackground = "#FFFFFF", activeforeground = "#000000", command = SendMessage)

		#Скролл бар для прокрутки чата
		scrollBar = Scrollbar(screenMain)

		#Еще полоска ^_^ 
		canva.delete(messageLoadSucc)
		ButtonScrollLoadSucc = canva.create_rectangle(3, 3, 150, 16, fill = "#614db3")

		#Лог чата
		logChat = Text(screenMain, state = "disabled", font = ("Whitney Medium", 10), yscrollcommand = scrollBar.set, bg = "#2C2F33", fg = "#FFFFFF")
		scrollBar.configure(command = logChat.yview)

		#Опять полоска
		canva.delete(ButtonScrollLoadSucc)
		LogChatLoadSucc = canva.create_rectangle(3, 3, 180, 16, fill = "#614db3")

		#Поле, надпись и кнопка для никнейма
		nickEntry = Entry(screenMain, font = ("Whitney", 11), bg = "#2C2F33", fg = "#FFFFFF")
		labelNickname = Label(text = "Nickname:", font = ("Whitney Bold", 13), bg = "#2C2F33", fg = "#FFFFFF")
		buttonNickname = Button(text = "Apply", bg = "#2C2F33", fg = "#FFFFFF", width = 6, font = ("Whitney Bold", 10), 
			activebackground = "#FFFFFF", activeforeground = "#000000", command = ApplyNickname)

		buttonExit = Button(text = "Exit", bg = "#2C2F33", fg = "#FFFFFF", width = 8, font = ("Whitney Bold", 13), 
			activebackground = "#FFFFFF", activeforeground = "#000000", command = lambda: os.kill(os.getpid(), 9))

		onlinePerson = Text(screenMain, state = "disabled", font = ("Whitney Medium", 11), bg = "#2C2F33", fg = "#FFFFFF")
		onlineLabel = Label(screenMain, text = "Online", font = ("Whitney Bold", 15), bg = "#2C2F33", fg = "#FFFFFF")

		#Люблю полоски)
		canva.delete(LogChatLoadSucc)
		LoadingSucc = canva.create_rectangle(3, 3, 250, 16, fill = "#614db3")

		#Изминение надписи
		labelLoad.configure(text = "Successfully Loading")
		labelLoadProc.configure(text = "Starting...")

		checkFile = os.path.isfile("name.txt") #Проверка, есть-ли в директории такой файл

		if checkFile == True: #Если есть
			#Опять глобальные переменные
			global reqALI
			global alias

			f = open("name.txt", "r")
			alias = f.read()
			nickEntry.insert(0, alias) #Вставка никнейма из файла в поле
			requstALI = "INF ALI " + alias

			reqALI = True
			rool = True

		else:
			#Если нет создается окно в котором вводится ник
			global window

			window = Toplevel(screenMain)
			window.geometry("150x100")
			window["bg"] = "#2C2F33"

			label = Label(window, text = "Write your nickname:", font = ("Whitney Bold", 10), bg = "#2C2F33", fg = "#FFFFFF")
			entry = Entry(window, font = ("Whitney Bold", 10))
			button = Button(window, text = "Apply", font = ("Whitney Bold", 10), command = rec, bg = "#2C2F33", fg = "#FFFFFF")

			label.pack(pady = (10, 0))
			entry.pack(fill = "x", pady = (13, 0))
			button.pack(fill = "x", pady = (15, 0))

		#Получение айпи и порта, удаление всего лишнего из него
		ipp = requests.get("https://ramziv.com/ip").text
		print(ipp)

		#Пока не введется ник на начальном экране, если файла с ником нет
		while True:
			if rool == True:
				try:
					window.destroy()

				except:
					pass

				#Отправка секретной инфы серверу
				requstIPP = "INF IPP " + ipp + ' ' + alias
				sock.sendto(requstIPP.encode("utf-8"), server)

				time.sleep(1)

				canva.destroy()

				#Изминение экрана под главное приложение
				screenMain.geometry("500x400")
				screenMain.protocol("WM_DELETE_WINDOW", lambda: os.kill(os.getpid(), 9))
				screenMain.title("NerChat")
				screenMain["bg"] = "#2C2F33"

				#Удаление старых надписей
				labelLoad.destroy()
				labelLoadProc.destroy()

				#Создание новых виджетов 
				logChat.place(x = 100, y = 5, width = 272, height = 320)
				messageEntry.place(x = 100, y = 330, height = 32)
				buttonSend.place(x = 315, y = 330, height = 32)
				nickEntry.place(x = 5, y = 35, height = 20, width = 90)
				labelNickname.place(x = 5, y = 5)
				buttonNickname.place(x = 5, y = 60, width = 90)
				scrollBar.place(x = 375, y = 5, height = 320)
				buttonExit.place(x = 403, y = 5)
				onlinePerson.place(x = 403, y = 80, width = 90, height = 245)
				onlineLabel.place(x = 415, y = 45)

				return screenMain

	def SendMessage(): #Отправка сообщения
		nick = ""
		nick = CheckNickname()
		message = ""

		if nick == True:
			message = messageEntry.get(1.0, END)

			if message.strip() == "":
				mb.showwarning("Warning", "You cant send empty message")
				messageEntry.delete(1.0, END)

			else:
				message = message.strip()
				message = "\n[" + alias + "]" + message
				sock.sendto(message.encode("utf-8"), server)
				messageEntry.delete(1.0, END)

	def ApplyNickname(): #Приминение никнейма
		global alias
		aliasOld = alias
		alias = nickEntry.get()
		if alias.strip() == "":
			mb.showwarning("Warning", "Cant apply '' nickname")
			nickEntry.insert(0, aliasOld)
			alias = aliasOld

		elif alias != aliasOld:
			f = open("name.txt", "w")
			f.write(alias)
			f.close()
			message = "\n" + aliasOld + f" Changed nickname to '{alias}'\n"
			sock.sendto(message.encode("utf-8"), server)
			mb.showinfo("Successfully", "Successfully changed nickname")

	def CheckNickname(): 
		if nickEntry.get() == "":
			mb.showwarning("Warning", "You cant send message without nickname")

			return False

		else:
			return True

	def AddMessageToLogChat(message): #После получения сообщения выводим его в лог чата
		logChat.configure(state = "normal")
		logChat.insert(END, message)
		logChat.configure(state = "disabled")

	def Receiver():
		global onlinePeople
		time.sleep(2)
		while True:
			if alias != "Guest":
				message = "\n" + alias + " Connected\n"
				sock.sendto(message.encode("utf-8"), server)

				while not exc:
					try:
						data = sock.recv(1024)
						data = data.decode("utf-8")

						if "Connected" in data:
							request = data.split()
							onlinePeople.append(request[0])

							onlinePerson.configure(state = "normal")
							onlinePerson.insert(END, request[0] + "\n")
							onlinePerson.configure(state = "disabled")

						elif "INF " in data:
							if "NICKS " in data:
								request = data.split()
								onlinePeople.append(request[3])

								onlinePerson.configure(state = "normal")

								for i in range(len(onlinePeople)):
									onlinePerson.insert(END, onlinePeople[i] + "\n")

								onlinePerson.configure(state = "disabled")

							elif "NICKDEL " in data:
								request = data.split()
								onlinePeople.remove(request[2])

								onlinePerson.configure(state = "normal")
								onlinePerson.delete(1.0, END)

								for i in range(len(onlinePeople)):
									onlinePerson.insert(END, onlinePeople[i] + "\n")
									
								onlinePerson.configure(state = "disabled")

						elif " Changed nickname to " in data:
							dataNew = data.split()

							aliasPersOld = dataNew[0]
							aliasPersNew = dataNew[4].replace("'", "")

							onlinePeople.remove(aliasPersOld)
							onlinePeople.append(aliasPersNew)

							onlinePerson.configure(state = "normal")
							onlinePerson.delete(1.0, END)

							for i in range(len(onlinePeople)):
								onlinePerson.insert(END, onlinePeople[i] + "\n")
									
							onlinePerson.configure(state = "disabled")

							AddMessageToLogChat(data)

							sock.sendto(("INF ALICHANG " + aliasPersOld + " " + aliasPersNew + " " + ipp).encode("utf-8"), server)

						else:
							AddMessageToLogChat(data)

					except ConnectionResetError:
						mb.showerror("Server error", "Server is down")
						time.sleep(1)
						os.kill(os.getpid(), 9)

	#Init
	tload = threading.Thread(target = Init)
	#tload.setDaemon(True)
	tload.start()

	#Запуск потока в котором получаем информацию
	tReceive = threading.Thread(target = Receiver)
	tReceive.start()

	screenMain.mainloop()

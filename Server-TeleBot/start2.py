# -*- coding: utf-8 -*-
#!/usr/bin/python

import telebot
from telebot import types
import time
import datetime
import imap4ssl
import idle
import mailboxes
import messages
from fetch_rfc822 import fetch
import configparser
import time, os, sys
from smtp import smtp
import requests
import threading

API_TOKEN="951787503:AAE6qHomMQn2wWBFOgqR-rEboUMgTrDtNOY"



class start(object):
	def __init__(self, r, bot):
		self.username=' '
		self.c=None
		self.files=[]
		self.mail=None
		self.receiver=''
		self.subject=''
		self.number=0
		self.size=0
		self.cnumber=0
		self.stop=0
		self.lowrep=[]
		self.msg=None
		self.threads=[]
		self.bot = bot
		self.text=''
		self.smtp = smtp()
		self.fetch = fetch()
		self.saveMail(r)


	#Responde a los comandos
	def welcome(self,message):
		try:
			sti = open('welcome.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			x = datetime.datetime.now()
			h = x.hour
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
			markup.add('Si', 'No')
			if(h<=12):
				r =  self.bot.send_message(message.chat.id, "Buenos días, bienvenido, ¿desea conectarse a su servicio de correo electrónico?", reply_markup=markup)
			elif(h<=18):
				r =  self.bot.send_message(message.chat.id, "Buenas tardes, bienvenido, ¿desea conectarse a su servicio de correo electrónico?", reply_markup=markup)
			else:
				r =  self.bot.send_message(message.chat.id, "Buenas noches, bienvenido, ¿desea conectarse a su servicio de correo electrónico?", reply_markup=markup)
			self.bot.register_next_step_handler(r, self.saveMail)

		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)

	def saveMail(self, message):

		try:
			if(message.text == 'Si'):
				email = self.bot.send_message(message.chat.id,"Ingrese su correo electrónico\nEjemplo: user@gmail.com")
				self.bot.register_next_step_handler(email, self.savePass)
			elif(message.text == 'No'): 
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				markup.add('Cerrar','Volver al inicio')
				r = self.bot.send_message(message.chat.id, "¿Qué desea hacer?",reply_markup=markup)
				self.bot.register_next_step_handler(r, self.savePass)
			else:
				print(message)
				self.bot.send_message(message.chat.id,"Por favor, responda con 'Si' o 'No'")
				self.welcome(message)
		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)


	def nowWhat(self,message):
		try:
				if(message.text == 'Cancelar'):
					markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
					markup.add('Cerrar','Volver al inicio')
					p = self.bot.send_message(message.chat.id, "¿Qué desea hacer?",reply_markup=markup)
					self.bot.register_next_step_handler(p, self.savePass)
				else:
					password=message.text
					sti = open('wait.webp', 'rb')
					self.bot.send_sticker(message.chat.id, sti)
					#self.bot.send_message(message.chat.id,"Espere...")
					config = configparser.ConfigParser(allow_no_value=True)
					config.read("config.txt")
					retry=0
					try :
						self.c = imap4ssl.open_connection(config,self.username,password)
						self.smtp.connection(self.username,password)
					except BaseException as be:
						sti = open('fail.webp', 'rb')
						self.bot.send_sticker(message.chat.id, sti)
						#self.bot.send_message(message.chat.id,'No se pudo establecer la conexión.')
						self.bot.send_message(message.chat.id,'¿Es la informacion provista correcta?.')
						print(be)
						retry=1
					if(retry==0):
						#self.bot.send_message(message.chat.id,"La conexion se establecio correctamente.")
						sti = open('success.webp', 'rb')
						self.bot.send_sticker(message.chat.id, sti)
						markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
						markup1.add('Revisar Inbox','Enviar Email')
						o = self.bot.send_message(message.chat.id, "¿Qué desea hacer?",reply_markup=markup1)
						self.bot.register_next_step_handler(o, self.sendAction)
					else:
						markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
						markup.add('Si', 'No')
						r =  self.bot.send_message(message.chat.id, "¿Desea volver a intentar establecer la conexion?", reply_markup=markup)
						self.bot.register_next_step_handler(r, self.saveMail)

		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)


	def savePass(self, message):
		try:
			if(message.text == 'Cerrar'):
				r = self.bot.send_message(message.chat.id,"Adiós.")
			elif(message.text == 'Volver al inicio'):
				#r = self.bot.send_message(message.chat.id,"Volvamos al inicio.")
				self.welcome(message)
			else:
				self.username=message.text
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				markup.add('Cancelar')
				r = self.bot.send_message(message.chat.id, "Ingrese su contraseña",reply_markup=markup)
				self.bot.register_next_step_handler(r, self.nowWhat)
		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)

	def sendAction(self,message):
		try:
			if(message.text == 'Revisar Inbox'):
				self.mail=message
				idler = idle.Idler(self.c, self.fetch,readonly=False)
				idler.start()
				#self.bot.send_message(message.chat.id, 'Espere mientras se cargan los correos.')
				sti = open('waitm.webp', 'rb')
				self.bot.send_sticker(message.chat.id, sti)
				#markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				#markup.add('Cancelar')
				#r = self.bot.send_message(message.chat.id, "Recuerde que puede cancelar en cualquier momento",reply_markup=markup)
				while(idler.iddling==0): 
					None
				
				self.size=len(self.fetch.emails)
				noreaded="Usted tiene "+str(self.size)+" sin leer."
				self.bot.send_message(message.chat.id, noreaded)
				q = self.bot.send_message(message.chat.id, "Ingrese el numero de correos que desea visualizar.")
		
				def selectQuantity(message):
					try:
						self.number=int(message.text)
						if self.number>len(self.fetch.emails):
							self.number=len(self.fetch.emails)
						if self.number<0 :
							self.number=0
						self.cnumber=self.number
						markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
						markup.add('Recientes','Viejos')
						r = self.bot.send_message(message.chat.id, "Ingrese en que orden se quieren los correos.",reply_markup=markup)
						def sortMail(message):
							if(message.text=='Recientes'):
								s=len(self.fetch.emails)-1

								#self.bot.send_message(message.chat.id, 'Enviando.....')
								while(self.number>0):
									line=self.fetch.emails.pop(s)
									self.bot.send_message(message.chat.id,line)
									attachments=self.fetch.attach.pop(s)
									j=len(attachments)
									while(j>0):
										file=attachments.pop(0)
										k=0
										while(True):
											if(file[k]==']'):
												break
											k=k+1

										ogfile=file[k+1:len(file)]
										os.rename(file,ogfile)
										doc = open(ogfile,'rb')
										self.bot.send_document(message.chat.id, doc)
										j=j-1
									s=s-1
									self.number=self.number-1

							elif(message.text)=='Viejos':
								#self.bot.send_message(message.chat.id, 'Enviando.....')
								while(self.number>0):
									line=self.fetch.emails.pop(0)
									self.bot.send_message(message.chat.id,line)
									attachments=self.fetch.attach.pop(0)
									j=len(attachments)
									while(j>0):
										file=attachments.pop(0)
										k=0
										while(True):
											if(file[k]==']'):
												break
											k=k+1

										ogfile=file[k+1:len(file)]
										os.rename(file,ogfile)
										doc = open(ogfile,'rb')
										self.bot.send_document(message.chat.id, doc)
										j=j-1
									self.number=self.number-1

							markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
							markup.add('Continuar la conexion','Cancelar')
							o = self.bot.send_message(message.chat.id, "¿Desea esperar a que lleguen nuevos correos?",reply_markup=markup)
							def selectNextMove(message):
								try:
									if (message.text=='Continuar la conexion'):
										markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
										markup.add('Cancelar')
										p = self.bot.send_message(message.chat.id, "Puede cancelar en cualquier momento.",reply_markup=markup)
										aux=self.size-self.cnumber
										while(aux>0):
											self.fetch.emails.pop(0)
											self.fetch.attach.pop(0)
											aux=aux-1
										self.stop=0

										def killWhile(message):
											self.stop=1
											self.cancelAction(message)

										self.bot.register_next_step_handler(p, killWhile)
										while(self.stop==0):
											if(self.fetch.emails):
												line=self.fetch.emails.pop(0)
												self.bot.send_message(message.chat.id,line)
												attachments=self.fetch.attach.pop(0)
												j=len(attachments)
												while(j>0):
													file=attachments.pop(0)
													k=0
													while(True):
														if(file[k]==']'):
															break
														k=k+1

													ogfile=file[k+1:len(file)]
													os.rename(file,ogfile)
													doc = open(ogfile,'rb')
													self.bot.send_document(message.chat.id, doc)
													j=j-1
											
										print("They try to kill me")
										idler.iddling=0
										try:
										    idler.stop()
										    idler.join()
										except:
										    print("Couldn't join idler.")
									elif(message.text=='Cancelar'):
										self.cancelAction(message)
										idler.iddling=0
										try:
										    idler.stop()
										    idler.join()
										except:
										    print("Couldn't join idler.")

										
								except Exception as e:
									self.bot.send_message(message.chat.id, 'Disculpe')
									sti = open('error.webp', 'rb')
									self.bot.send_sticker(message.chat.id, sti)
									print(e)
							self.bot.register_next_step_handler(o, selectNextMove)
						self.bot.register_next_step_handler(r, sortMail)
					except Exception as e:
						sti = open('error.webp', 'rb')
						self.bot.send_sticker(message.chat.id, sti)
						self.bot.send_message(message.chat.id, 'La entrada debe ser un número entero')
						self.cancelAction(message)
						print(e)	
				self.bot.register_next_step_handler(q, selectQuantity)

				

			elif(message.text == 'Enviar Email'):
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				markup.add('Cancelar')
				r = self.bot.send_message(message.chat.id, "Ingrese el destinatario.",reply_markup=markup)
				self.bot.register_next_step_handler(r, self.saveReceiver)

			elif(message.text=='Cancelar'):
				self.cancelAction(message)
		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)


	def saveReceiver(self,message):
		if(message.text == 'Cancelar'):
			self.cancelAction(message)
		else:
			self.receiver=message.text
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
			markup.add('Cancelar')
			r = self.bot.send_message(message.chat.id, "Ingrese el asunto",reply_markup=markup)
			self.bot.register_next_step_handler(r, self.saveSubject)


	def saveSubject(self,message):
		if(message.text == 'Cancelar'):
			self.cancelAction(message)
		else:
			self.subject=message.text
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
			markup.add('Cancelar')
			r = self.bot.send_message(message.chat.id, "Ingrese el mensaje a enviar.",reply_markup=markup)
			self.bot.register_next_step_handler(r, self.intermedio1)

	def intermedio1(self,message):
			self.text = message.text
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
			markup.add('Si','No')
			r = self.bot.send_message(message.chat.id, "¿Desea adjuntar algún archivo?",reply_markup=markup)
			self.bot.register_next_step_handler(r, self.intermedio2)

	def intermedio2(self,message):
		if(message.text=='No'):
			self.sendMessage(message)
		elif(message.text=='Si'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
			markup.add('Listo')
			r = self.bot.send_message(message.chat.id, "Adjunte los archivos a continuación.",reply_markup=markup)
			self.bot.register_next_step_handler(r, self.attachments)
		else:
			self.cancelAction(message)

	def attachments(self,message):
		if(message.text==None):
			file_info=None
			#requests.get('https://api.telegram.org/self.bot{0}/getFile?file_id=the_file_id'.format(API_TOKEN)))

			def downloadAction(message):
				if(message.content_type=='photo'):
					file_info = self.bot.get_file(message.photo[-1].file_id)

				elif(message.content_type=='audio'):
					file_info = self.bot.get_file(message.audio.file_id)

				elif(message.content_type=='voice'):
					file_info = self.bot.get_file(message.voice.file_id)

				elif(message.content_type=='video'):
					file_info = self.bot.get_file(message.video.file_id)

				elif(message.content_type=='video_note'):
					file_info = self.bot.get_file(message.video_note.file_id)

				elif(message.content_type=='sticker'):
					file_info = self.bot.get_file(message.sticker.file_id)

				else:
					file_info = self.bot.get_file(message.document.file_id)
				
				#if(message.content_type=='photo'):
				#exec("file_info = self.bot.get_file(message.{}.file_id)".format(message.content_type))
				# file_info = self.bot.get_file(message.content_type.file_id)
				print(file_info)
				file = self.bot.download_file(file_info.file_path)
				name=str(file_info.file_path)
				i=0
				while(i<len(name)):
					if(name[i]=='/'):
						break
					i=i+1

				name=name[i+1:len(name)]
				#print(file)
				self.files.append([file,name])
				self.bot.reply_to(message, 'Recibido.')
			
			t=threading.Thread(target=downloadAction,args=(message,))
			self.threads.append(t)
			t.start()
			self.bot.register_next_step_handler(message, self.attachments)
		elif(message.text=='Listo'):
			for hilo in self.threads:
				hilo.join()
			sti = open('wait_correo.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			#self.bot.send_message(message.chat.id, 'Cargando correo...')
			self.sendMessage(message)
			self.files=[]
			self.threads=[]
		else:
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			self.bot.send_message(message.chat.id, 'La entrada debe ser un archivo')
			self.cancelAction(message)



	def sendMessage(self,message):
		try:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
			if(message.text == 'Cancelar'):
				self.cancelAction(message)
			else:
				text=message.text
				try:
					self.lowrep,limitsize,self.msg=self.smtp.checkMessage(self.username,self.receiver,self.subject,self.text,self.files)
					if (limitsize==1):
						markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
						markup.add('Si', 'No')
						r =  self.bot.send_message(message.chat.id, 'El tamaño es mayor a 25MB.¿Desea Continuar?', reply_markup=markup)
						def sizeLimit(message):
							try :
								if(message.text=='No'):
									raise Exception("No se quiere el archivo con mas de 25MB")
									
								elif(message.text=='Si'):
									self.sendMessage2(message)
							except Exception as z:
								print(z)
								sti = open('no.webp', 'rb')
								self.bot.send_sticker(message.chat.id, sti)
								#self.bot.send_message(message.chat.id, 'El mensaje no pudo ser enviado.')
								self.cancelAction(message)
						self.bot.register_next_step_handler(r, sizeLimit)
					else:
						self.sendMessage2(message)

				except Exception as q:
					print(q)
					self.bot.send_message(message.chat.id, 'Disculpe')
					sti = open('error.webp', 'rb')
					self.bot.send_sticker(message.chat.id, sti)
					self.cancelAction(message)				

		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)

	def sendMessage2(self,message):
		try:
			
			if(self.lowrep!=[]):
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				markup.add('Si', 'No')
				self.bot.send_message(message.chat.id,'El correo posee URLs de baja reputacion')
				self.bot.send_message(message.chat.id,'Los cuales son: '+str(self.lowrep))
				x =  self.bot.send_message(message.chat.id, '¿Desea Continuar?', reply_markup=markup)

				def lowerRep(message):
					try :
						if(message.text=='No'):
							raise Exception("Cancelacion de envio por baja repuacion de URL")
							
						elif(message.text=='Si'):
							self.sendMessage3(message)


					except Exception as z:
						print(z)
						sti = open('no.webp', 'rb')
						self.bot.send_sticker(message.chat.id, sti)
						#self.bot.send_message(message.chat.id, 'El mensaje no pudo ser enviado.')
						self.cancelAction(message)

				self.bot.register_next_step_handler(x, lowerRep)
			else:	
				self.sendMessage3(message)

		except Exception as q:
			print(q)
			sti = open('no.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			#self.bot.send_message(message.chat.id, 'El mensaje no pudo ser enviado.')
			self.cancelAction(message)

	def sendMessage3(self,message):		
		try:
			self.smtp.sendMessage(self.msg,self.username,self.receiver)
			sti = open('correo_enviado.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			#self.bot.send_message(message.chat.id,'El mensaje se mando satisfactoriamente')
			self.cancelAction(message)
			return

		except Exception as q:
			print(q)
			sti = open('no.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			#self.bot.send_message(message.chat.id, 'El mensaje no pudo ser enviado.')
			self.cancelAction(message)

	def cancelAction(self,message):
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		markup.add('Cerrar','Realizar otra Accion')
		p = self.bot.send_message(message.chat.id, "¿Qué desea hacer?",reply_markup=markup)
		self.bot.register_next_step_handler(p, self.continueAction)


	def continueAction(self,message):
		try:
				if(message.text == 'Realizar otra Accion'):
					markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
					markup.add('Revisar Inbox','Enviar Email')
					o = self.bot.send_message(message.chat.id, "¿Qué desea hacer?",reply_markup=markup)
					self.bot.register_next_step_handler(o, self.sendAction)

				elif(message.text=='Cerrar'):
					self.bot.send_message(message.chat.id,"Adiós")
					self.c.logout()
					self.smtp.conn.quit()

				else:
					self.cancelAction(message)

		except Exception as e:
			self.bot.send_message(message.chat.id, 'Disculpe')
			sti = open('error.webp', 'rb')
			self.bot.send_sticker(message.chat.id, sti)
			print(e)

	#@self.bot.message_handler(func = lambda message:True) para responder cualquier cosa
	

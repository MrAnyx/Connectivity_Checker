import os
import time
import sqlite3 as sql
from tkinter import *
from pynput.keyboard import Key, Controller
from tkinter import messagebox



def frame_label():
	global frame5,variable, mini, maxi, avg, label1, label2, label3
	if(variable == 0):
		variable = 1
		frame5 = Frame(fenetre, bg = "#969696")
		mini = StringVar()
		maxi = StringVar()
		avg = StringVar()
		mini.set("{}".format(minimum))
		maxi.set("{}".format(maximum))
		avg.set("{}".format(average))

		label1 = Label(frame5, textvariable = mini, bg = "white", font = ("", 12)).pack(fill = X)
		label2 = Label(frame5, textvariable = maxi, bg = "white", font = ("", 12)).pack(fill = X, pady = 2)
		label3 = Label(frame5, textvariable = avg, bg = "white", font = ("", 12)).pack(fill = X)
	
		frame5.pack(fill = X, padx = 10, pady = (5,10))
	else:
		pass


def destroy():
	global variable
	
	if(variable == 1):
		frame5.destroy()
		variable = 0
	else:
		pass

def transition():
	if(value_radio.get() == 1):
		destroy()
	else:
		frame_label()

def exit():
	fenetre.destroy()

def cmd():
	os.system("start cmd")

def affiche_serveur():
	test = cursor.execute("""SELECT ip, serveur FROM DNS""").fetchall()
	for n in test:
		myliste.insert(END, "{} | {}".format(n[0], n[1]))

def remove_all():
	myliste.delete(0, END)

def actualiser():
	remove_all()
	affiche_serveur()

def raz():
	value_entry.set("")
	valeur_spinbox.set("1")
	value_radio.set(0)
	frame_label()
	actualiser()
	mini.set("")
	maxi.set("")
	avg.set("")





def ping1(arg, nb):
	global minimum, maximum, average

	ping = os.popen("ping -n {} {}".format(nb, arg), 'r')
	ligne = ping.readlines()

	ligne_ping = ligne[len(ligne)-1]
	liste_ligne_ping = ligne_ping.split(",")

	for i in range(len(liste_ligne_ping)):
		liste_ligne_ping[i] = liste_ligne_ping[i].strip()
	

	connexion_min = liste_ligne_ping[0]
	connexion_max = liste_ligne_ping[1]
	connexion_avg = liste_ligne_ping[2]

	if(len(connexion_min.split('q')) > 1):
		connexion_min = "{} paquet(s) envoyé(s)".format(valeur_spinbox.get())
		connexion_max = "0 paquet reçu"
		connexion_avg = "Perte : 100%"

	mini.set("{}".format(connexion_min))
	maxi.set("{}".format(connexion_max))
	avg.set("{}".format(connexion_avg))

	minimum = mini.get()
	maximum = maxi.get()
	average = avg.get()

	
def ping_cmd(arg, nb):
	os.system("start cmd.exe")
	keyboard = Controller()
	time.sleep(0.5)
	ping = "ping -n {} {}".format(nb, arg)
	for char in ping:
		keyboard.press(char)
		keyboard.release(char)
		time.sleep(0.02)
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)


def validate():
	if(value_radio.get() == 0):
		if(value_entry.get() != ""):
			try:
				valeur = value_entry.get().split(' ')
				# compteur_test = cursor.execute("""SELECT * FROM DNS WHERE ip LIKE "{}" and serveur like "{}" """.format(valeur[0], valeur[1])).fetchall()
				
				# for n in compteur_test:
				# 	compteur_final = int(n[3])



				cursor.execute("""INSERT INTO DNS (ip, serveur) VALUES (?, ?, ?)""", (valeur[0], valeur[1]))
				db.commit()
				actualiser()
				raz()
				yolo = valeur[0]
				ping1(yolo, str(valeur_spinbox.get()))
				frame_label()

			except:
				messagebox.showerror("Error | Add", "Veuillez remplir correctement le champs de\nsaisis puis ré-essayez [127.0.0.1 locashost] ou selectionner un element dans la liste")

		else:
			try:
				ping2 = myliste.get(myliste.curselection())
				liste_ping = ping2.split(' | ')
				ping_final = liste_ping[0]
				ping1(ping_final, str(valeur_spinbox.get()))
				frame_label()
				
			except:
				messagebox.showerror("Error | Add", "Veuillez remplir correctement le champs de\nsaisis puis ré-essayez [127.0.0.1 locashost] ou selectionner un element dans la liste")
	else: #value_radio.get() == 1
		if(value_entry.get() != ""):
			ping_cmd(value_entry.get(), valeur_spinbox.get())
			
			
		else:
			try:
				ping2 = myliste.get(myliste.curselection())
				liste_ping = ping2.split(' | ')
				ping_final = liste_ping[0]

				ping_cmd(ping_final, valeur_spinbox.get())
				
			except:
				messagebox.showerror("Error | Add", "Veuillez remplir correctement le champs de\nsaisis puis ré-essayez [127.0.0.1 locashost] ou selectionner un element dans la liste")
	
		
def supprimer():
	try:
		valeur_suppr = myliste.get(myliste.curselection())
		liste_valeur_suppr = valeur_suppr.split(" | ")
		cursor.execute("""DELETE FROM DNS WHERE ip LIKE "%{}%" AND serveur LIKE "%{}%" """.format(liste_valeur_suppr[0], liste_valeur_suppr[1]))
		db.commit()
		actualiser()
	except:
		messagebox.showerror("Error | Delete", "Veuillez selectioner un élément à supprimer")

def research():
	if(value_entry.get() != ""):
		liste = cursor.execute("""SELECT ip, serveur FROM DNS WHERE serveur LIKE "%{}%" """.format(value_entry.get())).fetchall()
		if(len(liste) > 0):
			for n in liste:
				myliste.delete(0, END)
				myliste.insert(END, "{} | {}".format(n[0], n[1]))
				value_entry.set("")		
		else:
			liste = cursor.execute("""SELECT ip, serveur FROM DNS WHERE ip LIKE "%{}%" """.format(value_entry.get())).fetchall()
			if(len(liste) > 0):
				for n in liste:
					myliste.delete(0, END)
					myliste.insert(END, "{} | {}".format(n[0], n[1]))
					value_entry.set("")	
			else:
				messagebox.showinfo("Info | Research", "le champ recherché n'existe pas.")				
	else:
		messagebox.showerror("Error | Research", "Veuillez remplir correctement le champs de\nsaisis puis ré-essayez [127.0.0.1 ou locashost]")


def supprimer_all():

	cursor.execute("""DROP TABLE DNS""")
	db.commit()
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS DNS(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		serveur TEXT NOT NULL,
		ip TEXT NOT NULL,
		compteur INTEGER)
	""")
	actualiser()


variable_couleur_label = 0 #couleur blanche et 1 pour la couleur en fonction du ping
variable = 0
minimum = ""
maximum = ""
average = ""

db = sql.connect("database_ping.db")
cursor = db.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS DNS(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	serveur TEXT NOT NULL,
	ip TEXT NOT NULL,
	compteur INTEGER)
""")



fenetre = Tk()
fenetre.title("Checker")
fenetre.iconbitmap("icone.ico")
fenetre.configure(bg = "#969696")
fenetre.resizable(width = FALSE, height = FALSE)

################### ListeBox ######################

frame1 = Frame(fenetre, bg = "#969696")


scrollbar = Scrollbar(frame1)
scrollbar.pack(side = RIGHT, fill = Y)

myliste = Listbox(frame1, yscrollcommand = scrollbar.set , width = 42)
affiche_serveur()
myliste.pack(side = LEFT, fill = X)

scrollbar.config(command = myliste.yview)

frame1.pack(fill = X, padx = 10, pady = (10,5))

################### Entry #########################

frame2 = Frame(fenetre, bg = "#969696")

value_entry = StringVar()
valeur_spinbox = IntVar()
entry_valider_chercher = Entry(frame2, bg = "bisque", textvariable = value_entry, selectbackground = "bisque", selectforeground = "red", font = ("", 12), width = 24).pack(side = LEFT, fill = X)
spin_box = Spinbox(frame2, from_ = 1, to= 10, width = 4, font = ("", 10), textvariable = valeur_spinbox).pack(side = LEFT, fill = X, padx = (10,0))
frame2.pack(fill = X, padx = 10, pady = (5,5))

#################### Bouton #######################

frame3 = Frame(fenetre, bg = "#969696")

bouton_valider = Button(frame3, text = "Validate", bg = "#515151", fg = "white", font = ("", 10), command = validate).pack(side = LEFT, fill = X, expand = 1, padx = (0,5))
bouton_rechercher = Button(frame3, text = "Research", bg = "#515151", fg = "white", font = ("", 10), command = research).pack(side = LEFT, fill = X, expand = 1, padx = (5,0))

frame3.pack(fill = X, padx = 10, pady = (5,5))

#################### Radio button #################

frame4 = Frame(fenetre, bg = "#969696")

value_radio = IntVar()

radio_button1 = Radiobutton(frame4, text = "None", variable = value_radio, value = 0, bg = "#969696", activebackground = "#969696", command = transition).pack(side = LEFT, fill = X, expand = 1)
radio_button2 = Radiobutton(frame4, text = "Command Prompt", variable = value_radio, value = 1, bg = "#969696", activebackground = "#969696", command = transition).pack(side = LEFT, fill = X, expand = 1)

frame4.pack(fill = X, padx = 10, pady = (2,5))

###################### Label ######################

frame_label()

###################### Menu ######################
menubar = Menu(fenetre)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Exit", command = exit)
filemenu.add_separator()
filemenu.add_command(label = "Open Command prompt", command = cmd)
menubar.add_cascade(label="File", menu=filemenu)

edit = Menu(menubar, tearoff = 0)
edit.add_command(label = "Delete", command = supprimer)
edit.add_command(label = "Delete All", command = supprimer_all)
edit.add_command(label = "RaZ", command = raz)
edit.add_command(label = "test", command = frame_label)
menubar.add_cascade(label = "Edit", menu = edit)


fenetre.config(menu = menubar)

fenetre.mainloop()

# TODO
# 4) automatické ukládání
# 5) Automatický datetime na vrcholu každé sekce

from tkinter import Tk, END, Label, N, W, S, E, LEFT, RIGHT, Menu, Frame, Button, Listbox, SINGLE, ACTIVE, Scrollbar, VERTICAL, BooleanVar, GROOVE
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import os
import datetime
import webbrowser # pro otevření URL v prohlížeči
from appdirs import user_data_dir

# balíčky v projektovém adresáři (aka moje balíčky)
import validations
import configJson


def parseText(text):
    " Rozebere text na jednotlivé řádky a zavolá na ně funkci na rozbor řádku. "
    textLines = text.split("\n")

    global textList
    textList = []

    i = 0
    while i < len(textLines):
        parseLine(textLines[i])
        i += 1


def parseLine(line):
    " Rozpáře příchozí string na slova. Pokud je první klíčovým slovem, tak přidá záznam do slovníku. "
    item = line.split(" ")
    if item[0].upper() in keywords:
        global textList
        textList.append(item)





def retrieveInput():
    " Vrátí obsah textového pole. "
    text = textField.get("1.0",END)
    obsah[listbox.get(ACTIVE)] = text.strip()
    return text



def toClipboard(label):
    "Zkopíruje kliknutý text do schránky"
    root.clipboard_clear()
    root.clipboard_append(label["text"])
    print(label["text"])



def coJeNoveho():
    global verze
    messagebox.showinfo("Co je nového",
            """Co je nového v aktuální verzi {}:\n
- Nové klíčové slovo DATUM (formát 31.01.2017)
- Manuál k aplikaci v nápovědě\n\n
Co bylo nového ve verzi 0.6\n
- Možnost vrácení zpět uživatelského nastavení
- Validace bankovního účtu
- Klíčové slovo BUCET je nyní jen UCET\n\n
Co bylo nového ve verzi 0.5\n
- Nová klíčová slova (JMENO, INFO, EMAIL)
- Přepínač "vždy navrchu"
- Konfigurační soubor si ukládá nastavení (c:\\Users\\_login_\\AppData\\Roaming\\cpoj_okolafa\\LPUPad\\)\n\n
Co bylo nového ve verzi 0.4\n
- Kontextové popisky pro vyhledávání na webu se pojmenovávají podle typu klíčovésho slova.
- Přidány vertikální záložky. (Možno použít Klávesouvou zkratku Ctrl+N)
- Sekce Co je nového :)
            """ .format(verze)
        )


def manual():
    os.system("start "+'\\\\czcsfs216\\Data1\\CDAp\\LPUNZP\\LPUPad\\manual.pdf')

def oProgramu():
    global verze
    messagebox.showinfo(
            "O programu LPUPad",
            "LPUPad verze {},\nbuild {:%Y-%m-%d}\n\nV roce {:%Y} vyrobil Ondřej Kolafa\n\nondrej.kolafa@ceskapojistovna.cz"  .format(verze, datetime.datetime.now(), datetime.datetime.now())
        )

def new():
    global defaultText
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    listbox.insert(END, time)
    print("Počet prvků v listboxu: ", listbox.size())
    listbox.selection_clear(0, listbox.size()-1)
    listbox.selection_set(listbox.size()-1)
    listbox.activate(listbox.size()-1)
    obsah[listbox.get(ACTIVE)] = ""
    textField.delete(1.0, END)
    textField.insert(1.0, defaultText)
    keypressed("a")

#    selection = listbox.curselection()
#    value = listbox.get(selection[0])
#    print( "%s" % value)


def fileSave():
    filename = asksaveasfilename(defaultextension='.txt',filetypes = (('Text files', '*.txt'),('All files', '*.*')))
    if len(filename) < 1:
        return
    else:
        file = open(filename, mode = 'w')
        file.write(textField.get("1.0",END))
        file.close()

def fileOpen():
    filename = askopenfilename(defaultextension='.txt',filetypes = (('Text files', '*.txt'),('All files', '*.*')))
    if len(filename) < 1:
        return
    else:
        file = open(filename, mode = 'r')
        textField.delete(1.0, END)
        textField.insert(END, file.read())
        file.close()
        keypressed("a")



def contextMenu(event, filterValue, key):
    print("Kliknuto pravým!", key, filterValue)
    if key in ("VIN", "RZ", "SPZ", "IC", "ICO"):
        if key == "VIN": labelValue = "Najdi VIN na cebia.com"
        if key in ("SPZ", "RZ"): labelValue = "Najdi RZ na cebia.com"
        if key in ("IC", "ICO"): labelValue = "Najdi IČO na ares.cz"
        popup_menu = Menu(root, tearoff=0)
        popup_menu.add_command(label=labelValue,
              command= lambda: getInformation(filterValue, key))
        popup_menu.tk_popup(event.x_root, event.y_root, 0)



def getInformation(filterValue, key):
    print("Searching for data: ", key, filterValue)
    if (key == "ICO" or key == "IC"):
        url = "http://wwwinfo.mfcr.cz/cgi-bin/ares/ares_es.cgi?jazyk=cz&ico="+filterValue+"&cestina=cestina&maxpoc=200&xml=1"
        webbrowser.open_new(url)
    if (key == "SPZ" or key == "RZ"):
        url = "http://cebia.com/checklease/frmHledej.aspx/?spz="+filterValue
        webbrowser.open_new(url)
    if (key == "VIN"):
        url = "http://cebia.com/checklease/frmHledej.aspx/?VIN="+filterValue
        webbrowser.open_new(url)


def setVzdyNahore():
    global path
    global config
    if vzdyNahore.get(): alwaysOn = 1
    else: alwaysOn = 0
    print("Vždy nahoře? ", vzdyNahore.get())
    root.wm_attributes("-topmost", alwaysOn)
    configJson.setVzdyNahore(config, alwaysOn)
    configJson.saveConfig(path, config)


def saveDefaultText():
    global path
    global config
    configJson.setDefaultText(config, textField.get("1.0",END))
    configJson.saveConfig(path, config)

def defaultSettings():
    result = messagebox.askquestion("Delete", "Pro vrácení do původního nastavení je vyžadováno zavření programu.\n\nChcete nyní vrátit zpět výchozí nastavení?", icon='warning')
    if result == 'yes':
        print("Vracím do výchozího nastavení")
        global path
        global config
        global root
        configJson.returnToDefault(path)
        print("Vráceno zpět")
        root.destroy()
    else:
        print("Vrácení do výchození nastavení bylo odmítnuto.")




def shrtNew(event):
    new()

def shrtFOpen(event):
    fileOpen()

def shrtFSave(event):
    fileSave()

def shrtOProgramu(event):
    oProgramu()





def keypressed(Event):
    """
    Při každém stisku klávesy smaže všechny labely z pravého sloupce,
    znovu projde napsaný text a vytvoří nové labely.

    textList = napsaný text (rozparsovaný do list[list])
    item = řádek textu, sktruktura by měla být následující (typ, hodnota, popis1, popis2, ...)
    """
    i = 0
    parseText(retrieveInput())
#    print(obsah)

    for label in labelFrame.grid_slaves():
        label.grid_forget()

    for item in textList:
        key = item[0].upper()
        if (len(item) >= 2 and len(item[1]) > 0) : # Vytváříme label pouze pokud má i popisek (tedy pole má více než dva prvky)
            lKeyTemp=Label(labelFrame, text=key, width=6, justify=LEFT, anchor=W, bg="LightSkyBlue1")
            lKeyTemp.grid(row=i*2, column=0, sticky=(N, W), padx=10, pady=1)

            validation = validations.validateValue(item)
            valuePU = validation[1]
            if validation[0] == "ok":
                fgColor = "green"
            elif validation[0] == "nok":
                fgColor = "red"
            else :
                fgColor = "blue"

            lValueTemp=Label(labelFrame, width=19, wraplength=115, text=valuePU, fg=fgColor, font= "Helvetica 8 underline", cursor="hand2", justify=LEFT, anchor=W, bg="LightSkyBlue1")
            lValueTemp.grid(row=i*2, column=1, sticky=(N, W), padx=1, pady=1)
            lValueTemp.bind("<Button-1>", lambda event, lValueTemp=lValueTemp: toClipboard(lValueTemp))
            lValueTemp.bind("<Button-3>", lambda event, filterValue=lValueTemp["text"], key=key: contextMenu(event, filterValue, key))

            if (len(item) > 2 and key not in ('JMENO', 'INFO', 'DATUM')) :
                lValueDesc=Label(labelFrame, text=item[2:], width=19, fg="gray", font= "Helvetica 8", wraplength=115, justify=RIGHT, anchor=W, bg="LightSkyBlue1")
                lValueDesc.grid(row=i*2+1, column=1, sticky=(N, W, S, E), padx=1, pady=1)
#                lValueDesc.bind("<Button-1>", lambda event, lValueDesc=lValueDesc: toClipboard(lValueDesc))

        i += 1

def ListboxSelect(Event):
    print("Listbox kliknuto", Event)
    global obsah
    print("vybráno:", listbox.curselection())
    if len(listbox.curselection()) > 0 :
        listbox.activate(listbox.curselection())
        textField.delete(1.0, END)
        textField.insert(END, obsah[listbox.get(ACTIVE)])
        keypressed("a")




################################
################################
#      Aplikační proměnné      #
################################
################################

verze = "0.7"

appauthor = "cpoj_okolafa"
appname = "LPUPad"

path = user_data_dir(appname, appauthor, roaming=True)
config = {}
config = configJson.readConfig(path)
configJson.saveConfig(path, config)


keywords = ["PU", "PS", "RC", "ICO", "UCET", "TEL", "RZ", "VIN", "JMENO", "EMAIL", "INFO", "DATUM"]
keywordsLabel = ", ".join(keywords[:7])+"\n"+", ".join(keywords[7:]) # Toto je jen kvůli zobrazení klíčových slov v GUI na dva řádky
obsah = {}
obsah[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = ""
defaultText = config["defaultText"]
textList = []


################################
################################
#        Vytváření GUI         #
################################
################################

root = Tk()
root.wm_attributes("-topmost", config["alwaysOn"]) # Stay on top featura
root.geometry("650x700+900+200")

root.title("LPU Pad | " + os.getlogin())

menubar = Menu(root)

# Rozbalovací menu Soubor
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nový panel", command=new, accelerator="Ctrl+N")
filemenu.add_command(label="Otevřít", command=fileOpen, accelerator="Ctrl+O")
filemenu.add_command(label="Uložit", command=fileSave, accelerator="Ctrl+S")
filemenu.add_separator()
filemenu.add_command(label="Konec", command=root.quit, accelerator="Alt-F4")
menubar.add_cascade(label="Soubor", menu=filemenu)

root.bind('<Control-n>', shrtNew)
root.bind('<Control-o>', shrtFOpen)
root.bind('<Control-s>', shrtFSave)
root.bind('<F1>', shrtOProgramu)

vzdyNahore = BooleanVar()
if config["alwaysOn"] == 1 : vzdyNahore.set(True)
else: vzdyNahore.set(False)

view_menu = Menu(menubar, tearoff=0)
view_menu.add_checkbutton(label='Vždy nahoře',command=setVzdyNahore,variable=vzdyNahore,onvalue = 1,offvalue = 0)
view_menu.add_command(label="Uložit aktuální text jako výchozí", command=saveDefaultText)
view_menu.add_separator()
view_menu.add_command(label="Výchozí nastavení", command=defaultSettings)
menubar.add_cascade(label='Nastavení', menu=view_menu)

# Rozbalovací menu O programu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_cascade(label="Co je nového", command=coJeNoveho)
helpmenu.add_cascade(label="Manuál", command=manual)
helpmenu.add_cascade(label="O programu", command=oProgramu, accelerator="F1")
menubar.add_cascade(label="Nápověda", menu=helpmenu)

listbox = Listbox(root, relief="sunken", selectmode=SINGLE, bg="LightSkyBlue1")
listbox.grid(row=0, column=0, rowspan=4, sticky=(N, W, S, E))
for key in obsah:
    listbox.insert(END, key)
listbox.select_set(0)
listbox.bind("<<ListboxSelect>>", ListboxSelect)

listbox_scrollbar = Scrollbar(root, orient=VERTICAL)
listbox_scrollbar.grid(row=0, column=1, rowspan=4, sticky=(N, S))

listbox.config(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.configure(command=listbox.yview)

textField = ScrolledText(root, borderwidth=2, relief="sunken", padx=5, pady=5, width=50, height=30)
textField.insert(END, defaultText)
textField.grid(row=0, column=2, rowspan=4, sticky=(N, W, S, E))
textField.bind("<KeyRelease>", keypressed)

labelFrame = Frame(root, bd=3, relief=GROOVE, bg="LightSkyBlue1")
labelFrame.grid(row=0, column=3, sticky=(N, W, S, E))

labelKeywords = Label(root, text="Klíčová slova:", fg="blue", font= "Helvetica 8", anchor=W)
labelKeywords.grid(row=1, column=3, sticky=(N, S, W, E), padx=(6), pady=(6,0))

labelKeywordsList = Label(root, text=keywordsLabel, font= "Helvetica 8 italic", anchor=W)
labelKeywordsList.grid(row=2, column=3, sticky=(N, S, W, E), padx=(6), pady=(6))

buttonNew = Button(root, command=new, text="Nový panel (Ctrl + N)", bg="LightSkyBlue1")
buttonNew.grid(row=3, column=3, sticky=(S, W, E), padx=(3), pady=(3))

root.config(menu=menubar)
root.columnconfigure(0, weight=0, minsize=25)
root.columnconfigure(1, weight=0, minsize=25)
root.columnconfigure(2, weight=2)
root.columnconfigure(3, weight=0, minsize=30)
root.rowconfigure(0, weight=1)

textField.focus_set() # Nastav po spuštění focus na textField

keypressed("a")

root.mainloop()


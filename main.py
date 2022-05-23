from tkinter import *
from tkinter import Tk, messagebox
import pickle

menus = {"ColdDrinks": {},
         "HotDrinks": {},
         "FastFood": {},
         "Desserts": {}}
inactiveItemsdict = {}
savefile = [menus,inactiveItemsdict]
isload = False
if isload is False:
    try:
        with open('save.mycafè', 'rb') as file:
            savefile = pickle.load(file)
            menus = savefile[0]
            inactiveItemsdict = savefile[1]
    except (OSError, IOError) as e:
        foo = 3
        pickle.dump(menus, open("save.mycafè", "wb"))
    isload = True


# functions FOR SIDE BUTtONS
def mainmenuhome(home, manage):
    for label in home.winfo_children():
        label.destroy()
    x = 0
    for i in menus:
        testo = StringVar(home)
        text = '\n'.join('{}\t£{}'.format(k, v) for k, v in menus[i].items())
        Label(home, text=i, relief="raise", font=("arial", 13), bd=5, width=38, anchor="n").place(x=x, anchor="nw")
        Label(home, textvariable=testo, relief="raise", font=("arial", 15), bd=6, width=31, height=20,
              anchor="n").place(x=x, y=100,
                                anchor="nw")
        x += 359
        testo.set(text)
    home.pack(fill=BOTH, expand=True)
    manage.forget()
    save()


def mainmenumanage(manage, home):
    manage.pack(fill=BOTH, expand=True)
    home.forget()
    save()


def save():
    try:
        text_file = open('save.mycafè', 'wb')
        pickle.dump([menus,inactiveItemsdict], text_file)
        text_file.close()
    except:
        print("ao")


def quit():
    root.destroy()


# basic tkinter initialization


root = Tk()
root.title('myCafè')
root.iconbitmap("images/cafe.ico")
root.geometry('1280x720')
root.state('zoomed')

# pictures
photo = PhotoImage(file="images/cafe.png")
homeimage = PhotoImage(file="images/home.png")
settingimage = PhotoImage(file="images/settings.png")
background = PhotoImage(file="images/background.png")
exiticonimage = PhotoImage(file="images/exiticon.png")
backgroundmainmenu = PhotoImage(file="images/backgroundmainmenu.png")
# background label
background_label = Label(root, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# root side label
side = Frame(root, width=250, height=1000, bd=12, relief="raise")
side.pack(side=RIGHT)
# mainmenu
mainmenu = Label(root, width=2500, height=1000, bd=5, relief="raise", image=backgroundmainmenu)

leftsidebutton = Button(side, image=homeimage, command=lambda: mainmenuhome(mainmenu, managemenu))
leftsidebutton.pack()
leftsidebutton2 = Button(side, image=settingimage, command=lambda: mainmenumanage(managemenu, mainmenu))
leftsidebutton2.pack()
leftsidebutton3 = Button(side, image=exiticonimage, command=lambda: quit())
leftsidebutton3.pack()

mainmenu.pack(side=TOP, fill="both", expand=1)
mainmenu.forget()


# managemenu functions


def buttondeleteinactive(listbox, index: int):
    delete = messagebox.askquestion("Delete Item",
                           "Are You Sure to delete the item?\n"
                           "it will be removed Permanently")
    if delete == "yes":

        item = listbox.get(index)
        key = item[0]
        del inactiveItemsdict[key]
        listbox.delete(index)


def restoreitem(listbox, index: int, menu, indexmenu: int, window):
    inactive_item = listbox.get(index)
    category_item = menu.get(indexmenu)
    key = inactive_item[0]
    new_nest = {key: inactive_item[1]}
    del inactiveItemsdict[key]
    listbox.delete(index)
    menus[category_item].update(new_nest)
    window.destroy()
    print(menus)
    save()


def createnewitem(nest, listbox, index: int, window):
    new_itemlistindex = listbox.get(index)
    menus[new_itemlistindex].update(nest)
    window.destroy()
    save()


def restoreitemswindow(listbox, index: int):
    temp_window = Toplevel(root)
    temp_window.title("Restore an item")
    temp_window.geometry("300x300")
    temp_window.resizable(False, False)
    Label(temp_window, text="Choose category").pack()
    temp_list = Listbox(temp_window, width=50, height=10)
    for key in sorted(menus):
        temp_list.insert(1, f"{key}")
    temp_list.pack()
    Button(temp_window, width=50, height=10, text="Restore",
           command=lambda: restoreitem(listbox, index, temp_list, ANCHOR, temp_window)).pack()


def createnewitemwindow(text, price):
    new_nest = {text: price}
    temp_window = Toplevel(root)
    temp_window.title("Create new Item")
    temp_window.geometry("300x300")
    temp_window.resizable(False, False)
    Label(temp_window, text="Choose category").pack()
    temp_list = Listbox(temp_window, width=50, height=10)
    for key in sorted(menus):
        temp_list.insert(1, f"{key}")
    temp_list.pack()
    Button(temp_window, width=50, height=10, text="Create",
           command=lambda: createnewitem(new_nest, temp_list, ANCHOR, temp_window)).pack()




def inactivateitem(itemtext, listbox):
    for i in menus:
        if itemtext in menus[i]:
            price = menus[i].get(itemtext)
            inactiveItemsdict.update({itemtext: price})
            listbox.delete(0, END)
            for key, value in sorted(inactiveItemsdict.items()):
                listbox.insert(1, [key, value])
            del menus[i][itemtext]
    save()


# Managemenu widget


managemenu = Frame(root, width=2500, height=1000, bd=12, relief="raise")
# label menu for widget
Label_frametop = Label(managemenu, width=151, height=20, bd=10, relief="raise")
Label_framebottom = Label(managemenu, width=151, height=20, bd=10, relief="raise")

# Entry texts
Entry_newitem = Entry(managemenu, width=25)
Entry_newprice = Entry(managemenu, width=25)
Entry_inactivateitem = Entry(managemenu, width=25)
# label menu for inactive items
Label_newitemtext = Label(Label_frametop, text="New Item")
Label_newitemtext.config(font=("arial", 30))

Label_newitemnametext = Label(Label_frametop, text="name:                                <= insert new name")
Label_newitemnametext.config(font=("arial", 15))

Label_newitempricetext = Label(Label_frametop, text="value:                                <= insert new value")
Label_newitempricetext.config(font=("arial", 15))

Label_moveitemtoinactivetext = Label(Label_framebottom, text="Inactivate item")
Label_moveitemtoinactivetext.config(font=("arial", 30))

Label_moveitemtoinactivenametext = Label(Label_framebottom,
                                         text="name:                                <= insert new name")
Label_moveitemtoinactivenametext.config(font=("arial", 15))

Label_inactiveItems = Label(managemenu, relief="raise", bd=7, width=50, height=100)
Label_inactiveItemsname = Label(Label_inactiveItems, text="Inactive Items", height=1)
Label_inactiveItemsBottomframe = Label(Label_inactiveItems, height=17)
# listbox for inactive items with scrollbar
Listbox_inactiveitems = Listbox(Label_inactiveItems, width=50, height=30)
scrollbar = Scrollbar(Label_inactiveItems)
scrollbar.config(command=Listbox_inactiveitems.yview)
Listbox_inactiveitems.config(yscrollcommand=scrollbar.set)
for k, v in sorted(inactiveItemsdict.items()):
    Listbox_inactiveitems.insert(1, [k, v])

# buttons
Button_deleteinactiveitem = Button(Label_inactiveItems, text="Delete Item",
                                   command=lambda: buttondeleteinactive(Listbox_inactiveitems, ANCHOR))
Button_Restoreinactiveitem = Button(Label_inactiveItems, text="Restore", width=10,
                                    command=lambda: restoreitemswindow(Listbox_inactiveitems, ANCHOR))
Button_newitem = Button(managemenu, text="submit", width=20, height=5,
                        command=lambda: createnewitemwindow(Entry_newitem.get(), Entry_newprice.get()))
Button_inactivateitem = Button(Label_framebottom, width=21, height=5, text="Submit",
                               command=lambda: inactivateitem(Entry_inactivateitem.get(), Listbox_inactiveitems))

# packings
managemenu.pack(side=TOP, fill="both", expand=1)
Label_newitemtext.place(x=0)
Label_newitemnametext.place(x=0, y=100)
Label_newitempricetext.place(x=0, y=150)
Label_moveitemtoinactivetext.place(x=0)
Label_moveitemtoinactivenametext.place(x=0, y=100)

Label_inactiveItems.pack(side=RIGHT, fill=BOTH)
Entry_newitem.place(x=100, y=115)
Entry_newprice.place(x=100, y=170)
Entry_inactivateitem.place(x=95, y=465)
Label_frametop.place(x=1)
Label_framebottom.place(x=1, y=350)
Label_inactiveItemsname.pack(side=TOP)
Listbox_inactiveitems.pack(side=LEFT, anchor="n")
Label_inactiveItemsBottomframe.pack(side=BOTTOM, fill=BOTH)
scrollbar.pack(side=RIGHT, fill=Y)
Button_deleteinactiveitem.place(x=10, y=520)
Button_Restoreinactiveitem.place(x=230, y=520)
Button_newitem.place(x=17, y=220)
Button_inactivateitem.place(x=0, y=212)
managemenu.forget()

# main infinite loop

root.mainloop()

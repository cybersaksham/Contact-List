from tkinter import *
import collections


class GUI(Tk):
    def __init__(self, title="Window", width=200, height=200, bg="white", resizableX=0, resizableY=0):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.config(bg=bg)
        self.resizable(resizableX, resizableY)

    def start(self):
        self.mainloop()


def checkInput(event):
    name = name_var.get()
    number = number_var.get()
    names = contact_list.get(0, END)
    if name == "" or number == "":
        save_btn.config(state=DISABLED)
    elif (name in names) and not isEditing:
        save_btn.config(state=DISABLED)
    else:
        try:
            num_int = int(number)
            save_btn.config(state=ACTIVE)
        except Exception as e:
            save_btn.config(state=DISABLED)


def pressAfter():
    global isView, isEditing
    if isView:
        name_entry.config(state=NORMAL)
        number_entry.config(state=NORMAL)
        save_btn.config(state=DISABLED, text="Save")
        isView = False
    if isEditing:
        dlt_btn.config(state=ACTIVE)
        edit_btn.config(state=ACTIVE)
        view_btn.config(state=ACTIVE)
        clear_btn.config(state=ACTIVE)
        contact_list.config(state=NORMAL)
        isEditing = False
    name_var.set("")
    number_var.set("")


def sortDict(item):
    return collections.OrderedDict(sorted(item.items()))


def setListByDict():
    contact_list.delete(0, END)
    items = sortDict(contacts)
    for i, j in items.items():
        contact_list.insert(END, i)


def setDictByFile():
    global contacts
    f = open("contacts.txt", 'r')
    items = f.readlines()
    contacts = {}
    for item in items:
        contact = item[:-1].split(":")
        name = ":".join([contact[i] for i in range(len(contact) - 1)])
        number = contact[len(contact) - 1]
        contacts[name] = number
    f.close()
    setListByDict()


def setFileByList():
    f = open("contacts.txt", "w")
    items = list(contact_list.get(0, END))
    items.sort()
    for item in items:
        f.write(f"{item}:{contacts[item]}\n")
    f.close()
    setDictByFile()


def saveContact():
    global isEditing
    if isEditing:
        for i in contact_list.curselection():
            contacts.pop(contact_list.get(i))
    if not isView:
        name = name_var.get()
        number = number_var.get()
        contacts[name] = number
        contact_list.insert(END, name)
    pressAfter()
    setListByDict()
    setFileByList()
    name_var.set("")
    number_var.set("")
    save_btn.config(state=DISABLED)


def deleteContact():
    pressAfter()
    for i in contact_list.curselection():
        contact_list.delete(i)
    setFileByList()


def dltShort(event):
    deleteContact()


def editContact():
    global isEditing
    for i in contact_list.curselection():
        pressAfter()
        name_var.set(contact_list.get(i))
        number_var.set(contacts[contact_list.get(i)])
        isEditing = True
        save_btn.config(state=ACTIVE, text="Save")
        dlt_btn.config(state=DISABLED)
        edit_btn.config(state=DISABLED)
        view_btn.config(state=DISABLED)
        clear_btn.config(state=DISABLED)
        contact_list.config(state=DISABLED)


def viewContact():
    global isView
    for i in contact_list.curselection():
        name_var.set(contact_list.get(i))
        number_var.set(contacts[contact_list.get(i)])
        name_entry.config(state=DISABLED)
        number_entry.config(state=DISABLED)
        save_btn.config(state=ACTIVE, text="New")
        isView = True


def viewShort(event):
    viewContact()


def clearContacts():
    pressAfter()
    contact_list.delete(0, END)
    setFileByList()


if __name__ == '__main__':
    # Variables
    BACKGROUND = "#53cfcf"
    contacts = {}
    isEditing = False
    isView = False

    # Making Window
    root = GUI(title="Contacts", width=350, height=340, bg=BACKGROUND)

    # Input Frame
    input_frame = Frame(root, bg=BACKGROUND)
    name_label = Label(input_frame, text="Name", bg=BACKGROUND, font="lucida 12 bold", width=7, anchor="e")
    number_label = Label(input_frame, text="Number", bg=BACKGROUND, font="lucida 12 bold", width=7, anchor="e")
    name_var = StringVar()
    number_var = StringVar()
    name_entry = Entry(input_frame, textvariable=name_var, font="lucida 12")
    number_entry = Entry(input_frame, textvariable=number_var, font="lucida 12")
    name_label.grid(row=0, column=0)
    number_label.grid(row=1, column=0)
    name_entry.grid(row=0, column=1, padx=15, pady=5)
    number_entry.grid(row=1, column=1, padx=15, pady=5)
    input_frame.pack(fill=X, pady=10, padx=10)

    # Main Frame
    main_frame = Frame(root, bg=BACKGROUND)
    main_frame.pack(fill=X, pady=10, padx=20)

    # Buttons Frame
    btn_frame = Frame(main_frame, bg=BACKGROUND)
    save_btn = Button(btn_frame, text="Save", command=saveContact, width=8, state=DISABLED)
    dlt_btn = Button(btn_frame, text="Delete", command=deleteContact, width=8)
    edit_btn = Button(btn_frame, text="Edit", command=editContact, width=8)
    view_btn = Button(btn_frame, text="View", command=viewContact, width=8)
    clear_btn = Button(btn_frame, text="Clear Log", command=clearContacts, width=8)
    save_btn.pack(pady=10)
    dlt_btn.pack(pady=10)
    edit_btn.pack(pady=10)
    view_btn.pack(pady=10)
    clear_btn.pack(pady=10)
    btn_frame.grid(row=0, column=0)

    # List Frame
    list_frame = Frame(main_frame, bg="white")
    scroll = Scrollbar(list_frame)
    scroll.pack(side=RIGHT, fill=Y)
    contact_list = Listbox(list_frame, yscrollcommand=scroll.set, height=11, width=15, font="lucida 12")
    contact_list.pack()
    setDictByFile()
    scroll.config(command=contact_list.yview)
    list_frame.grid(row=0, column=1, padx=70)

    # Events
    name_entry.bind("<KeyRelease>", checkInput)
    number_entry.bind("<KeyRelease>", checkInput)
    contact_list.bind("<Return>", viewShort)
    contact_list.bind("<Double-1>", viewShort)
    contact_list.bind("<Delete>", dltShort)

    # Starting Window
    root.start()

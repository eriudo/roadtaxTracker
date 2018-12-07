#!/usr/bin/env python3
from tkinter import (BooleanVar, Button, Checkbutton, Entry, Frame, Label,
                     Scrollbar, Tk, messagebox, LabelFrame, ttk)
from tkinter.constants import (NORMAL, W, E, N, S, END)

from controller import (add_new, delete_item, show_within, sort_show_vehicle,
                        update_checks)
from view_autocomplete import Combobox_Autocomplete
from view_multi_listbox import Multicolumn_Listbox

bg_colour = "DeepSkyBlue2"
btn_colour = "DeepSkyBlue3"

root = Tk()
root.title("RoadTax Renewal Tracker")
root.configure(background=bg_colour)
# root.resizable(width=False, height=False)


vehicle = ""
expiry = ""
informed = BooleanVar()
inspected = BooleanVar()
renewed = BooleanVar()


def on_select(data):
    # to impliment multiple selection
    global vehicle, expiry, new_vehicle_license, new_vehicle_expiry
    new_vehicle_expiry.delete(0, END)
    new_vehicle_expiry.insert(END, data[1])
    new_vehicle_license.set_value(data[0])
    vehicle = data[0]
    expiry = data[1]
    informed.set(data[2])
    inspected.set(data[3])
    renewed.set(data[4])

    return vehicle, informed, inspected, renewed


def show_info(msg):
    messagebox.showinfo("This is magical!", msg)


titleframe = Frame(root)
titleframe.configure(background=bg_colour)
titleframe.grid(row=0, column=0)

editframe = LabelFrame(root, text="Edit")
editframe.configure(background=bg_colour)
editframe.grid(row=2, column=0, padx=30,  pady=30)

roadtax_tab = ttk.Notebook(root)

bodyframe = Frame(roadtax_tab)
bodyframe.configure(background=bg_colour)
bodyframe.grid()

roadtax_tab.add(bodyframe, text="Roadtax")
roadtax_tab.enable_traversal()
roadtax_tab.grid(row=1, column=0, sticky=S)

title = Label(titleframe, font=("Courier", 28),
              text="Road-Tax Renewal Tracker", bg=bg_colour)

label = Label(bodyframe, text="day(s)", bg=bg_colour)

column_header = ["Vehicle Number", "Expiry Date",
                 "Informed", "Inspected", "Renewed"]

mc = Multicolumn_Listbox(bodyframe,
                         column_header,
                         command=on_select,
                         stripped_rows=("white", bg_colour),
                         select_mode="browse",
                         cell_anchor="center", height=20)

scrollbar = Scrollbar(bodyframe)
scrollbar.config(command=mc.interior.yview, activebackground=btn_colour)
scrollbar.grid(row=1, column=7, sticky=N+S)

mc.interior.config(yscrollcommand=scrollbar.set)
mc.interior.grid(row=1, column=0, columnspan=6, sticky=N+S+E+W)

entry = Entry(bodyframe)
entry.insert(0, "30")
entry.focus_set()

mc.table_data = show_within(entry.get())

chkbox1 = Checkbutton(bodyframe,
                      text="Informed",
                      variable=informed,
                      bg=bg_colour)
chkbox2 = Checkbutton(bodyframe,
                      text="Inspected",
                      variable=inspected,
                      bg=bg_colour)
chkbox3 = Checkbutton(bodyframe,
                      text="Renewed",
                      variable=renewed,
                      bg=bg_colour)


def callback():
    """
    update database with boolean values.
    currently partially managed by model.py
    """
    try:
        update = update_checks(
            vehicle, expiry, informed.get(), inspected.get(), renewed.get())
        if update is not None:
            show_info(update)
            mc.table_data = show_within(entry.get())
    except ValueError:
        show_info("Invalid input, Number only la!!!")
        update.config(state=NORMAL)
        pass


def refresh(event):
    """
    Dynamically update table as user type in the query
        :param event:
            KeyRelease event binded to Entry widget
    """
    mc.table_data = show_within(entry.get())


add_vehlabel = Label(editframe, text='Vehicle no.', bg=bg_colour)
sorted_list = list(sort_show_vehicle())
new_vehicle_license = Combobox_Autocomplete(editframe,
                                            list_of_items=sorted_list)
add_explabel = Label(editframe,
                     text='expiry date in (dd.mm.yyyy)', bg=bg_colour)
new_vehicle_expiry = Entry(editframe)


def delete_button_func():
    """
    delete item from database
    """
    result = delete_item(new_vehicle_license.get())
    if result is not None:
        show_info(result)


delete_button = Button(editframe,
                       command=delete_button_func,
                       text="delete",
                       background=btn_colour,
                       disabledforeground="DeepSkyBlue4")


def quit_edit():
    new_vehicle_license1 = add_new(
            new_vehicle_license.get(), new_vehicle_expiry.get())
    if new_vehicle_license1 is not None:
        show_info(new_vehicle_license1)


add_button = Button(editframe,
                    command=quit_edit,
                    text="Add / Edit",
                    background=btn_colour)
update = Button(bodyframe,
                text="Update!",
                background=btn_colour,
                command=callback)

entry.bind("<KeyRelease>", refresh)

title.grid(row=0, column=0, columnspan=6, padx=20, pady=20)

entry.grid(row=0, column=0, pady=10, padx=10, sticky=E)
label.grid(row=0, column=1, pady=10, padx=10, sticky=W)
chkbox1.grid(row=0, column=2, pady=10, padx=10, sticky=W+E)
chkbox2.grid(row=0, column=3, pady=10, padx=10, sticky=W+E)
chkbox3.grid(row=0, column=4, pady=10, padx=10, sticky=W+E)
update.grid(row=0, column=5, pady=10, padx=10)

add_vehlabel.grid(row=2, column=1, pady=5, padx=5)
new_vehicle_license.grid(row=2, column=2, pady=5, padx=5)
add_explabel.grid(row=2, column=3, pady=5, padx=5)
new_vehicle_expiry.grid(row=2, column=4, pady=5, padx=5)
delete_button.grid(row=2, column=5, pady=5, padx=5)
add_button.grid(row=2, column=6, pady=5, padx=5)

"""Configure window to launch in the middle of the screen"""
root.update_idletasks()
h = root.winfo_reqheight()  # width for the Tk root
w = root.winfo_reqwidth()  # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

print(w, h, ws, hs)

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.mainloop()

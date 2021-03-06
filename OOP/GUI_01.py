from tkinter import *
from backend import Database

database = Database("books.db")
 
def get_selected_row(event):
    global selected_tuple
    try :
        index=list1.curselection()[0]
    except IndexError:
        selected_tuple = ("","","","","")
    else:
        selected_tuple=list1.get(index)
        e1.delete(0,END)
        e1.insert(END,selected_tuple[1])
        e2.delete(0,END)
        e2.insert(END,selected_tuple[2])
        e3.delete(0,END)
        e3.insert(END,selected_tuple[3])
        e4.delete(0,END)
        e4.insert(END,selected_tuple[4])

def view_all():
    list1.delete(0,END)
    for row in database.view():
        list1.insert(END,row)

def search_entry():
    list1.delete(0,END)
    rows = database.search(title_text.get(),author_text.get(),year_text.get(),isbn_text.get())
    for row in rows:
        list1.insert(END,row)

def add_entry():
    database.insert(title_text.get(),author_text.get(),year_text.get(),isbn_text.get())
    list1.delete(0,END)
    list1.insert(END,(title_text.get(),author_text.get(),year_text.get(),isbn_text.get()))

def update_selected():
    database.update(selected_tuple[0],title_text.get(),author_text.get(),year_text.get(),isbn_text.get())
    view_all()

def delete_selected():
    database.delete(selected_tuple[0])
    view_all()

def close() :
    window.destroy()

if __name__=="__main__" :

    window = Tk()

    window.wm_title("BookStore")

    l1=Label(window,text="Title")
    l1.grid(row=0,column=0) 
    
    title_text=StringVar()
    e1=Entry(window,textvariable=title_text)
    e1.grid(row=0,column=1)

    l2=Label(window,text="Author")
    l2.grid(row=0,column=2) 
    
    author_text=StringVar()
    e2=Entry(window,textvariable=author_text)
    e2.grid(row=0,column=3)

    l3=Label(window,text="Year")
    l3.grid(row=1,column=0) 
    
    year_text=StringVar()
    e3=Entry(window,textvariable=year_text)
    e3.grid(row=1,column=1)

    l4=Label(window,text="ISBN")
    l4.grid(row=1,column=2) 
    
    isbn_text=StringVar()
    e4=Entry(window,textvariable=isbn_text)
    e4.grid(row=1,column=3)

    # CREATE LIST WITH SCROLLBAR
    list1=Listbox(window,height=6, width=35)
    list1.grid(row=2, column=0, rowspan=6, columnspan= 2)

    sb1=Scrollbar(window)
    sb1.grid(row=2, column=2, rowspan=6)
    
    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)

    list1.bind('<<ListboxSelect>>',get_selected_row)

    # CREATE BUTTON
    b1 = Button(window, text="View All", width=12, command = view_all)
    b1.grid(row=2, column= 3)
    b2 = Button(window, text="Search Entry", width=12, command = search_entry)
    b2.grid(row=3, column= 3)
    b3 = Button(window, text="Add Entry", width=12, command = add_entry)
    b3.grid(row=4, column= 3)
    b4 = Button(window, text="Update Selected", width=12, command = update_selected)
    b4.grid(row=5, column= 3)
    b5 = Button(window, text="Delete Selected", width=12, command = delete_selected)
    b5.grid(row=6, column= 3)
    b6 = Button(window, text="Close", width=12, command = close)
    b6.grid(row=7, column= 3)

    window.mainloop()

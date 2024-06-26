from tkinter import *
from tkinter import ttk
from functools import partial
import pandas as pd
import requests
from bs4 import BeautifulSoup
import webbrowser as wb

screen_X = 700
screen_Y = 400

root = Tk()
root.title("library manage ment system")
root.geometry(f"{screen_X}x{screen_Y}")

menu = Menu(root)
root.config(menu=menu)

# multiple frames //////////////////////////////////
search_page = Frame(root,height=screen_Y,width=screen_X)
table_page = Frame(root,height=screen_Y,width=screen_X)
index_page = Frame(root,height=screen_Y,width=screen_X)
link_page = Frame(root,height=screen_Y,width=screen_X)
search_page.pack()

# global functions //////////////////////////////////
def change_to_search_page():
    search_page.pack()
    table_page.pack_forget()
    index_page.pack_forget()
    link_page.pack_forget()
def change_to_tabel_page():
    search_page.pack_forget()
    table_page.pack()
    index_page.pack_forget()
    link_page.pack_forget()
def change_to_index_page():
    index_page.pack()
    table_page.pack_forget()
    search_page.pack_forget()
    link_page.pack_forget()
def change_to_link_page():
    link_page.pack()
    table_page.pack_forget()
    index_page.pack_forget()
    search_page.pack_forget()

def searcher(search,list_):
    ret=[]
    for index,i in enumerate(list_):
        for aa,j in enumerate(i):
            try:
                if search.upper() == i[aa:aa+len(search)].upper():
                    ret.append((index,list_[index]))
                    break
            except:
                f""
    return ret

# search screen //////////////////////////////////////////
    

def Search(entry):
    df = pd.read_csv('movie.csv')
    sear = entry.get()
    movie_names = df['movie_name']
    print(sear)

    return searcher(sear,movie_names)

def mk_list(list_):
    change_to_tabel_page()
    data = Search(list_)
    print(data[0][0],data[0][1])

    columns = ('movie_code', 'title')

    tree = ttk.Treeview(table_page, columns=columns, show='headings')
        # Define headings
    tree.heading('movie_code', text='Movie Code')
    tree.heading('title', text='Title')
    
    tree.column('movie_code', width=100)
    tree.column('title', width=600)
    
    for row in data:
        tree.insert('', END, values=row)

    tree.pack(fill='both', expand=True)
    
def mk_link(code):
    global ros
    change_to_index_page()
    df = pd.read_csv('movie.csv')
    link = df["URL"].loc[int(code.get())]

    req = requests.get(link)
    soup = BeautifulSoup(req.content, 'html.parser')

    ros=[]
    for index , i in enumerate(soup.find_all("div","touch")):
        ros.append([index,i.a.string,i.span.string,i.a["href"]])

    columns = ('sno', 'title','size')
    tree = ttk.Treeview(index_page, columns=columns, show='headings')

        # Define headings
    tree.heading('sno', text='S.No')
    tree.heading('title', text='Title')
    tree.heading('size', text='SIZE(MB)')
    
    tree.column('sno', width=100)
    tree.column('title', width=500)
    tree.column('size', width=100)

    for row in ros:
        tree.insert('', END, values=(row[0],row[1],row[2]))

    tree.pack(fill='both', expand=True)


def links(index):
    change_to_link_page()
    z = requests.get(ros[int(index.get())][3])
    soup = BeautifulSoup(z.content, 'html.parser')
    filtered_links = []
    for index,i in enumerate(soup.find_all("a","newdl")):
        filtered_links.append(f"https://www.filmyzilla.vg{i['href']}")
    
    for i,links in enumerate(filtered_links):
        link_info = partial(wb.open,links)
        link_btn = Button(link_page,text=f"{i}:server",command=link_info)
        link_btn.pack()



search_lb = Label(search_page,text="SEARCH")
search_lb.place(x=300,y=200,height=15,width=100)
search_en = Entry(search_page)
search_en.place(x=250,y=220,height=25,width=200)
search_info  = partial(mk_list,search_en)
search_btn = Button(search_page,text="search",command=search_info)
search_btn.place(x=300,y=250,height=25,width=100)

#  tabel screen 
code_lb = Label(table_page,text="enter movie code")
code_lb.pack()
code_en = Entry(table_page)
code_en.pack()
code_info  = partial(mk_link,code_en)
code_btn = Button(table_page,text="continue",command=code_info)
code_btn.pack()

#  index screen 
index_lb = Label(index_page,text="enter S.No")
index_lb.pack()
index_en = Entry(index_page)
index_en.pack()
index_info  = partial(links,index_en)
index_btn = Button(index_page,text="continue",command=index_info)
index_btn.pack()


root.mainloop()
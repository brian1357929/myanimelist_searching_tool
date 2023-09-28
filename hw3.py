import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter.constants import *
import webbrowser
import csv
import psycopg2


def onOK():

    def link(event):
        for item in tree.selection():
            item_url=tree.item(item,'values')
            f_ctrler = webbrowser.get('chrome')
            print(item_url)
            f_ctrler.open(rows[tree.index(item)][10])


    sql='select a."animeID",a."name",a."season",a."year",a."type",a."episodes",a."source",a."scored",a."scoredBy",a."members",a."url"'
    if entry2.get() != '':
        sql=sql+',s."studios"'
    if genre.get() != '____':
        sql=sql+',g."genre"'

    sql=sql+'from anime as a'
    if entry2.get() != '':
        sql=sql+',studios as s'
    if genre.get() != '____':
        sql=sql+',genre as g'

    sql=sql+' where a."animeID"=a."animeID"'
    if entry2.get() != '':
        sql=sql+' and a."animeID"=s."animeID"'
    if genre.get() != '____':
        sql=sql+' and a."animeID"=g."animeID"'

    if entry.get() != '':
        sql=sql+' and a."name" ilike \'%'+entry.get()+'%\''
    if season.get() != '____':
        sql=sql+' and (a."season"=\''+season.get()+'\''
        if(season.get() =='spring'):
            sql=sql+' or "season"=\'Spring\')'
        if(season.get() =='summer'):
            sql=sql+' or "season"=\'Summer\')'
        if(season.get() =='fall'):
            sql=sql+' or "season"=\'Fall\')'
        if(season.get() =='winter'):
            sql=sql+' or "season"=\'Winter\')'
    if year.get() != '____':
        if(year.get() == 'before 2020'):
            sql=sql+' and a."year"<2000'
        else:
            sql=sql+' and a."year"='+year.get()
    if type.get() != '____':
        sql=sql+' and a."type"=\''+type.get()+'\''
    if source.get() != '____':
        sql=sql+' and a."source"=\''+source.get()+'\''
    if genre.get() != '____':
        sql=sql+' and g."genre"=\''+genre.get()+'\''
    if entry2.get() != '':
        sql=sql+' and s."studios" ilike \'%'+entry2.get()+'%\''
    if order.get()=='time':
        sql=sql+' order by a."year" DESC NULLS LAST'
    else:
        sql=sql+' order by a."scored" DESC NULLS LAST'
    #sql='select * from project.Databases.postgres.Schemas.public.Tables.anime;'
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchmany(100)

    root = tk.Toplevel()
    root.title('search_result')
    root.configure(bg="#7AFEC6")
    root.geometry('960x500')

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

    root.rowconfigure(1,weight=1)
    root.columnconfigure(1,weight=1)
    root.columnconfigure(3,weight=1)

    s=ttk.Style()
    s.theme_use('clam')
    s.configure('Treeview', rowheight=40)




    tree=ttk.Treeview(root,columns=('animeID', 'name', 'season', 'year', 'type', 'episodes'
    , 'source', 'scored', 'scoredBy', 'members'),show='headings',displaycolumns="#all",yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)
    tree.heading('animeID',text='animeID')
    tree.heading('name',text='name')
    tree.heading('season',text='season')
    tree.heading('year',text='year')
    tree.heading('type',text='type')
    tree.heading('episodes',text='episodes')
    tree.heading('source',text='source')
    tree.heading('scored',text='scored')
    tree.heading('scoredBy',text='scoredBy')
    tree.heading('members',text='members')

    tree.column('animeID',width=56)
    tree.column('season',width=56)
    tree.column('year',width=64)
    tree.column('type',width=64)
    tree.column('episodes',width=60)
    tree.column('source',width=80)
    tree.column('scored',width=80)
    tree.column('scoredBy',width=80)
    tree.column('members',width=100)
    tree.column('name',width=250)

    tree.bind("<Double-Button-1>", link)


    for row in rows:
        tree.insert("",index="end",values=tuple([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]))


    tree.pack(ipadx=20,ipady=20,padx=10,pady=6)





#user and password are blank
conn = psycopg2.connect(database="postgres", user="************", password="**********", host="project.ci77zueykeyy.us-east-1.rds.amazonaws.com", port="5432")

cursor = conn.cursor()

chrome_path='C:\\Program Files (x86)\\Google/Chrome\\Application\\chrome.exe'
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))

window = tk.Tk()
window.title('MAL search')
window.resizable(False, False)
window.geometry("640x660+10+10")


s=ttk.Style()
s.theme_use('clam')
##################################################################################################
img =tk.PhotoImage(file='logo.png')

label = tk.Label(image=img)
'''label = tk.Label(window,                 # 文字標示所在視窗
                 text = 'Hello, world',  # 顯示文字
                 bg = '#EEBB00',         #  背景顏色
                 font = ('Arial', 16),   # 字型與大小
                 width = 15, height = 2) # 文字標示尺寸'''
##################################################################################################
# 以預設方式排版標示文字
label.pack(side="top")
##################################################################################################
label = tk.Label(window,
                 text = 'name_search',
                 font = ('Arial', 12),
                 )
label.place(x=10 ,y=100,anchor=NW)


entry = tk.Entry(window,
                 width = 32,font = ('Arial', 16))
entry.place(x=115 ,y=100,anchor=NW)

##################################################################################################

label = tk.Label(window,
                 text = 'season',
                 font = ('Arial', 12),
                 )
label.place(x=10 ,y=400,anchor=NW)


comboboxList =["____", "spring", "summer","fall","winter"]
season = ttk.Combobox(window, state='readonly')
season['values'] = comboboxList
season.config(width=16, font=('Helvetica', 12))
season.place(x=115 ,y=400,anchor=NW)
season.current(0)
'''
olist1 = ("__", "spring", "summer","fall","winter")
season = tk.StringVar()
season.set("__")
omenu1 = tk.OptionMenu(window, season, *olist1)
omenu1.config(width=8, font=('Helvetica', 12))
omenu1.place(x=115 ,y=400,anchor=NW)'''
##################################################################################################


label = tk.Label(window,text = 'year',font = ('Arial', 12),)
label.place(x=10 ,y=220,anchor=NW)

olist = ["____", "2023", "2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012"
,"2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","before 2020"]
year = ttk.Combobox(window, state='readonly')
year['values'] = olist
year.config(width=16, font=('Helvetica', 12))
year.place(x=115 ,y=220,anchor=NW)
year.current(0)

##################################################################################################

label = tk.Label(window,text = 'type',font = ('Arial', 12),)
label.place(x=10 ,y=280,anchor=NW)

olist = ["____", "Movie", "Music","ONA","OVA","Special","TV","Unknown"]
type = ttk.Combobox(window, state='readonly')
type['values'] = olist
type.config(width=16, font=('Helvetica', 12))
type.place(x=115 ,y=280,anchor=NW)
type.current(0)


##################################################################################################

label = tk.Label(window,text = 'source',font = ('Arial', 12),)
label.place(x=10 ,y=340,anchor=NW)

olist = ["____", "4-koma manga", "Book","Card game","Game","Light novel","Manga","Mixed media","Music"
,"Novel","Original","Other","Picture book","Radio","Unknown","Visual novel","Web manga","Web novel"]
source = ttk.Combobox(window, state='readonly')
source['values'] = olist
source.config(width=16, font=('Helvetica', 12))
source.place(x=115 ,y=340,anchor=NW)
source.current(0)


##################################################################################################
label = tk.Label(window,text = 'studios',font = ('Arial', 12),)
label.place(x=10 ,y=160,anchor=NW)


entry2 = tk.Entry(window,
                 width = 32,font = ('Arial', 16))
entry2.place(x=115 ,y=160,anchor=NW)

##################################################################################################

label = tk.Label(window,text = 'genre',font = ('Arial', 12),)
label.place(x=10 ,y=460,anchor=NW)

olist = ["____", "Action", "Adventure","Avant Garde","Award Winning","Boys Love","Comedy","Ecchi","Erotica"
,"Fantasy","Girls Love","Gourmet","Hentai","Horror","Mystery","Romance","Sci-Fi","Slice of Life"
,"Sports","Supernatural","Suspense"]
genre = ttk.Combobox(window, state='readonly')
genre['values'] = olist
genre.config(width=16, font=('Helvetica', 12))
genre.place(x=115 ,y=460,anchor=NW)
genre.current(0)


##################################################################################################
label = tk.Label(window,text = 'sort by',font = ('Arial', 12),)
label.place(x=10 ,y=560,anchor=NW)

frame = ttk.Frame(window)
frame.place(x=100,y=560,width=480,height = 30)

order = tk.StringVar()

radio_buttons = ttk.Radiobutton(frame,text='time',variable=order,value='time')
radio_buttons.pack(expand=True, fill='both',side=LEFT)

radio_buttons = ttk.Radiobutton(frame,text='scored',variable=order,value='scored')
radio_buttons.pack(expand=True, fill='both',side=LEFT)
order.set('time')
##################################################################################################




button = tk.Button(window, text = "OK", command = onOK,width = 10)
button.place(x=300,y=650,anchor=S)



window.mainloop()
cursor.close()
conn.close()

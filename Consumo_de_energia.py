from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector

# Consumo mensal de energia
# Feito por Jonas Santana

class Janela(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x800')
        self.title('CONSUMO MENSAL DE ENERGIA')

        self.entry_ident = Entry(self)
        self.entry_nome = Entry(self)
        self.entry_pot = Entry(self)
        self.entry_horas = Entry(self)
        self.entry_dias = Entry(self)

        ident= Label(self,text='ID',font='verdana 15').place(x=100,y=30)
        self.entry_ident.place(x=320,y=30)

        nome = Label(self,text = 'Nome',font='verdana 15')
        nome.place(x=100,y=80)
        self.entry_nome.place(x=320,y=80)

        pot = Label(self,text = 'Potência',font='verdana 15')
        pot.place(x=100,y=130)
        self.entry_pot.place(x=320,y=130)

        horas = Label(self,text = 'Quant. de horas/dia',font='verdana 15')
        horas.place(x=100,y=180)
        self.entry_horas.place(x=320,y=180)

        dias = Label(self,text = 'Quant. de dias',font='verdana 15')
        dias.place(x=100,y=230)
        
        self.entry_dias.place(x=320,y=230)

        cad = Button(self,text = 'Cadastrar',command = self.cadastro,height=3,width=10).place(x=100,y=280)
        atualiz = Button(self,text='Atualizar',command=self.atualizar,height=3,width=10).place(x=200,y=280)
        delet = Button(self,text='Deletar',command=self.excluir,height=3,width=10).place(x=300,y=280)

        colun = ('id', 'Nome', 'Potência (W)', 'Horas/dia', 'Dias', 'Consumo (kWh)')
        self.tab = ttk.Treeview(self,columns=colun,show='headings')

        self.tab.column('id',width=50,anchor='center')
        self.tab.column('Nome',width=120,anchor='center')
        self.tab.column('Potência (W)',width=100,anchor='center')
        self.tab.column('Horas/dia',width=100,anchor='center')
        self.tab.column('Dias',width=50,anchor='center')
        self.tab.column('Consumo (kWh)',width=100,anchor='center')
        for col in colun:
            self.tab.heading(col,text=col)
            self.tab.grid(row=1,column=0, columnspan=2)
            self.tab.place(x=10, y=350)

        self.consulta()
        self.tab.bind('<Double-Button-1>',self.getvalues)

    def getvalues(self,event):
        self.entry_ident.delete(0,END)
        self.entry_nome.delete(0,END)
        self.entry_pot.delete(0,END)
        self.entry_horas.delete(0,END)
        self.entry_dias.delete(0,END)

        row_id = self.tab.selection()[0]    
        select = self.tab.set(row_id)
        self.entry_ident.insert(0,select['id'])
        self.entry_nome.insert(0,select['Nome'])
        self.entry_pot.insert(0,select['Potência (W)'])
        self.entry_horas.insert(0,select['Horas/dia'])
        self.entry_dias.insert(0,select['Dias'])

    def cadastro(self):
        self.val = 0.64837
        self.id = self.entry_ident.get()
        self.name = self.entry_nome.get()
        self.p = self.entry_pot.get()
        self.h = self.entry_horas.get()
        self.d = self.entry_dias.get()
        self.c = (float(self.p) * float(self.h) * float(self.d))/1000

        if(self.id == '' or self.name == '' or self.p == '' or self.h == '' or self.d == ''):
            messagebox.showinfo('ALERTA','Por favor preencha todos os campos')
        else:     
            conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="crud")
            cursor = conexao.cursor()
            self.tab.insert('','end',values=(self.id,self.name,self.p,self.h,self.d, self.c))
            comando = "INSERT INTO dados (id, nome, potencia, horas, dias, consumo) VALUES (%s,%s, %s, %s, %s, %s)"
            valores = (self.id,self.name,self.p,self.h,self.d, self.c)
            cursor.execute(comando,valores)
            conexao.commit()
            messagebox.showinfo("Status", "Cadastrado com Sucesso!")

            self.entry_ident.delete(0,END)
            self.entry_nome.delete(0,END)
            self.entry_pot.delete(0,END)
            self.entry_horas.delete(0,END)
            self.entry_dias.delete(0,END)
            cursor.close()
            conexao.close()      

    def consulta(self):
        conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="crud")
        cursor = conexao.cursor()
        comando = "SELECT id, nome, potencia, horas, dias, consumo FROM dados"
        cursor.execute(comando)
        result = cursor.fetchall()

        for i, (id,nome,w,time,day,cons) in enumerate(result,start=1):
            self.tab.insert('','end',values=(id,nome,w,time,day,cons))
            cursor.close()
            conexao.close()    

    def atualizar(self):
        self.id = self.entry_ident.get()
        self.name = self.entry_nome.get()
        self.p = self.entry_pot.get()
        self.h = self.entry_horas.get()
        self.d = self.entry_dias.get()
        self.c = (float(self.p) * float(self.h) * float(self.d))/1000

        if(self.name == '' or self.p == '' or self.h == '' or self.d == ''):
            messagebox.showinfo('ALERTA','Por favor preencha todos os campos')
        else:
            conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="crud")
            cursor = conexao.cursor()
            select = self.tab.focus()
            self.tab.item(select,values=(self.id,self.name,self.p,self.h,self.d,self.c))
            comando = "Update dados set nome= %s, potencia= %s, horas= %s, dias= %s, consumo= %s where id= %s"
            valores = (self.name,self.p,self.h,self.d,self.c,self.id)
            cursor.execute(comando,valores)
            conexao.commit()
            messagebox.showinfo("Status", "Atualizado com Sucesso")

            self.entry_ident.delete(0,END)
            self.entry_nome.delete(0,END)
            self.entry_pot.delete(0,END)
            self.entry_horas.delete(0,END)
            self.entry_dias.delete(0,END)
            cursor.close()
            conexao.close()    

    def excluir(self):
        self.id = self.entry_ident.get()
    
        try:
            conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="crud")
            cursor = conexao.cursor()
            child_id = self.tab.selection()[0]
            self.tab.delete(child_id)
            comando = "delete from dados where id = %s"
            valores = (self.id,)
            cursor.execute(comando,valores)
            conexao.commit()
            messagebox.showinfo('Status','Deletado com Sucesso')

            self.entry_ident.delete(0,END)
            self.entry_nome.delete(0,END)
            self.entry_pot.delete(0,END)
            self.entry_horas.delete(0,END)
            self.entry_dias.delete(0,END)
            cursor.close()
            conexao.close()    
        
        except IndexError:
            messagebox.showinfo('ALERTA', 'Por favor selecione uma linha')
    
janela = Janela()
janela.mainloop()

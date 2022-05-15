from tkinter import*
import requests
import bs4
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import numpy as np
  

def f1():
	addemp.deiconify()
	mainwind.withdraw()

def f2():
	mainwind.deiconify()
	addemp.withdraw()

def f3():
	viewemp.deiconify()
	mainwind.withdraw()
	viewdata.delete(1.0,END)
	info =""
	con = None
	try:
		con = connect("intern.db")
		cursor = con.cursor()
		sql = "select * from employe"
		cursor.execute(sql)
		data= cursor.fetchall()
		for d in data:
			info = info + "id : " +str(d[0]) + "  name : "+str(d[1])+   "  salary : "+str(d[2]) + "\n"
		viewdata.insert(INSERT,info)
	except Exception as e:
		showerror("issue ",e)
	finally:
		if con is not None:
			con.close()

def f4():
	mainwind.deiconify()
	viewemp.withdraw()
	
def f5():
	updateemp.deiconify()
	mainwind.withdraw()
def f6():
	mainwind.deiconify()
	updateemp.withdraw()
def f7():
	deleteemp.deiconify()
	mainwind.withdraw()
def f8():
	mainwind.deiconify()
	deleteemp.withdraw()
	


try:
	
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res= requests.get(wa)
	data = bs4.BeautifulSoup(res.text ,"html.parser")
	info = data.find("img", {"class" :"p-qotd"})
	text2 = info["alt"]
	
	

except Exception as e:
	print("issue ",e)

def save():
	try:

		con = None
		id = int(id_entry.get())
		name =name_entry.get()
		salary = int(salary_entry.get())
		n1=name.isalpha()
	
		con = connect("intern.db")
		cursor = con.cursor()
		
		if len(name)==0:
			showerror("Name","Name shldnt be empty")
		
		elif len(name)<2:
			showerror("Name ","name should contain at least two alphabets")
			con.rollback()
			
		elif len(name) >2:
			showerror("Name ","name should contain only two alphabets")
			con.rollback()

		elif n1==False:
			showerror("Name","name should contain only alpha ")
			con.rollback()
		
		elif id < 0:
			showerror("ID ","ID should be positive")
			con.rollback()

		elif id == 0:
			showerror("ID","ID shldnt be  0")
			con.rollback()

		elif cursor.rowcount == 1:
				con.commit()
				showerror("Record","id already exists")
		
		elif salary <8000 :
			showerror("Salary ","min salary should be 8k")
			con.rollback()
				
			
		else:
			sql = "insert into employe values ('%d' , '%s','%d' )"
			cursor.execute(sql %(id,name,salary))
			con.commit ()
			showinfo("success ", "Record Added")
	except ValueError:
		showerror("Empty Input ","Enter valid id,salary ,name ")
	
	except IntegrityError:
		showerror("Record","Record already exists")	

	except Exception as e:
		print("Issue ",e)
	finally:
		if con is not None:
			con.close()	

def update():
	try:
		con = None
		id = int(id_update.get())
		name = name_update.get()
		salary = int(salary_update.get())
		n2=name.isalpha()

		con = connect("intern.db")
		cursor = con.cursor()
		
		if len(name)==0:
			showerror("Name","Name shldnt be empty")
		elif len(name) >2:
			showerror("Name ","name should contain only two alphabets")
			con.rollback()

		elif len(name) <2:
			showerror("Name ","name should contain at least two alphabets")
			con.rollback()
			
		
		elif n2==False:
			showerror("Name","name should contain only alpha ")
			con.rollback()
		
		elif id < 0:
			showerror("ID ","Int shld be positive")
			con.rollback()

		elif id == 0:
			showerror("ID","ID shldnt be 0")
			con.rollback()

		
		elif salary <8000 :
			showerror("Salary ","min salary should be 8k")
			con.rollback()
		else:
			sql = "update employe set name ='%s'  where  id ='%d'"
			sql2= "update employe set salary ='%d'  where  id ='%d'"
			cursor.execute(sql % (name,id))
			cursor.execute(sql2 % (salary,id))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("success","record updated")

			else:
				showerror("ID" ," does not exists ")
	except ValueError:
		showerror("Empty Input ","Enter valid id,salary ,name ")
		
	
	except Exception as e:
		showerror("Issue ",e)
	
	finally:
		if con is not None:
			con.close()
			

def delete():
	try:	
		con = None
		id = int(iddelete_entry.get())
		con = connect("intern.db")
		cursor =con.cursor()
		sql="delete from employe where id = '%d'"
		cursor.execute(sql %(id) )
		if cursor.rowcount ==1:
			con.commit()
			showinfo("sucess","ID deleted ")
		else:
			showerror("Invalid ID ","doesnt exists ")
	except ValueError:
		showerror("Invalid","Enter int only")
	
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
			
def chart():
	info =""
	name=[]
	salary=[]
	con = None
	try:
		con = connect("intern.db")
		cursor = con.cursor()
		sql = "select * from employe order by -salary limit 5"
		cursor.execute(sql)
		data= cursor.fetchall()
		
		for d in data:
			name.append(str(d[1]))
			salary.append(str(d[2]))

		#print(name)
		#print(salary)
		
		for i in range(0,len(salary)):
			salary[i]=int(salary[i])
		#print(salary)

		en=name
		sl=salary
		
		x=np.arange(len(name))
		plt.bar(x,salary,color=["#AC92EB","#4FC1E8","#A0D568","#FFCE54","#ED5564"],width=0.3)
		plt.xlabel("Employe")
		plt.ylabel("Salary")
		plt.title("Top five highest Earning Employe ")
		plt.xticks(x,name)
		
		plt.show()


	except Exception as e:
		showerror("issue ",e)
	finally:
		if con is not None:
			con.close()



mainwind= Tk()
mainwind.geometry("800x500+100+100")
mainwind.configure(bg="#F4EDED")
mainwind.title("E.M.S")


f = ("Arial",20,"bold")
qt=("Arial",10,"bold")
qlabel=Label(mainwind,text = "QOTD:",font=f,fg="black",bg="#F4EDED")
qtlabel=Label(mainwind,text = text2,font=qt,fg="black",bg="#F4EDED")
qlabel.place(x=10,y=395)
qtlabel.place(x=10,y=425)

btnadd =Button(mainwind,text = "Add",font = f,bd=2,bg="#344955",fg="#FCFBFC",command=f1)
btnadd.pack(pady=20)

btnview =Button(mainwind,text = "View",font = f,bd=2,bg="#344955",fg="#FCFBFC",command=f3)
btnview.pack(pady=10)

btnupdate =Button(mainwind,text = "Update",font = f,bd=2,bg="#344955",fg="#FCFBFC",command=f5)
btnupdate.pack(pady=10)

btndelete =Button(mainwind,text = "Delete",font = f,bd=2,bg="#344955",fg="#FCFBFC",command=f7)
btndelete.pack(pady=10)

btnchart =Button(mainwind,text = "Chart",font = f,bd=2,bg="#344955",fg="#FCFBFC",command=chart)
btnchart.pack(pady=10)

#Add emp window

addemp = Toplevel(mainwind)
addemp.title("Add Emp .")
addemp.geometry("500x500+100+100")
addemp.configure(bg="#BC544B")
addemp.withdraw()

id_label = Label(addemp,text="Enter id",font = f,bd=2,bg="#BC544B",fg="#FCFBFC")
id_entry=Entry(addemp,font=f,bd=2)
id_label.pack(pady=10)
id_entry.pack(pady=10)
name_label=Label(addemp,text="Enter name",font=f,bd=2,bg="#BC544B",fg="#FCFBFC")
name_entry=Entry(addemp,font=f,bd=2)
name_label.pack(pady=10)
name_entry.pack(pady=10)
salary_lab=Label(addemp,text="Enter Salary",font=f,bd=2,bg="#BC544B",fg="#FCFBFC")
salary_entry=Entry(addemp,font=f,bd=2)
salary_lab.pack(pady=10)
salary_entry.pack(pady=10)
savebtn=Button(addemp,text="Save",font=f,bd=2,command=save,bg="#900D09",fg="#FCFBFC")
backbtn=Button(addemp,text="Back",font=f,bd=2,command=f2,bg="#900D09",fg="#FCFBFC")
savebtn.pack(pady=10)
backbtn.pack(pady=10)

#View window

viewemp = Toplevel(mainwind)
viewemp.title("View Emp ")
viewemp.geometry("500x500+100+100")
viewemp.configure(bg="#4B4BC3")
viewemp.withdraw()

g = ("NewsGoth BT",14,)
viewdata = ScrolledText(viewemp,width =40,height=17,font = g,bg="beige")
viewback = Button(viewemp,text = "Back",font=f,command=f4)
viewdata.pack(pady=10)
viewback.pack(pady=10)

#Update Emp window

updateemp = Toplevel(mainwind)
updateemp.title("Update Emp .")
updateemp.geometry("500x500+100+100")
updateemp.configure(bg="#266E73")
updateemp.withdraw()

idlabel = Label(updateemp,text="Enter id",font = f,bg="#266E73",fg="#FCFBFC")
id_update=Entry(updateemp,font=f,bd=2)
idlabel.pack(pady=10)
id_update.pack(pady=10)
namelabel=Label(updateemp,text="Enter name",font=f,bg="#266E73",fg="#FCFBFC")
name_update=Entry(updateemp,font=f,bd=2)
namelabel.pack(pady=10)
name_update.pack(pady=10)
salarylab=Label(updateemp,text="Enter Salary",font=f,bg="#266E73",fg="#FCFBFC")
salary_update=Entry(updateemp,font=f,bd=2)
salarylab.pack(pady=10)
salary_update.pack(pady=10)
savebtn=Button(updateemp,text="Save",font=f,bd=2,command=update,bg="#344955",fg="#FCFBFC")
backbtn=Button(updateemp,text="Back",font=f,bd=2,command=f6,bg="#344955",fg="#FCFBFC")
savebtn.pack(pady=10)
backbtn.pack(pady=10)

#Delete Emp wind

deleteemp=Toplevel(mainwind)
deleteemp.title("Delete Emp ")
deleteemp.geometry("500x500+100+100")
deleteemp.configure(bg="#2c542d")
deleteemp.withdraw()

idlabel = Label(deleteemp,text="Enter id",font = f,bg="#2c542d",fg="#2F2D2E")
iddelete_entry=Entry(deleteemp,font=f,bd=2)
idlabel.pack(pady=10)
iddelete_entry.pack(pady=10)
savebtn=Button(deleteemp,text="Save",font=f,bd=2,command=delete,bg="#C6ECCF",fg="#2F2D2E")
backbtn=Button(deleteemp,text="Back",font=f,bd=2,command=f8,bg="#C6ECCF",fg="#2F2D2E")
savebtn.pack(pady=10)
backbtn.pack(pady=10)






mainwind.mainloop()
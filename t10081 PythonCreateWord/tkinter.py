

#
from tkinter import *

top=Tk()

check_EDU = IntVar()
check_DHF = IntVar()
check_IRF = IntVar()
check_PNF = IntVar()
check_SHF = IntVar()

label = Label(top, text = "hello tkinter")
button = Button(top ,text="first button")

check_DHF = Checkbutton(top,text="DHF", variable = check_DHF, onvalue =1, offvalue =0)
check_EDU = Checkbutton(top,text="EDU", variable = check_EDU, onvalue =1, offvalue =0)
check_IRF = Checkbutton(top,text="IRF", variable = check_IRF, onvalue =1, offvalue =0)
check_PNF = Checkbutton(top,text="PNF", variable = check_PNF, onvalue =1, offvalue =0)
check_SHF = Checkbutton(top,text="SHF", variable = check_SHF, onvalue =1, offvalue =0)

font = ("yahei", 10, "bold")
# text = Text(top,height=5, width=30, font=font, bg="white", fg="black")
# text.insert(INSERT,"Hello GUI,")
# text.insert(END, "Bye!")

# label.pack()
# button.pack()
check_DHF.pack()
check_SHF.pack()
check_IRF.pack()
check_PNF.pack()
check_EDU.pack()

top.mainloop()


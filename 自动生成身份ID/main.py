def autoID():
    import random
    ar = [0 for i in range(18)]
    ar[0] = random.randint(1,6)
    if ar[0] == 1:
        ar[1] = random.randint(1,5)
    elif ar[0] == 2:
        ar[1] = random.randint(1,3)
    elif ar[0] == 3:
        ar[1] = random.randint(1,7)
    elif ar[0] == 4:
        ar[1] = random.randint(1,6)
    elif ar[0] == 5:
        ar[1] = random.randint(1,4)
    elif ar[0] == 6:
        ar[1] = random.randint(1,5)
    elif ar[0] == 7:
        ar[1] = 1
    elif ar[0] == 8:
        ar[1] = random.randint(1,2)
    ar[2] = random.randint(0,4)
    ar[3] = random.randint(0,9)
    ar[4] = random.randint(0,5)
    ar[5] = random.randint(0,9)
    #年
    ar[6] = random.randint(1,2)
    if ar[6] == 1:
        ar[7] = 9
        ar[8] = random.randint(6,9)
    else:
        ar[7] = 0
        ar[8] = random.randint(0,4)
    ar[9] = random.randint(0, 9)
    #月份
    ar[10] = random.randint(0,1)
    if ar[10] == 0:
        ar[11] = random.randint(1,9)
    else:
        ar[11] = random.randint(1,2)
    #日期
    ar[12] = random.randint(0,2)
    ar[13] = random.randint(0,9)
    #顺序码
    ar[14] = random.randint(0, 9)
    ar[15] = random.randint(0, 9)
    ar[16] = random.randint(0, 9)
    s1 = 0
    list1 = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    for i in range(17):
        s1 = s1 + ar[i] * list1[i]
    s2 = s1 % 11
    #校验码
    Y = {0:1,1:0,2:'X',3:9,4:8,5:7,6:6,7:5,8:4,9:3,10:2}
    ar[17] = Y[s2]
    str1 = str()
    for i in range(len(ar)):
        str1 = str1 + str(ar[i])
    return str1
def setID():
    str1 = autoID()
    str2.set(str1)

from tkinter import *
gw  = Tk()
gw.wm_title('身份ID自动生成')
Label(gw,text='身份证ID：').grid(row=0,sticky=W)
str2 = StringVar()
en = Entry(gw,textvariable=str2)
str2.set('生成的身份证ID将在这里显示')
en.grid(row=0,column=1,sticky=W)
b1 = Button(gw,text='生成',command=setID)
b1.grid(row=1,sticky=W)
b2 = Button(gw,text='退出',command=gw.destroy)
b2.grid(row=1,column=1,sticky=W)
gw.mainloop()



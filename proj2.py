def warn(*args,**kwargs):
    pass
import warnings
warnings.warn=warn
from sklearn.linear_model import LinearRegression
import pymysql
import numpy
#percepts: [v1,v2,v3,v4], [i1,i2,i3,i4], opacity value
#quantities that should be known [il1,il2,il3,il4]
v=[]
i=[]
il=[]
opacity=int(input("Enter opacity"))
#gets input values
def get_percept():
    print("Enter voltage values")
    for it in range(4):
        v.append(int(input()))
    print("Enter current values")
    for it in range(4):
        i.append(int(input()))
    print("Enter current limit values")
    for it in range(4):
        il.append(int(input()))
#criteria 1: [v1,v2,v3,v4]>=30
#returns 1 if all conditions are met else returns -1
def criteria1():
    if v[0]>=30 and v[1]>=30 and v[2]>=30 and v[3]>=30:
        return 1
    else:
        return -1

#criteria 2: i1<i2<i3<i4
#returns 1 if all conditions are met else r
    eturns -1
def criteria2():
    if i[0]<i[1] and i[1]<i[2] and i[2]<i[3]:
        return 1
    else:
        return -1
#criteria 3: i1<=il1,i2<=il2,i3<=il3,i4<=il4
#returns 1 if all conditions are met else returns -1
def criteria3():
    if i[0]<=il[0] and i[1]<=il[1] and i[2]<=il[2] and i[3]<=il[3]:
        return 1
    else:
        return -1
#criteria 4: if opacity<=50
#returns 1 if all conditions are met else returns -1
def criteria4():
    print(opacity)
    if opacity<=50:
        return 1
    else:
        return -1
#check for optimisation
#if all above criteria are met, esp is optimised
#return 1 if all conditions are met else returns -1
def check_opt():
    b4=criteria4()
    if b4==1:
        print("esp is optimised")
        return 1
    else:
        print("esp is not optimised")
        return -1
def reduce_current(val):
    limit=il[val]
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    x=[]
    y=[]
    cur.execute("SELECT * FROM ac1")
    c=cur.fetchall()
    for row in c:
        x.append(row[0])
        y.append(row[1])
    print(x)
    print(y)
    xn=numpy.array(x)
    yn=numpy.array(y)
    #x.values.reshape(2,1)
    #y.values.reshape(2,1)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(xn)),numpy.transpose(numpy.matrix(yn)))
    k=[i[val]]
    y_predict=model.predict(k)
    if y_predict[0]<=limit:
        cur.execute("INSERT INTO ac1(x,y) VALUES(%d,%d)"%(i[val],y_predict[0]))
        db.commit()
        i[val]=y_predict[0]
    else:
        cur.execute("INSERT INTO ac1(x,y) VALUES(%d,%d)"%(i[val],i[val]/2))
        db.commit()
        i[val]=i[val]/2
def power_down_rap(val):
    limit=il[val]
    dbv=pymysql.connect("localhost","root","","esp")
    dbi=pymysql.connect("localhost","root","","esp")
    curv=dbv.cursor()
    curi=dbi.cursor()
    curv.execute("SELECT * FROM ac2v")
    curi.execute("SELECT * FROM ac2i")
    x1=[]
    y1=[]
    cv=curv.fetchall()
    for row in cv:
        x1.append(row[0])
        y1.append(row[1])
    x1n=numpy.array(x1)
    y1n=numpy.array(y1)
    print(x1n)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(x1n)),numpy.transpose(numpy.matrix(y1n)))
    k=[v[val]]
    y_predict=model.predict(k)
    if y_predict[0]>=30:
        curv.execute("INSERT INTO ac2v(x,y) VALUES(%d,%d)"%(v[val],y_predict[0]))
        dbv.commit()
        v[val]=y_predict[0]
    else:
        curv.execute("INSERT INTO ac2v(x,y) VALUES(%d,%d)"%(v[val],30))
        dbv.commit()
        v[val]=30
    x2=[]
    y2=[]
    ci=curi.fetchall()
    for row in ci:
        x2.append(row[0])
        y2.append(row[1])
    x2n=numpy.array(x2)
    y2n=numpy.array(y2)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(x2n)),numpy.transpose(numpy.matrix(y2n)))
    k=[i[val]]
    y_predict=model.predict(k)
    if y_predict[0]<=limit:
        curi.execute("INSERT INTO ac2i(x,y) VALUES(%d,%d)"%(i[val],y_predict[0]))
        dbi.commit()
        i[val]=y_predict[0]
    else:
        curi.execute("INSERT INTO ac2i(x,y) VALUES(%d,%d)"%(i[val],i[val]/2))
        dbi.commit()
        i[val]=i[val]/2
def action3(val):
    limit=il[val]
    dbv=pymysql.connect("localhost","root","","esp")
    dbi=pymysql.connect("localhost","root","","esp")
    curv=dbv.cursor()
    curi=dbi.cursor()
    curv.execute("SELECT * FROM ac3v")
    curi.execute("SELECT * FROM ac3i")
    x1=[]
    y1=[]
    cv=curv.fetchall()
    for row in cv:
        x1.append(row[0])
        y1.append(row[1])
    x1n=numpy.array(x1)
    y1n=numpy.array(y1)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(x1n)),numpy.transpose(numpy.matrix(y1n)))
    k=[v[val]]
    y_predict=model.predict(k)
    if y_predict[0]>=30:
        curv.execute("INSERT INTO ac3v(x,y) VALUES(%d,%d)"%(v[val],y_predict[0]))
        dbv.commit()
        v[val]=y_predict[0]
    else:
        curv.execute("INSERT INTO ac3v(x,y) VALUES(%d,%d)"%(v[val],30))
        dbv.coomit()
        v[val]=30
    x2=[]
    y2=[]
    ci=curi.fetchall()
    for row in ci:
        x2.append(row[0])
        y2.append(row[1])
    x2n=numpy.array(x2)
    y2n=numpy.array(y2)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(x2n)),numpy.transpose(numpy.matrix(y2n)))
    k=[i[val]]
    y_predict=model.predict(k)
    if y_predict[0]<=limit:
        curi.execute("INSERT INTO ac3i(x,y) VALUES(%d,%d)"%(i[val],y_predict[0]))
        dbi.commit()
        i[val]=y_predict[0]
    else:
        curi.execute("INSERT INTO ac3i(x,y) VALUES(%d,%d)"%(i[val],i[val]/2))
        dbi.commit()
        i[val]=i[val]/2
#fork 1: if esp is not optimised, check these in sequence
def not_opt():
    temp=0
    print("checking if opacity<=50")
    print(criteria4())
    if criteria4()==-1:
        #print("opacity= "+opacity)
        if criteria1()==-1:
            if v[0]<30 and v[0]>=20:
                print("performing current reduction on i1")
                reduce_current(0)
                print("The new current value is")
                print(i)
            elif v[0]<20:
                print("performing power down rapping on v1 and i1")
                power_down_rap(0)
                print("The new voltage and current values are")
                print(v)
                print(i)
                if v[0]<20:
                    print("Inspection required")
            if v[1]<30 and v[1]>=20:
                print("performing current reduction on i2")
                reduce_current(1)
                print("The new current value is")
                print(i)
            elif v[1]<20:
                print("performing power down rapping on v2 and i2")
                power_down_rap(1)
                print("The new current and voltage values are")
                print(v)
                print(i)
                if v[1]<20:
                    print("Inspection required")
            if v[2]<30 and v[2]>=20:
                print("performing current reduction on i3")
                reduce_current(2)
                print("The new current value is")
                print(i)
            elif v[2]<20:
                print("performing power down rapping on v3 and i3")
                power_down_rap(2)
                print("The new voltage and current values are")
                print(v)
                print(i)
                if v[2]<20:
                    print("Inspection required")
            if v[3]<30 and v[3]>=20:
                print("performing current reduction on i4")
                reduce_current(3)
                print("The new current value is")
                print(i)
            elif v[3]<20:
                print("performing power down rapping on v4 and i4")
                power_down_rap(3)
                print("The new voltage and current values are")
                print(v)
                print(i)
                if v[3]<20:
                     print("Inspection required")
        elif il[0]<il[1] and il[1]<il[2] and il[2]<il[3]:
            #criteria1 is ok- all voltages are >=30
            if i[0]<=il[0]:
                if i[1]<=il[1]:
                    if i[2]>0.9*il[2]:
                        if i[2]<il[2]:
                            print("continuous power rapping on i3")
                            print("enter value of new i3")
                            temp=int(input())
                            if temp>0.9*il[2]:
                                temp2=int(input("again enter new value of i3")) 
                                if temp2>0.9*il[2]:
                                    print("reduce current limit of i3 by 25%")
                    if i[3]>0.9*il[3]:
                        if i[3]<il[3]:
                            print("contnuous power rapping on i4")
                            temp=int(input("enter value of new i4"))
                            if temp>0.9*il[3]: 
                                temp2=int(input("again enter value of i4"))
                                if temp2>0.9*il[3]:
                                    print("reduce current limit of i4 by 25%")
        else: print("opacity within limits")
get_percept()
val=check_opt()
if val==-1:
    not_opt()

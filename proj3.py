def warn(*args,**kwargs):
    pass
import warnings
warnings.warn=warn
from sklearn.linear_model import LinearRegression
import pymysql
import numpy
v=[0,0,0,0]
i=[0,0,0,0]
i_limit=[200,500,1500,2000]
p4_num=0
p4_den=0
p3_num=0
p3_den=0
p21_num=0
p21_den=0
p22_num=0
p22_den=0
p11_num=0
p11_den=0
p12_num=0
p12_den=0
def get_input():
    print("enter voltage values")
    for j in range(4):
        v[j]=int(input())
    print("enter current values")
    for j in range(4):
        i[j]=int(input())
def curve4(v):
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    x=[35,37,39,41]
    y=[790,810,830,850]
    #cur.execute("SELECT * FROM crv4")
    #c=cur.fetchall()
    #for row in c:
    #    x.append(row[0])
    #    y.append(row[1])
    xn=numpy.array(x)
    yn=numpy.array(y)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(yn)),numpy.transpose(numpy.matrix(xn)))
    k=[v[3]]
    y_predict=model.predict(k)
    print(y_predict)
    return y_predict
def actionX():
    print("Do internal inspection for misalignment of electrodes, ash deposits, failure of rapping system components")
def power_down_rapping():
    print("Perform power down rapping")
def reduce_charge_ratio():
    print("Charge reduction by 25% required")
def update4(val):
    global p4_num
    global p4_den
    p4_num+=val
    p4_den+=1
def success_4():
    global p4_num
    global p4_den
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    #cur.execute("SELECT * FROM prob4")
    #c=cur.fetchall()
    x=[9,15]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    prob=(x[0]+p4_num)/(x[1]+p4_den)
    return prob
def up4():
    global p4_num
    global p4_den
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    cur.execute("SELECT * FROM prob4")
    c=cur.fetchall()
    x=[]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    cur.execute("UPDATE prob4 SET num=%d, den=%d"%(x[0]+p4_num,x[1]+p4_den))
    db.commit()
def opt_stage4(v,i,i_limit):
    flag=0
    if v[3]<30 or i[3]>=0.95*i_limit[3]:
        bound=curve4()
        prob=success_4()
        print(bound,prob)
        if i[3]>1.25*bound:
            print("current greater than 1.25 times expected value")
            power_down_rapping()
            return(0)
        elif i[3]>1.1*bound:
            print("current greater than 1.1 times expected value")
            if prob>0.25:
                print("success rate of charge reduction is >25%")
                reduce_charge_ratio()
                #get_input()
                if v[3]>30 and i[3]<0.95*i_limit[3]:
                    print("field 4 optimised")
                    update4(1)
                    return(1)
                else:
                    print("action unsuccessful")
                    update4(0)
                    flag=-1
                    return(2)
            else: 
                print("success rate of charge reduction is <25%")
                power_down_rapping()
                return(3)
        else:
            print("current less than 1.1 times expected value and greater than 0.95 times current limit")
            if flag==0:
                reduce_charge_ratio()
                #get_input()
                if v[3]>30 and i[3]<0.95*i_limit[3]:
                    print("field 4 optimised")
                    update4(1)
                    return(4)
                else:
                    print("field 4 not optimised by charge reduction")
                    update4(0)
                    return(5)
            else:
                print("previous action was charge reduction which was unsuccessful")
                power_down_rapping()
                return(6)
    #get_input()
    if v[3]<30 or i[3]>=0.95*i_limit[3]:
        print("field 4 is still not optimised")
        actionX()
        return(7)
    else:
        print("field 4 is optimised")
        return(8)
    #up4()
def up3():
    global p3_num
    global p3_den
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    cur.execute("SELECT * FROM prob3")
    c=cur.fetchall()
    x=[]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    cur.execute("UPDATE prob3 SET num=%d, den=%d"%(x[0]+p3_num,x[1]+p3_den))
    db.commit()
def curve3(v):
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    x=[35,37,39,41]
    y=[790,810,830,850]
    #cur.execute("SELECT * FROM crv3")
    #c=cur.fetchall()
    #for row in c:
    #    x.append(row[0])
    #    y.append(row[1])
    xn=numpy.array(x)
    yn=numpy.array(y)
    model=LinearRegression()
    model.fit(numpy.transpose(numpy.matrix(yn)),numpy.transpose(numpy.matrix(xn)))
    k=[v[2]]
    y_predict=model.predict(k)
    print(y_predict)
    return y_predict
def update3(val):
    global p3_num
    global p3_den
    p3_num+=val
    p3_den+=1
def success_3():
    global p3_num
    global p3_den
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    #cur.execute("SELECT * FROM prob3")
    #c=cur.fetchall()
    x=[9,15]
    #for row in c:
    #    x.append(row[0])
    #    x.append(row[1])
    prob=(x[0]+p3_num)/(x[1]+p3_den)
    return prob
def opt_stage3(v,i,i_limit):
    flag=0
    if v[2]<30 or i[2]>=0.95*i_limit[2]:
        bound=curve3(v)
        prob=success_3()
        print(bound,prob)
        if i[2]>1.25*bound:
            print("current greater than 1.25 times expected value")
            power_down_rapping()
            return(0)
        elif i[2]>1.1*bound:
            print("current greater than 1.1 times expected value")
            if prob>0.25:
                print("success rate of charge reduction is >25%")
                reduce_charge_ratio()
                #get_input()
                if v[2]>30 and i[2]<0.95*i_limit[2]:
                    print("field 3 optimised")
                    update3(1)
                    return(1)
                else:
                    print("action unsuccessful")
                    update3(0)
                    flag=-1
                    return(2)
            else: 
                print("success rate of charge reduction is <25%")
                power_down_rapping()
                return(3)
        else:
            print("current less than 1.1 times expected value and greater than 0.95 times current limit")
            if flag==0:
                reduce_charge_ratio()
                #get_input()
                if v[2]>30 and i[2]<0.95*i_limit[2]:
                    print("field 3 optimised")
                    update3(1)
                    return(4)
                else:
                    print("field 3 not optimised by charge reduction")
                    update3(0)
                    return(5)
            else:
                print("previous action was charge reduction which was unsuccessful")
                power_down_rapping()
                return(6)
    #get_input()
    if v[2]<30 or i[2]>=0.95*i_limit[2]:
        print("field 3 is still not optimised")
        actionX()
        return(7)
    else:
        print("field 3 is optimised")
        return(8)
def update22(val):
    global p22_num
    global p22_den
    p22_num+=val
    p22_den+=1
def up21():
    global p21_num
    global p21_den
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    cur.execute("SELECT * FROM prob21")
    c=cur.fetchall()
    x=[]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    cur.execute("UPDATE prob21 SET num=%d, den=%d"%(x[0]+p21_num,x[1]+p21_den))
    db.commit()
def up22():
    global p22_num
    global p22_den
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    cur.execute("SELECT * FROM prob22")
    c=cur.fetchall()
    x=[]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    cur.execute("UPDATE prob22 SET num=%d, den=%d"%(x[0]+p22_num,x[1]+p22_den))
    db.commit()
def update21(val):
    global p21_num
    global p21_den
    p21_num+=val
    p21_den+=1
def success_21():
    global p21_num
    global p21_den
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    #cur.execute("SELECT * FROM prob21")
    #c=cur.fetchall()
    x=[9,15]
    #for row in c:
    #    x.append(row[0])
    #    x.append(row[1])
    prob=(x[0]+p21_num)/(x[1]+p21_den)
    #cur.execute("UPDATE prob21 SET num=%d, den=%d"%(x[0]+p21_num,x[1]+p21_den))
    p21_num=0
    p21_den=0
    #db.commit()
    return prob
def success_22():
    global p22_num
    global p22_den
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    #cur.execute("SELECT * FROM prob22")
    #c=cur.fetchall()
    x=[9,15]
    #for row in c:
    #    x.append(row[0])
    #    x.append(row[1])
    prob=(x[0]+p22_num)/(x[1]+p22_den)
    #cur.execute("UPDATE prob3 SET num=%d, den=%d"%(x[0]+p22_num,x[1]+p22_den))
    p22_num=0
    p22_den=0
    #db.commit()
    return prob
def opt_stage2(v,i,i_limit):
    global p21_num
    global p21_den
    if v[1]>30 and i[1]<=200:
        print("increase limit by 25%")
        i_limit[1]=1.25*i_limit[1]
        #get_input()
        return(0)
    flag=0
    if v[1]<30 or i[1]>0.95*i_limit[1]:
        prob1=success_21()
        prob2=success_22()
        print(prob1,prob2)
        if (prob1<0.25 or prob2<0.5) and flag==-1:
            print("set limit of current for field 2 as 200")
            i_limit[1]=200
            #get_input()
            return(0)
        else:
            flag=-1
            print("lower value of current limit for field 2 by 25%")
            i_limit[1]=0.75*i_limit[1]
            #get_input()
            if v[1]>30 and i[1]<=0.95*i_limit[1]:
                print("field 1 optimised")
                print("updating probability values of action 1...")
                update21(1)
                return(1)
            else:
                print("action unsuccessful")
                print("again reduce value of current for field 2 by 25%")
                update21(0)
                i_limit[1]=0.75*i_limit[1]
                #get_input()
                if v[1]>30 and i[1]<=0.95*i_limit[1]:
                    print("field 2 optimised")
                    print("updating probability of action 2...") 
                    update22(1)
                    return(2)
                else:
                    print("now reduce value of current limit of field 2 by 200")
                    update22(0)
                    i_limit[1]=i_limit[1]-200
                    return(3)
    if v[1]<30 and i[1]>0.95*i_limit[1]:
        print("field 2 is still not optimised")
        actionX()
        return(4)
    else:
        print("field 2 is optimised")
        return(5)
    #up21()
    #up22()
def update12(val):
    global p12_num
    global p12_den
    p12_num+=val
    p12_den+=1
def up11():
    global p12_num
    global p12_den
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    cur.execute("SELECT * FROM prob11")
    c=cur.fetchall()
    x=[]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    cur.execute("UPDATE prob11 SET num=%d, den=%d"%(x[0]+p11_num,x[1]+p11_den))
    db.commit()
def up12():
    global p11_num
    global p11_den
    db=pymysql.connect("localhost","root","","esp")
    cur=db.cursor()
    cur.execute("SELECT * FROM prob12")
    c=cur.fetchall()
    x=[]
    for row in c:
        x.append(row[0])
        x.append(row[1])
    cur.execute("UPDATE prob12 SET num=%d, den=%d"%(x[0]+p12_num,x[1]+p12_den))
    db.commit()
def update11(val):
    global p11_num
    global p11_den
    p11_num+=val
    p11_den+=1
def success_12():
    global p12_num
    global p12_den
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    #cur.execute("SELECT * FROM prob12")
    #c=cur.fetchall()
    x=[9,15]
    #for row in c:
    #    x.append(row[0])
    #    x.append(row[1])
    prob=(x[0]+p12_num)/(x[1]+p12_den)
    return prob
def success_11():
    global p11_num
    global p11_den
    #db=pymysql.connect("localhost","root","","esp")
    #cur=db.cursor()
    #cur.execute("SELECT * FROM prob11")
    #c=cur.fetchall()
    x=[9,15]
    #for row in c:
    #    x.append(row[0])
    #    x.append(row[1])
    prob=(x[0]+p11_num)/(x[1]+p11_den)
    return prob
def opt_stage1(v,i,i_limit):
    global p11_num
    global p11_den
    #v=[31,32,33,34]
    #i=[195,300,900,1100]
    #i_limit=[250,400,1200,1500]
    if v[0]>30 and i[0]<=200:
        print("increase limit by 25%")
        i_limit[0]=1.25*i_limit[0]
        #v=[28,32,33,34]
        #i=[210,300,900,1100]
        #get_input()
    flag=0
    if v[0]<30 or i[0]>0.95*i_limit[0]:
        prob1=success_11()
        prob2=success_12()
        prob1=0.3
        prob2=0.8
        print(prob1,prob2)
        if (prob1<0.25 or prob2<0.5) and flag==-1:
            print("set limit of current for field 1 as 200")
            i_limit[0]=200
            return(0)
            #get_input()
        else:
            flag=-1
            print("lower value of current limit for field 1 by 25%")
            i_limit[0]=0.75*i_limit[0]
            #get_input()
            if v[0]>30 and i[0]<=0.95*i_limit[0]:
                print("field 1 optimised")
                print("updating probability values of action 1...")
                update11(1)
                return(1)
            else:
                print("action unsuccessful")
                print("again reduce value of current for field by 25%")
                update11(0)
                i_limit[0]=0.75*i_limit[0]
                #get_input()
                if v[0]>30 and i[0]<=0.95*i_limit[0]:
                    print("field 1 optimised")
                    print("updating probability of action 2...") 
                    update12(1)
                    return(2)
                else:
                    print("now reduce value of current limit of field 1 by 200")
                    update12(0)
                    i_limit[0]=i_limit[0]-200
                    return(3)
    if v[0]<30 and i[0]>0.95*i_limit[0]:
        print("field 1 is still not optimised")
        actionX()
        return(4)
    else:
        print("field 1 is optimised")
        return(5)
    #up11()
    #up12()
def check_opacity():
    print("enter value of opacity")
    op=int(input())
    return op
def start():
    op=56
    if op>50:
        get_input()
        print("optimising field 1")
        value1=opt_stage1(v,i,i_limit)
        print("optimising field 2")
        value2=opt_stage2(v,i,i_limit)
        print("optimising field 3")
        value3=opt_stage3(v,i,i_limit)
        print("optimising field 4")
        value4=opt_stage4(v,i,i_limit)
        print(value1,value2,value3,value4)
start()

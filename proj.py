from sklearn.linear_model import LinearRegression
import pymysql
v=[35,20,30,17]
i=[400,500,600,700]
out_v=[]
out_i=[]
out_v_val=[]
out_i_val=[]
#ct=[0,0,0]
#wt=[0,0,0]
#prob=[0,0,0]
#dec is used in decide function 
dec=[]
ct=[]
wt=[]
prob=[]
pri=[2,1,3]
db1=pymysql.connect("localhost","arushi","raspi","ac1")
db2=pymysql.connect("localhost","arushi","raspi","ac2v")
db3=pymysql.connect("localhost","arushi","raspi","ac3v")
db4=pymysql.connect("localhost","arushi","raspi","ac2i")
db5=pymysql.connect("localhost","arushi","raspi","ac3i")
dbs=pymysql.connect("localhost","arushi","raspi","stat")
c1=db1.cursor()
c2=db2.cursor()
c3=db3.cursor()
c4=db4.cursor()
c5=db5.cursor()
c22=dbs.cursor()
def initi():
    c22.execute("SELECT ct FROM stat")
    ctt=c22.fetchall()
    for row in ctt:
        ct.append(row[1])
        wt.append(row[2])
        prob.append(row[3])
def find_out_v():
    for k in range(4):
        if (v[k]<30):
            out_v.append(k)
            out_v_val.append(i[k])
def find_out_i():
    for k in range(3):
        if i[k]>i[k+1]:
            out_i.append(k+1)
            out_i_val.append(i[k+1])
def action1():
    ct[0]=ct[0]+1
    #charge ratio increase
    #priority 2
    #reduce i value
    #---------------------------------
    #get y and x arrays
    x=[]
    y=[]
    c1.execute("SELECT * FROM ac1")
    a1x=c1.fetchall()
    for row in a1x:
        x.append(row[0])
        y.append(row[1])
    model=LinearRegression()
    model.fit(x,y)
    y_predict=model.predict(out_i_val)
    it=0
    for k in out_i:
        i[k]=y_predict[it]
        it=it+1
def action2():
    ct[1]=ct[1]+1
    #power down rapping
    #priority 1
    #increase v and i
    #---------------------------------
    #for voltages
    #get x1,y1
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    c2.execute("SELECT * FROM ac2v")
    a2x=c2.fetchall()
    for row in a2x:
        x1.append(row[0])
        y1.append(row[1])
        #x2.append(row[2])
        #y2.append(row[3])
    c4.execute("SELECT * FROM ac2i")
    a2y=c4.fetchall()
    for row in a2y:
        x2.append(row[0])
        y2.append(row[1])
    model=LinearRegression()
    model.fit(x1,y1)
    y_predict=model.predict(out_v_val)
    it=0
    for k in out_v:
        v[k]=y_predict[it]
        it=it+1
    #----------------------------------
    #for current
    #get x2,y2
    model.fit(x2,y2)
    y_predict=model.predict(out_i_val)
    it=0
    for k in out_i:
        i[k]=y_predict[it]
        it=it+1
def action3():
    ct[2]=ct[2]+1
    #continuous rapping for 10 min
    #priority 3
    #increase v and i
    #----------------------------------
    #for voltage
    #get x1,y1
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    c3.execute("SELECT * FROM ac3v")
    a2x=c3.fetchall()
    for row in a2x:
        x1.append(row[0])
        y1.append(row[1])
        #x2.append(row[2])
        #y2.append(row[3])
    c5.execute("SELECT * FROM ac3i")
    a2y=c5.fetchall()
    for row in a2y:
        x2.append(row[0])
        y2.append(row[1])
    model=LinearRegression()
    model.fit(x1,y1)
    y_predict=model.predict(out_v_val)
    it=0
    for k in out_v:
        v[k]=y_predict[it]
        it=it+1
    #----------------------------------
    #for current
    #get x2,y2
    model.fit(x2,y2)
    y_predict=model.predict(out_i_val)
    it=0
    for k in out_i:
        i[k]=y_predict[it]
        it=it+1
#def action4():
#    ct[3]=ct[3]+1
def assign_wt(action,success):
    wt[action-1]=wt[action-1]+success
    prob[action-1]=wt[action-1]/ct[action-1]
def eval_act1():
    find_out_v()
    find_out_i()
    print(out_v)
    print(out_i)
    val=get_opacity()
    if val<50:
        assign_wt(1,1)
        for it in range(len(out_v)):
            c3.execute("INSERT INTO ac1(x,y) VALUES(%d,%d)" %(out_i_val[it],v[out_i[it]]))
            db1.commit()
    else:
        assign_wt(1,-1)
        c22.execute("UPDATE stat SET prob=%d WHERE sno='1'" %(prob[0]))
        dbs.commit()
        c22.execute("UPDATE stat SET wt=%d WHERE sno='1'" %(wt[0]))
        dbs.commit()
        c22.execute("UPDATE stat SET ct=%d WHERE sno='1'" %(ct[0]))
        dbs.commit()
def eval_act2():
    #find_out_v()
    #find_out_i()
    #print(out_v)
    #print(out_i)
    val=get_opacity()
    if val<50:
    #if len(out_v)==0 and len(out_i)==0:
        assign_wt(2,1)
        for it in range(len(out_v)):
            c2.execute("INSERT INTO ac2v(x,y) VALUES(%d,%d)" %(out_v_val[it],v[out_v[it]]))
            db2.commit()
            c4.execute("INSERT INTO ac2i(x,y) VALUES(%d,%d)" %(out_i_val[it],v[out_i[it]]))
            db4.commit()
    else:
        assign_wt(2,-1)
        c22.execute("UPDATE stat SET prob=%d WHERE sno='2'" %(prob[1]))
        dbs.commit()
        c22.execute("UPDATE stat SET wt=%d WHERE sno='2'" %(wt[1]))
        dbs.commit()
        c22.execute("UPDATE stat SET ct=%d WHERE sno='2'" %(ct[1]))
        dbs.commit()
def eval_act3():
    #find_out_v()
    #find_out_i()
    #print(out_v)
    #print(out_i)
    val=get_opacity()
    if val<50:
    #if len(out_v)==0 and len(out_i)==0:
        assign_wt(3,1)
        for it in range(len(out_v)):
            c3.execute("INSERT INTO ac3v(x,y) VALUES(%d,%d)" %(out_v_val[it],v[out_v[it]]))
            db3.commit()
            c5.execute("INSERT INTO ac3i(x,y) VALUES(%d,%d)" %(out_i_val[it],v[out_i[it]]))
            db5.commit()
    else:
        assign_wt(3,-1)
        c22.execute("UPDATE stat SET prob=%d WHERE sno='3'" %(prob[2]))
        dbs.commit()
        c22.execute("UPDATE stat SET wt=%d WHERE sno='3'" %(wt[2]))
        dbs.commit()
        c22.execute("UPDATE stat SET ct=%d WHERE sno='3'" %(ct[2]))
        dbs.commit()
def decide():
    high=0
    for k in range(3):
        if prob[k]>prob[high]:
            high=k
            dec.append(k)
    h2=priority()
    return h2
def priority():
    high=dec[0]
    if len(dec)>1:
        for k in dec:
            if pri[k]>pri[high]:
                high=k
    return high
#find_out_v()
#print(out_v)
#find_out_i()
#print(out_i)
def work():
    #this function checks opacity and takes action accordingly
    #this ignores anomalies in voltage and current if opacity is within norms
    find_out_v()
    find_out_i()
    action=decide()
    if action==1:
        action1()
        eval_act1()
    if action==2:
        action2()
        eval_act2()
    if action==3:
        action3()
        eval_act3()
    if action==4:
        action4()
        eval_act4()
    db1.close()
    db2.close()
    db3.close()
    db4.close()
    db5.close()
    dbs.close()

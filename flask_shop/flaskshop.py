from flask import Flask, render_template, url_for, request, redirect,session, Markup,flash
#from flask_mysqldb import MySQL
import yaml
import random
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)


app.secret_key = 'helloworld'
butStat=False
butStat1=False
searchID=''
globCartid=''
globitemid=''
ratID=''
#configure db
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql=MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    if 'loggedin' in session:
        check=True;
        return render_template('index.html', check=check)
    else:
        check=False;
        return render_template('index.html',check=check)


@app.route('/aboutUs')
def aboutUs():
    if 'loggedin' in session:
        check=True;
        return render_template('aboutUs.html', check=check)
    else:
        check=False;
        return render_template('aboutUs.html',check=check)
@app.route('/review',methods=['GET','POST'])
def review():
    global globitemid
    global ratID
    cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur2.execute('SELECT review_id FROM reviews order by review_id desc')
    latestU=cur2.fetchone()
    cur2.close()
    finalU=""
    if latestU:
        stringTran=latestU['review_id']
        a=list(stringTran)
        b=a[-1]
        c=int(b)
        c=c+1
        d=str(c)
        d=list(d)
        e=a[:3]
        e=e+d
        finalU=finalU.join(e)
    else:
        finalU="R100"

    if 'loggedin' in session:
        cid=session['id']
        if request.method=='POST' and 'rating' in request.form:
            print('I\'m here')
            rDetails= request.form
            ratID=rDetails['rating']
            itemID=str(globitemid)
            print(itemID)
            x=float(ratID)
            con=mysql.connect
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('INSERT INTO reviews VALUES(%s,%s,%s)', (finalU,itemID,x))
            print('1')
            con.commit()
            con.close()
            return redirect(url_for('products'))
        check=True;
        return render_template('review.html',check=check,cid=cid,globitemid=globitemid)
    else:
        check=False;
        return render_template('review.html',check=check)

@app.route('/signUp',methods=['GET','POST'])
def signUp():
    cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur2.execute('SELECT user_id FROM user order by user_id desc')
    latestU=cur2.fetchone()
    cur2.close()
    finalU=""
    if latestU:
        stringTran=latestU['user_id']
        a=list(stringTran)
        b=a[-1]
        c=int(b)
        c=c+1
        d=str(c)
        d=list(d)
        e=a[:3]
        e=e+d
        finalU=finalU.join(e)
    else:
        finalU="U100"
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form:
        userDetails=request.form
        print(userDetails)
        name=userDetails['fullname']
        pwd=userDetails['password']
        ph=userDetails['phoneno']
        em=userDetails['email']
        gn=userDetails['gender']
        ad=userDetails['address']
        con=mysql.connect
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        print('1')
        cur.execute('INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s)', (finalU, name, ad, gn, ph, em, pwd))

        con.commit()
        con.close()
        return redirect(url_for('login'))

    return render_template('signUp.html')


@app.route('/login',methods=['GET','POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form:
        #fetch form data
        userDetails=request.form
        name=userDetails['fullname']
        pwd=userDetails['password']
        # Check if account exists using MySQL
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM user WHERE name = %s AND password = %s', (name, pwd))
        # Fetch one record and return result
        account = cur.fetchone()
        cur.close()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            check=session['loggedin']
            session['id'] = account['user_id']
            session['username'] = account['name']
            session['email_id'] = account['email_id']
            session['password'] = account['password']
            session['address'] = account['address']
            session['phone_no'] = account['phone_no']
            session['gender'] = account['gender']
            ui=account['user_id']
            con = mysql.connect
            cur1 = con.cursor(MySQLdb.cursors.DictCursor)
            #cur1=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur1.execute('SELECT user_id from cart where user_id = %s',[ui])
            x = cur1.fetchone()
            print(x)
            if not x:
                temp="C"+account['user_id']
                a=list(temp)
                a[1]='R'
                temp=''
                temp=temp.join(a)
                args=[temp,0.0,account['user_id']]
                result_args = cur1.callproc('insert_cart', args)
                con.commit()
                print(result_args[1])
            con.close()

            #print(type(account['user_id']))
            #cust['id'] = account['user_id']
            #cust['username'] = account['name']
            # Redirect to home page
            return redirect(url_for('products'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login/logout')
def logout():
    global globCartid
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('address', None)
    session.pop('phone_no', None)
    session.pop('gender', None)
    session.pop('password', None)
    session.pop('email_id', None)
    globCartid=''
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/products',methods=['GET','POST'])
def products():
    global butStat
    global searchID
    global globitemid
    global ratID
    msg=''
    cur1= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur1.execute('SELECT * FROM products')
    cur2.execute('SELECT * FROM category')
    row= cur1.fetchall()
    #prods=list(row)
    #print(prods)
    row3=cur2.fetchall()
    cur1.close()
    cur2.close()
    if request.method == 'POST' and 'search' in request.form:
        sDetails=request.form
        searchID=sDetails['search']
        return redirect(url_for('searchPage'))

    if 'loggedin' in session:
        cid=session['id']
        '''if request.method == 'POST' and 'rating' in request.form:
            rDetails=request.form
            ratID=rDetails['rating']
            return redirect(url_for('review'))'''
        if request.method == 'POST' and 'iid' in request.form:
            #fetch form data
            itemDetails=request.form
            iidx=itemDetails['iid']
            globitemid=iidx
            conn=mysql.connect
            cur3=conn.cursor(MySQLdb.cursors.DictCursor)
            cur3.execute('SELECT * FROM products where item_id = %s',[iidx])
            x=cur3.fetchone()
            #cur4=conn.cursor(MySQLdb.cursors.DictCursor)
            cur3.execute('SELECT cart_id from cart where user_id = %s', [cid])
            y=cur3.fetchone()
            args=[y['cart_id'],x['item_id'],1,0]
            stat=cur3.callproc('insert_cart_items', args)
            cur3.execute('SELECT @_insert_cart_items_3')
            res = cur3.fetchone()
            print(res['@_insert_cart_items_3'])
            if res['@_insert_cart_items_3']:
                message= 'Item added to cart!'
                butStat=True
                print("hello")
            else:
                butStat=False
                message='Item could not be added to cart!'
            flash(message)
            conn.commit()
            conn.close()
        check=True;
        return render_template('products.html',username=session['username'],row=row,row3=row3,check=check,butStat=butStat)
    else:
        check=False;
        return render_template('products.html',row=row,row3=row3,check=check,butStat=False)


@app.route('/cart',methods=['GET','POST'])
def cart():
    msg=''
    if 'loggedin' in session:
        cid=session['id']
        cur1= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1.execute('SELECT * FROM cart WHERE user_id = %s', [cid])
        ucart=cur1.fetchone()
        tot=ucart['total_price']
        cur2.execute('SELECT p.item_id as myid,p.item_name as nm, p.item_price as ip, ci.qty as qt FROM cart_items as ci ,products as p WHERE ci.cart_id =%s and p.item_id=ci.item_id',[ucart['cart_id']])
        ucitem=cur2.fetchall()
        cur1.close()
        cur2.close()
        check=True;
        if ucitem:
            if request.method == 'POST' and 'idname' in request.form:
                cDetails=request.form
                itemname=cDetails['idname']
                cur4=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur4.execute('SELECT item_id FROM products WHERE item_name = %s', [itemname])
                n=cur4.fetchone()
                cur4.close()
                conn=mysql.connect
                cur3=conn.cursor(MySQLdb.cursors.DictCursor)
                m=ucart['cart_id']
                args=[m,n['item_id'],0]
                #stat=cur3.callproc('insert_cart_items', args)
                stat=cur3.callproc('delete_cart_items', args)
                cur3.execute('SELECT @_delete_cart_items_2')
                res = cur3.fetchone()
                conn.commit()
                conn.close()
                print(res['@_delete_cart_items_2'])
                if res['@_delete_cart_items_2']:
                    return redirect(url_for('cart'))
                    print(res['@_delete_cart_items_2'])

            if request.method == 'POST' and 'ianame' in request.form:
                cDetails=request.form
                itemname=cDetails['ianame']
                cur4=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur4.execute('SELECT item_id FROM products WHERE item_name = %s', [itemname])
                n=cur4.fetchone()
                cur4.close()
                conn=mysql.connect
                cur3=conn.cursor(MySQLdb.cursors.DictCursor)
                m=ucart['cart_id']
                args=[m,n['item_id'],1,0]
                #stat=cur3.callproc('insert_cart_items', args)
                stat=cur3.callproc('insert_cart_items', args)
                cur3.execute('SELECT @_insert_cart_items_3')
                res = cur3.fetchone()
                conn.commit()
                conn.close()
                print(res['@_insert_cart_items_3'])
                if res['@_insert_cart_items_3']:
                    return redirect(url_for('cart'))
                    print(res['@_insert_cart_items_3'])


            return render_template('cart.html', check=check,ucitem=ucitem,tot=tot)

        else:
            return render_template('cart.html', check=check)
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cid=session['id']
        cnm=session['username']
        cad=session['address']
        cph=session['phone_no']
        cgd=session['gender']
        cem=session['email_id']
        cpd=session['password']

        cur1= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1.execute('SELECT o.order_id as oid,o.order_amt as oam,o.transaction_id as tid FROM orders o,payment p where o.transaction_id= p.transaction_id and  p.user_id=%s',[cid])
        row= cur1.fetchall()
        cur1.close()
        print(row)
        check=True;
        return render_template('profile.html', check=check,cid=cid,cnm=cnm,cad=cad,cph=cph,cgd=cgd,cem=cem,cpd=cpd,row=row)
    else:
        return redirect(url_for('login'))

@app.route('/searchPage',methods=['GET','POST'])
def searchPage():
    global searchID
    global butStat1
    global globitemid
    temp=''
    if request.method == 'POST' and 'search' in request.form:
        sDetails=request.form
        searchID=sDetails['search']

    temp=searchID+'%'
    cur1= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur1.execute('SELECT * FROM products where item_name LIKE %s',[temp])
    row= cur1.fetchall()

    cur1.close()

    if 'loggedin' in session:
        cid=session['id']
        if request.method == 'POST' and 'iid' in request.form:
            #fetch form data
            itemDetails=request.form
            iidx=itemDetails['iid']
            globitemid=iidx
            conn=mysql.connect
            cur3=conn.cursor(MySQLdb.cursors.DictCursor)
            cur3.execute('SELECT * FROM products where item_id = %s',[iidx])
            x=cur3.fetchone()
            #cur4=conn.cursor(MySQLdb.cursors.DictCursor)
            cur3.execute('SELECT cart_id from cart where user_id = %s', [cid])
            y=cur3.fetchone()
            args=[y['cart_id'],x['item_id'],1,0]
            stat=cur3.callproc('insert_cart_items', args)
            cur3.execute('SELECT @_insert_cart_items_3')
            res = cur3.fetchone()
            print(res['@_insert_cart_items_3'])
            if res['@_insert_cart_items_3']:
                butStat1=True
                message= 'Item added to cart!'
                print("hello")
            else:
                butStat1=False
                message='Item could not be added to cart!'
            flash(message)
            conn.commit()
            conn.close()
        check=True;
        return render_template('searchPage.html', check=check, row=row,butStat=butStat1,username=session['username'])
    else:
        check=False;
        return render_template('searchPage.html',check=check, row=row,butStat=False)


@app.route('/receipt')
def receipt():
    global globCartid
    if 'loggedin' in session:
        cid=session['id']
        cnm=session['username']
        cad=session['address']
        cph=session['phone_no']
        cur1= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1.execute('SELECT * FROM cart WHERE user_id = %s', [cid])
        ucart=cur1.fetchone()
        tot=ucart['total_price']
        globCartid=ucart['cart_id']
        cur2.execute('SELECT sum(qty) as sp FROM cart_items group by cart_id having cart_id=%s',[ucart['cart_id']])
        ucitem=cur2.fetchone()
        totquant=ucitem['sp']
        cur1.close()
        cur2.close()
        check=True
        return render_template('receipt.html', check=check,cnm=cnm,cad=cad,cph=cph,tot=tot,totquant=totquant)
    else:
        return redirect(url_for('login'))
'''@app.route('/review')
def review():
    if 'loggedin' in session:
        return redirect(url_for('review'))'''
@app.route('/confirmation')
def confirmation():
    global globCartid
    if 'loggedin' in session:
        cid=session['id']
        cad=session['address']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT transaction_id FROM payment order by transaction_id desc')
        latestT=cur.fetchone()
        cur.close()

        cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur2.execute('SELECT order_id FROM orders order by order_id desc')
        latestO=cur2.fetchone()
        cur2.close()

        finalT=""
        finalO=""
        if latestT:
            stringTran=latestT['transaction_id']
            a=list(stringTran)
            b=a[-1]
            c=int(b)
            c=c+1
            d=str(c)
            d=list(d)
            e=a[:3]
            e=e+d
            finalT=finalT.join(e)
        else:
            finalT="T100"
        if latestO:
            stringTran=latestO['order_id']
            a=list(stringTran)
            b=a[-1]
            c=int(b)
            c=c+1
            d=str(c)
            d=list(d)
            e=a[:3]
            e=e+d
            finalO=finalO.join(e)
        else:
            finalO="O100"

        args=[finalO,finalT,cid,0]
        conn=mysql.connect
        cur3=conn.cursor(MySQLdb.cursors.DictCursor)
        stat=cur3.callproc('insert_payment', args)
        cur3.execute('SELECT @_insert_payment_3')
        res = cur3.fetchone()
        conn.commit()
        conn.close()
        conn1=mysql.connect
        cur4=conn1.cursor(MySQLdb.cursors.DictCursor)
        args1=[finalO,globCartid,0]
        stat1=cur4.callproc('insert_orderitems', args1)
        cur4.execute('SELECT @_insert_orderitems_2')
        conn1.commit()
        conn1.close()
        res1 = cur4.fetchone()

        if res['@_insert_payment_3'] and res1['@_insert_orderitems_2']:
            #return redirect(url_for('cart'))
            print(res1['@_insert_orderitems_2'])
            print(res['@_insert_payment_3'])
            cur5=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur5.execute('SELECT employee_id,name,phone_no FROM employee where area_code=%s',[cad])
            empDet=cur5.fetchone()
            cur5.close()
            check=True
            return render_template('confirmation.html', check=check,cid=cid,finalO=finalO,empDet=empDet)
        '''
        check=True
        return render_template('confirmation.html', check=check,cid=cid)
        '''
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

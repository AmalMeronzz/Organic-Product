from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

# Create your views here.
from textblob import TextBlob


def temfunc():
    return None

def login(request):
    if request.method == 'POST':
        idname = request.POST['name']
        password = request.POST['password']
        print(idname,password)

        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id = '"+str(idname)+"' and password = '"+str(password)+"'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from agri_shop_register where shop_id = '" + str(idname) + "' and password = '"+str(password)+"' and status = 'approved'")
            shop = cursor.fetchone()
            if shop == None:
                cursor.execute("select * from farmer where farmer_id = '"+str(idname)+"' and password = '"+str(password)+"' and status = 'approved'")
                farmer = cursor.fetchone()
                if farmer == None:
                    cursor.execute("select * from user_register where user_id = '"+str(idname)+"' and password = '"+str(password)+"'")
                    user = cursor.fetchone()
                    if user == None:
                        return redirect('login')
                    else:
                        request.session["userid"] = idname
                        return redirect('userindex')
                else:
                    request.session["farmerid"] = idname
                    return redirect('farmerindex')
            else:
                request.session["shopid"] = idname
                return redirect('shopindex')
        else:
            request.session["adminid"] = idname
            return redirect('adminindex')
    else:
        return render(request,'login.html')

def login_home(request):
    return render(request,'login_home.html')

def logout1(request):
    logout(request)
    return redirect('login')

def admin_home(request):
    return render(request,'admin/index.html')

def new_shop_registration(request):
    cursor = connection.cursor()
    cursor.execute("select * from agri_shop_register where status ='pending'")
    shop = cursor.fetchall()
    return render(request,'admin/New_shop_registration.html',{'data':shop})

def approve_shop(request,id):
    cursor = connection.cursor()
    cursor.execute("update agri_shop_register set status = 'approved' where shop_id = '"+id+"' ")
    return redirect('newshopregistration')

def delete_shop(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from agri_shop_register where shop_id = '"+id+"'")
    return redirect('approvedshop')

def approved_shop(request):
    cursor = connection.cursor()
    cursor.execute("select * from agri_shop_register where status = 'approved'")
    shop = cursor.fetchall()
    return render(request,'admin/view_approved_shop.html',{'data':shop})

def farmer_registration(request,id):
    if request.method == 'POST':
        idfarmer = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']

        cursor = connection.cursor()

        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id = '" + str(idfarmer) + "' and password = '" + str(password) + "'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from agri_shop_register where shop_id = '" + str(idfarmer) + "' and password = '" + str(password) + "'")
            shop = cursor.fetchone()
            if shop == None:
                cursor.execute("select * from user_register where user_id = '" + str(idfarmer) + "' and password = '" + str(password) + "'")
                user = cursor.fetchone()
                if user == None:
                    cursor.execute("select * from farmer where name = '"+str(name)+"'")
                    farmer = cursor.fetchone()
                    if farmer == None:
                        cursor.execute("insert into farmer values('"+str(idfarmer)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(password)+"','"+id+"','pending')")
                        return redirect('login')
                    else:
                        return HttpResponse("<script>alert('User Name already exists');window.location='../allshoplist';</script>")
                else:
                    return HttpResponse("<script>alert('User Name already exists');window.location='../allshoplist';</script>")
            else:
                return HttpResponse("<script>alert('User Name already exists');window.location='../allshoplist';</script>")
        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../allshoplist';</script>")

    else:
        return render(request,'farmer_register.html')

def shop_registration(request):
    if request.method =='POST':
        name = request.POST['name']
        place = request.POST['is_place1']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        cursor = connection.cursor()

        cursor.execute("select * from login where admin_id = '" + str(name) + "'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from farmer where farmer_id = '" + str(name) + "'")
            farmer = cursor.fetchone()
            if farmer == None:
                cursor.execute("select * from user_register where user_id = '" + str(name) + "'")
                user = cursor.fetchone()
                if user == None:
                    cursor.execute("select * from agri_shop_register where shop_id = '"+str(name)+"'")
                    shop = cursor.fetchone()
                    if shop == None:
                        cursor.execute("insert into agri_shop_register values('"+str(name)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(password)+"','"+str(place)+"','"+str(image)+"','pending')")
                        return redirect('login')
                    else:
                        return HttpResponse("<script>alert('Shop name already exists');window.location='../shopregistration';</script>")

                else:
                    return HttpResponse("<script>alert('Shop name already exists');window.location='../shopregistration';</script>")

            else:
                return HttpResponse("<script>alert('Shop name already exists');window.location='../shopregistration';</script>")

        else:
            return HttpResponse("<script>alert('Shop name already exists');window.location='../shopregistration';</script>")

    else:
        return render(request,'shop_register.html')


def shop_home(request):
    return render(request,'shop/index.html')

def view_new_farmer(request):
    shopid = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("select * from farmer where status = 'pending' and shop_id = '"+shopid+"'")
    farmer = cursor.fetchall()
    return render(request,'shop/view_new_farmer.html',{'data':farmer})

def approve_farmer(request,id):
    cursor = connection.cursor()
    cursor.execute("update farmer set status = 'approved' where farmer_id = '"+id+"'")
    return redirect('viewnewfarmer')

def delete_farmer(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from farmer where farmer_id = '"+id+"'")
    return redirect('viewnewfarmer')

def view_approved_farmer(request):
    shopid = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("select * from farmer where status = 'approved' and shop_id = '"+shopid+"'")
    farmer = cursor.fetchall()
    return render(request,'shop/view_approved_farmer.html',{'data':farmer})

def delete_farmer1(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from farmer where farmer_id = '"+id+"'")
    return redirect('viewapprovedfarmer')

def farmer_home(request):
    return render(request,'farmer/index.html')

def all_shop_list(request):
    cursor = connection.cursor()
    cursor.execute("select * from agri_shop_register where status = 'approved'")
    shop = cursor.fetchall()
    return render(request,'allshoplist.html',{'data':shop})


def user_registration(request):
    if request.method == 'POST':
        userid = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        pincode = request.POST['pincode']
        password = request.POST['password']

        cursor =  connection.cursor()

        cursor.execute("select * from login where admin_id = '" + str(userid) + "'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from farmer where farmer_id = '" + str(userid) + "'")
            farmer = cursor.fetchone()
            if farmer == None:
                cursor.execute("select * from agri_shop_register where shop_id = '" + str(userid) + "'")
                shop = cursor.fetchone()
                if shop == None:
                    cursor.execute("select * from user_register where user_id = '"+str(userid)+"'")
                    user = cursor.fetchone()
                    if user == None:
                        cursor.execute("insert into user_register values('"+str(userid)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(pincode)+"','"+str(password)+"')")
                        request.session["userid"] = userid
                        return redirect('userindex')
                    else:
                        return HttpResponse("<script>alert('User Name already exists');window.location='../userregistration';</script>")

            else:
                return HttpResponse("<script>alert('User Name already exists');window.location='../userregistration';</script>")

        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../userregistration';</script>")

    else:
        return render(request,'user_register.html')


def viewfarmer(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from farmer where shop_id = '"+id+"'")
    data = cursor.fetchall()
    return render(request,'admin/view_farmer.html',{'data':data})

def edit_shop(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.POST['name']
        place = request.POST['place']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES['is_image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        cursor.execute("update agri_shop_register set name='"+str(name)+"',place='"+str(place)+"',email='"+str(email)+"',phone='"+str(phone)+"',address='"+str(address)+"',password='"+str(password)+"',image='"+str(image)+"' where shop_id = '"+id+"'")
        return redirect('approvedshop')

    else:
        cursor.execute("select * from agri_shop_register where shop_id = '"+id+"'")
        data = cursor.fetchall()
        return render(request,'admin/edit_shop.html',{'data':data})


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['categoryname']

        cursor = connection.cursor()
        cursor.execute("insert into category values(null,'"+str(category_name)+"')")
        print("insert into category values(null,'"+str(category_name)+"')")

        return redirect('addcategory')
    else:
        return render(request,'admin/add_category.html')

def view_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'admin/view_category.html',{'data':category})

def edit_category(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.POST['name']

        cursor.execute("update category set name ='"+str(name)+"' where idcategory = '"+id+"'")
        return redirect('viewcategory')
    else:
        cursor.execute("select * from category where idcategory = '"+id+"'")
        category = cursor.fetchone()
        return render(request,'admin/edit_category.html',{'data':category})

def delete_category(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from category where idcategory = '"+id+"'")
    return redirect('viewcategory')

def add_items(request,id):
    if request.method == 'POST':
        item_name = request.POST['itemname']
        farmer_price = request.POST['farmerprice']
        public_price = request.POST['publicprice']

        cursor = connection.cursor()
        cursor.execute("insert into item_details values(null,'"+id+"','"+item_name+"','"+farmer_price+"','"+public_price+"')")
        print("value inserted into item_details")
        return redirect('viewcategory')
    else:
        return render(request,'admin/add_items.html')


def category_view(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'admin/category_items.html',{'data':category})

def view_items(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from item_details where idcategory = '"+id+"'")
    items = cursor.fetchall()
    return render(request,'admin/view_items.html',{'data':items})

def edit_item(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        item_name = request.POST['itemname']
        farmer_price = request.POST['farmerprice']
        public_price = request.POST['publicprice']

        cursor.execute("update item_details set name='"+str(item_name)+"',farmer_price='"+str(farmer_price)+"',public_price='"+str(public_price)+"' where iditem_details = '"+id+"'")
        print("value inserted into item_details")
        return redirect('categoryview')
    else:
        cursor.execute("select * from item_details where iditem_details = '" + id + "'")
        category = cursor.fetchone()
        return render(request, 'admin/edit_item.html',{'data':category})


def delete_item(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from item_details where iditem_details = '"+id+"'")
    return redirect('categoryview')

def view_shop_orders(request):
    cursor = connection.cursor()
    cursor.execute("select agri_shop_register.shop_id from public_order_items join agri_shop_register where agri_shop_register.shop_id = public_order_items.shop_id")
    # cursor.execute("select public_order_items.*,agri_shop_register.shop_id from public_order_items JOIN agri_shop_register where agri_shop_register.shop_id = public_order_items.shop_id")
    shop = cursor.fetchall()
    shop = list(shop)

    l =[]
    for i in shop:
        n = list(i)
        l.append(n[0])
    l = set(l)
    m = list(l)
    print()
    return render(request,'admin/view_shop_order.html',{'data':m})

def admin_view_orders(request,id):
    cursor = connection.cursor()
    cursor.execute("select public_order_items.quantity,public_order_items.total,public_order_items.shop_id,public_order.order_date,public_order_items.item_name,public_order_items.image,public_order_items.user_id,public_order.shipping_address,public_order.name from public_order join public_order_items where public_order.idpublic_order = public_order_items.idpublic_order and public_order_items.shop_id = '"+id+"' ")
    orders = cursor.fetchall()
    connection.close()
    return render(request,'admin/view_order.html',{'data':orders})

def view_feedback_count(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback_count")
    feedback = cursor.fetchall()
    connection.close()
    return render(request,'admin/feedback_count.html',{'data':feedback})

def view_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback")
    feedback = cursor.fetchall()
    connection.close()
    return render(request,'admin/feedback_count.html',{'data':feedback})

# farmer
# ---------------------------------------------------------------------------------

def category_list(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'farmer/category_list.html',{'data':category})

def items_in_category(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        return redirect('categorylist')
    else:
        cursor.execute("select * from item_details where idcategory = '"+str(id)+"'")
        item = cursor.fetchall()
        return render(request,'farmer/view_items.html',{'data':item})


def add_product(request,id):
    cursor = connection.cursor()
    farmerid = request.session["farmerid"]
    if request.method == 'POST':
        shopid = str(request.POST['shopid'])
        idcategory = str(request.POST['idcategory'])
        quantity = request.POST['quantity']
        # total_amount = request.POST['totalamount']
        image = request.FILES['image']
        # if image:
        #     file_date =image.date().strftime('%Y-%m-%d %H:%M:%S')
        #     print(file_date)
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)
        print("______________________________________________________________________________________")
        print("fss",fss,"file",file,"file_url",file_url)
        # path_url = "../media/IMG_20211126_143417.jpg"
        # with Image.open("C:\ewfolder\IMG_20211126_143417.jpg") as img:
        #     exif = img.getexif()
        #     for tag_id in exif:
        #         tag = TAGS.get(tag_id, tag_id)
        #         print("tag:----------------",tag)
        #         if tag == 'DateTimeOriginal':
        #             date_taken = exif.get(tag_id)
        #         else:
        #             print("not working")
        # print(date_taken)

        cursor.execute("insert into farmer_to_shop_selling values(null,'"+str(farmerid)+"','"+shopid+"','"+idcategory+"','"+str(id)+"','"+str(quantity)+"','none',curdate(),'"+str(image)+"','pending',curdate())")
        return redirect('categorylist')

    else:
        cursor.execute("select farmer.shop_id from farmer where farmer_id ='"+farmerid+"'")
        shopid = cursor.fetchone()

        cursor.execute("select item_details.idcategory from item_details where iditem_details ='"+id+"' ")
        idcategory = cursor.fetchone()

        return render(request,'farmer/add_product.html',{'data':shopid,'data1':idcategory})


def view_product_farmer(request):
    farmerid = request.session["farmerid"]
    cursor = connection.cursor()
    cursor.execute("select * from farmer_to_shop_selling where farmer_id = '"+str(farmerid)+"'")
    product = cursor.fetchall()
    return render(request,'farmer/product.html',{'data':product})

# shop
# ----------------------------------------------------------------------------------------

def view_stock_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    connection.close()
    return render(request, 'shop/view_stock_category.html', {'data': category})

def view_stock(request,id):
    shopid = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.file_path,item_details.name,shop_item_stock_details.balance_quantity from shop_item_stock_details join item_details join farmer_to_shop_selling where farmer_to_shop_selling.category_id = '"+id+"' and farmer_to_shop_selling.iditem_details = item_details.iditem_details and farmer_to_shop_selling.shop_id = '"+shopid+"' and shop_item_stock_details.shop_id = farmer_to_shop_selling.shop_id and shop_item_stock_details.shop_id = '"+shopid+"' and shop_item_stock_details.iditem_details = item_details.iditem_details and shop_item_stock_details.shop_id = '"+shopid+"'")
    quantity = cursor.fetchall()
    return render(request,'shop/view_stock.html',{'data':quantity})

def view_category_in_shop(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request, 'shop/view_category.html', {'data': category})

def view_farmer_uploaded(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from farmer_to_shop_selling where status = 'pending' and category_id = '"+id+"' ")
    product = cursor.fetchall()
    return render(request,'shop/view_farmer_uploaded.html',{'data':product})

def approve_request(request,id,iditem,qty):
    shopid = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("update farmer_to_shop_selling set status = 'approved' where idfarmer_to_shop_selling = '"+id+"'")
    cursor.execute("select balance_quantity from shop_item_stock_details where iditem_details = '"+iditem+"' and shop_id = '"+shopid+"'")
    quantity = cursor.fetchone()

    if quantity == None:
        cursor.execute("insert into shop_item_stock_details values(null,'"+shopid+"','"+iditem+"','"+qty+"')")
        return redirect('viewfarmeruploaded', id)
    else:
        q = list(quantity)
        qtny = q[0]
        total = int(qtny) + int(qty)
        cursor.execute("update shop_item_stock_details set balance_quantity = '"+str(total)+"' where iditem_details = '"+iditem+"' and shop_id = '"+shopid+"' ")
        return redirect('viewfarmeruploaded',id)

def delete_request(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from farmer_to_shop_selling where idfarmer_to_shop_selling = '"+id+"'")
    return redirect('viewfarmeruploaded',id)

def view_product_in_shop(request):
    shop_id = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.*, item_details.name from farmer_to_shop_selling join item_details where farmer_to_shop_selling.status = 'approved' and farmer_to_shop_selling.shop_id = '"+shop_id+"' and farmer_to_shop_selling.iditem_details = item_details.iditem_details ")
    product = cursor.fetchall()
    return render(request,'shop/view_product.html',{'data':product})

# delete product from shop
def delete_product(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from farmer_to_shop_selling where idfarmer_to_shop_selling = '"+id+"'")
    return redirect('viewproductinshop')

def view_order(request):
    shopid = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("select public_order_items.quantity,public_order_items.total,public_order_items.shop_id,public_order.order_date,public_order_items.item_name,public_order_items.image,public_order_items.user_id,public_order.shipping_address,public_order.name from public_order join public_order_items where public_order.idpublic_order = public_order_items.idpublic_order and public_order_items.shop_id = '"+shopid+"' ")
    orders = cursor.fetchall()
    connection.close()
    return render(request,'shop/view_orders.html',{'data':orders})

def view_payment(request):
    shopid = request.session["shopid"]
    cursor = connection.cursor()
    cursor.execute("select public_order.* from public_order join public_order_items where public_order.idpublic_order = public_order_items.idpublic_order and public_order_items.shop_id = '"+shopid+"' ")
    payment = cursor.fetchall()
    connection.close()
    return render(request,'shop/view_payment.html',{'data':payment})


# admin
# ------------------------------------------------------------------------------------

def view_shops(request):
    cursor = connection.cursor()
    cursor.execute("select * from agri_shop_register where status = 'approved'")
    shop = cursor.fetchall()
    return render(request,'admin/view_shops.html',{'data':shop})

def shop_category(request,id):
    request.session['SHOP']=id
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    print(category)
    return render(request,'admin/shop_category.html',{'data':category})

def admin_view_stock(request,id):
    shopid = request.session['SHOP']
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.file_path,item_details.name,shop_item_stock_details.balance_quantity from shop_item_stock_details join item_details join farmer_to_shop_selling where farmer_to_shop_selling.category_id = '"+id+"' and farmer_to_shop_selling.iditem_details = item_details.iditem_details and farmer_to_shop_selling.shop_id = '"+shopid+"' and shop_item_stock_details.shop_id = farmer_to_shop_selling.shop_id and shop_item_stock_details.shop_id = '"+shopid+"' and shop_item_stock_details.iditem_details = item_details.iditem_details and shop_item_stock_details.shop_id = '"+shopid+"'")
    quantity = cursor.fetchall()
    return render(request,'admin/view_stock.html',{'data':quantity})


# user
# --------------------------------------------------------------------------------------------------------

def user_home(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request, 'user/index.html', {'data0': category})

def user_all_shops(request):
    cursor = connection.cursor()
    cursor.execute("select * from agri_shop_register where status = 'approved'")
    shop = cursor.fetchall()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'user/all_shops.html',{'data':shop,'data0': category})

def view_place(request):
    cursor = connection.cursor()
    cursor.execute("select agri_shop_register.place,agri_shop_register.shop_id from agri_shop_register where status = 'approved'")
    place = cursor.fetchall()
    return render(request,'user/view_places.html',{'data':place})


def view_shop(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from agri_shop_register where shop_id = '"+str(id)+"'")
    shop = cursor.fetchone()
    return render(request,'user/view_shop.html',{'i':shop})


def product_page(request,id):
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.*,item_details.name,item_details.public_price from farmer_to_shop_selling join item_details where farmer_to_shop_selling.iditem_details = item_details.iditem_details and category_id = '"+id+"' and status ='approved'")
    product = cursor.fetchall()

    print(product)
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'user/product.html',{'data':product,'data0': category})

def product_details(request,id):
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.*,item_details.name,item_details.public_price from farmer_to_shop_selling join item_details where farmer_to_shop_selling.iditem_details = item_details.iditem_details and idfarmer_to_shop_selling = '"+id+"'")
    product = cursor.fetchone()
    print("---------------------------------------------++",product)


    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'user/produt_detail.html',{'data':product,'data0': category})

def all_products(request):
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.*,item_details.name,item_details.public_price from farmer_to_shop_selling join item_details where farmer_to_shop_selling.iditem_details = item_details.iditem_details and status = 'approved'")
    product = cursor.fetchall()

    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'user/all_products.html',{'data':product,'data0': category})

def all_product(request,id):
    cursor = connection.cursor()
    cursor.execute("select farmer_to_shop_selling.*,item_details.name,item_details.public_price from farmer_to_shop_selling join item_details where farmer_to_shop_selling.iditem_details = item_details.iditem_details and status = 'approved' and farmer_to_shop_selling.shop_id = '"+str(id)+"'")
    product = cursor.fetchall()

    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'user/all_products.html',{'data':product,'data0': category})


def add_to_cart(request,id,iditem,idshop):
    if request.method == 'POST':
        price = request.POST['price']
        QTY = request.POST['qty']
        userid = request.session['userid']

        print(price,QTY)
        total = int(price)*int(QTY)
        print(total)
        cursor = connection.cursor()
        cursor.execute("select balance_quantity from shop_item_stock_details where iditem_details = '"+iditem+"' and shop_id = '"+idshop+"'")
        quantity = cursor.fetchone()
        print("______________________________________________++++",quantity,iditem,idshop)
        q = list(quantity)
        n = q[0]
        if int(QTY) > int(n) :
            return HttpResponse("<script>alert('Insufficient quantity, available quantity is "+str(n)+" KG');window.location='../../../allproducts';</script>")

        else:
            cursor.execute("select * from cart where userid = '"+userid+"' and idfarmerselling = '"+id+"'")
            item = cursor.fetchone()

            if item == None:
                cursor.execute("insert into cart values(null,'"+userid+"','"+id+"','"+str(QTY)+"','"+str(total)+"')")
                print("------------------------------------------------------------------------quantity",QTY)
                return redirect('viewcart')
            else:
                cursor.execute("select idcart from cart where userid = '" + userid + "' and idfarmerselling = '" + id + "'")
                idcart = cursor.fetchone()
                idcart = list(idcart)
                idcart = idcart[0]

                cursor.execute("update cart set quantity = '"+str(QTY)+"',total = '"+str(total)+"' where idcart = '"+str(idcart)+"'")
                return redirect('viewcart')
    else:
        print("------------------------------------------------------------------------hello")
        return redirect('userindex')


def view_cart(request):
    userid = request.session['userid']
    cursor = connection.cursor()
    cursor.execute("select * from cart where userid = '"+str(userid)+"'")
    cart = cursor.fetchone()
    if cart == None:
        return redirect('emptycart')
    else:
        # cursor.execute("select farmer_to_shop_selling.* from farmer_to_shop_selling join cart where farmer_to_shop_selling.idfarmer_to_shop_selling = cart.idfarmerselling")
        # product total price
        cursor.execute("select cart.*,farmer_to_shop_selling.file_path,item_details.name,item_details.public_price,farmer_to_shop_selling.shop_id from cart join farmer_to_shop_selling join item_details where item_details.iditem_details = farmer_to_shop_selling.iditem_details and cart.idfarmerselling = farmer_to_shop_selling.idfarmer_to_shop_selling and cart.userid = '"+str(userid)+"'")
        product = cursor.fetchall()

        # shop name
        cursor.execute("select farmer_to_shop_selling.shop_id from cart join farmer_to_shop_selling join item_details where item_details.iditem_details = farmer_to_shop_selling.iditem_details and cart.idfarmerselling = farmer_to_shop_selling.idfarmer_to_shop_selling and cart.userid = '"+str(userid)+"'")
        shop = cursor.fetchall()
        print("-------------------------------",shop)


        cursor.execute("select cart.*,farmer_to_shop_selling.file_path,item_details.name,item_details.public_price,sum(item_details.public_price) from cart join farmer_to_shop_selling join item_details where item_details.iditem_details = farmer_to_shop_selling.iditem_details and cart.idfarmerselling = farmer_to_shop_selling.idfarmer_to_shop_selling and cart.userid = '"+str(userid)+"'")
        total = cursor.fetchone()
        print("---------------------------------",total)
        print("---------------------------------",product)

        # cart total
        cursor.execute("select sum(cart.total) from cart where userid = '"+userid+"'")
        amount = cursor.fetchone()

        cursor.execute("select * from category")
        category = cursor.fetchall()
        connection.close()
        return render(request,'user/view_cart.html',{'data':product,'total':total,'data0': category,'amount':amount})


def remove_cart(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from cart where idcart = '"+id+"'")
    connection.close()
    return redirect('viewcart')


def check_out_page(request):
    cursor = connection.cursor()
    userid = request.session['userid']
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']


        cursor.execute("select sum(cart.total) from cart where userid = '" + userid + "'")
        amount = cursor.fetchone()
        total = amount[0]
        cursor.execute("insert into public_order values(null,'"+userid+"','"+str(address)+"','"+str(phone)+"',curdate(),'"+str(total)+"','pending','"+str(name)+"')")
        connection.close()
        return redirect('makepayment')
    else:
        cursor.execute("select * from cart where userid = '"+str(userid)+"'")
        cart = cursor.fetchone()

        if cart == None:
            return HttpResponse("<script>alert('cart is empty');window.location='../viewcart';</script>")
        else:
            print("cart is not None")
            return render(request,'user/check-out.html')

def make_payment(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        card_number = request.POST['card_no']
        cvv = request.POST['cvv']
        date = request.POST['date']
        card_holder = request.POST['card_holder']
        userid = request.session["userid"]

        cursor.execute("select * from bank where card_no = '" + str(card_number) + "' and cvv = '" + str(cvv) + "' and exp_date = '" + str(date) + "' and card_holder = '" + str(card_holder) + "'")
        card = cursor.fetchone()
        print("----------------------------------------------------------------------", card_number, date)
        if card == None:
            return redirect('makepayment')
        else:
            cursor.execute("select idpublic_order from public_order where user_id ='"+str(userid)+"' and status = 'pending' and order_date =curdate() ")
            data = cursor.fetchone()
            data = list(data)
            public_order = data[0]
            cursor.execute("select cart.*,farmer_to_shop_selling.file_path,item_details.iditem_details,item_details.name,item_details.public_price,farmer_to_shop_selling.shop_id from cart join farmer_to_shop_selling join item_details where item_details.iditem_details = farmer_to_shop_selling.iditem_details and cart.idfarmerselling = farmer_to_shop_selling.idfarmer_to_shop_selling and cart.userid = '" + str(userid) + "'")
            data = cursor.fetchall()
            data = list(data)
            n=[]
            for i in data:
                m = list(i)
                cartid =m[0]
                itemid =m[6]
                quantity =m[3]
                total = m[4]
                shopid =m[9]
                image = m[5]
                item_name = m[7]
                n.append(cartid)
                cursor.execute("insert into public_order_items values(null,'"+str(public_order)+"','"+str(itemid)+"','"+str(quantity)+"','"+str(total)+"','"+str(shopid)+"','"+str(userid)+"','"+str(item_name)+"','"+str(image)+"')")

                cursor.execute("select balance_quantity from shop_item_stock_details where iditem_details = '" + str(itemid) + "' and shop_id = '" + str(shopid) + "'")
                quantity1 = cursor.fetchone()

                q = list(quantity1)
                qtny = q[0]
                total = int(qtny) - int(quantity)
                cursor.execute("update shop_item_stock_details set balance_quantity = '" + str(total) + "' where iditem_details = '" + str(itemid) + "' and shop_id = '" + str(shopid) + "' ")

            cursor.execute("update public_order set status = 'approved' where idpublic_order ='"+str(public_order)+"' ")

            for i in n:
                cursor.execute("delete from cart where idcart ='"+str(i)+"' ")
            return render(request, 'user/success_page.html')
    else:
        cursor.execute("select * from bank")
        value = cursor.fetchone()
        return render(request, 'user/make_payment.html', {'i': value})


def public_order(request):
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']

        userid = request.session['userid']

        cursor = connection.cursor()
        cursor.execute("insert into public_order values(null,'"+str(address)+"','"+str(phone)+"',curdate(),'"+str()+"','"+str()+"')")

def my_orders(request):
    userid = request.session['userid']
    cursor = connection.cursor()
    cursor.execute("select public_order_items.quantity,public_order_items.total,public_order_items.shop_id,public_order.order_date,public_order_items.item_name,public_order_items.image from public_order join public_order_items where public_order.idpublic_order = public_order_items.idpublic_order and public_order.user_id = '"+userid+"' ")
    orders = cursor.fetchall()
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',orders)
    cursor.execute("select * from category")
    category = cursor.fetchall()

    connection.close()
    return render(request,'user/my_orders.html',{'data':orders,'data0':category})

def success_page(request):
    return render(request,'user/success_page.html')

def empty_cart(request):
    return render(request,'user/empty_cart.html')


def add_feedback(request,id):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        userid = request.session['userid']

        cursor = connection.cursor()
        cursor.execute("insert into feedback values(null,'"+str(userid)+"','"+feedback+"',curdate(),'"+id+"')")

        # Feedback = feedback
        # # print text
        # print(Feedback)
        # obj = TextBlob(Feedback)
        # # returns the sentiment of text
        # # by returning a value between -1.0 and 1.0
        # sentiment = obj.sentiment.polarity
        # print(sentiment)
        # if sentiment == 0:
        #     print('The text is neutral')
        #     cursor = connection.cursor()
        #     cursor.execute("select * from feedback_count where shopid='" + id + "' ")
        #     pins = cursor.fetchone()
        #     if pins == None:
        #         cursor = connection.cursor()
        #         cursor.execute("insert into feedback_count values(null,0,0,1,'" + id + "')")
        #     else:
        #         cursor = connection.cursor()
        #         cursor.execute(
        #             "update feedback_count set neutral=neutral+1 where shopid='" + id + "' ")
        # elif sentiment > 0:
        #     print('The text is positive')
        #     cursor = connection.cursor()
        #     cursor.execute("select * from feedback_count where shopid='" + id + "' ")
        #     pins = cursor.fetchone()
        #     if pins == None:
        #         cursor = connection.cursor()
        #         cursor.execute("insert into feedback_count values(null,1,0,0,'" + id + "')")
        #     else:
        #         cursor = connection.cursor()
        #         cursor.execute(
        #             "update feedback_count set positive=positive+1 where shopid='" + id + "' ")
        # else:
        #     print('The text is negative')
        #     cursor = connection.cursor()
        #     cursor.execute("select * from feedback_count where shopid='" + id + "' ")
        #     pins = cursor.fetchone()
        #     if pins == None:
        #         cursor = connection.cursor()
        #         cursor.execute("insert into feedback_count values(null,0,1,0,'" + id + "')")
        #     else:
        #         cursor = connection.cursor()
        #         cursor.execute("update feedback_count set negative=negative+1 where shopid='" + id + "' ")

        return redirect('userallshops')
    else:
        return render(request,'user/add_feedback.html')


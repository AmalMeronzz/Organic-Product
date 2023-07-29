from . import views
from django.urls import path

urlpatterns = [
    path('',views.login_home,name="loginhome"),
    path('loginhome', views.login_home, name="loginhome"),
    path('login',views.login,name="login"),
    path('logout',views.logout1,name="logout"),
    path('userregistration', views.user_registration, name="userregistration"),
    path('farmerregistration/<str:id>',views.farmer_registration,name="farmerregistration"),
    path('shopregistration', views.shop_registration, name="shopregistration"),
    path('allshoplist', views.all_shop_list, name="allshoplist"),

    # admin
    # -----
    path('viewshops',views.view_shops,name="viewshops"),
    path('shopcategory/<str:id>',views.shop_category,name="shopcategory"),
    path('adminviewstock/<str:id>', views.admin_view_stock, name="adminviewstock"),
    path('adminindex', views.admin_home, name="adminindex"),
    path('newshopregistration', views.new_shop_registration, name="newshopregistration"),
    path('approvedshop', views.approved_shop, name="approvedshop"),
    path('approveshop/<str:id>', views.approve_shop, name="approveshop"),
    path('deleteshop/<str:id>', views.delete_shop, name="deleteshop"),
    path('viewfarmer/<str:id>', views.viewfarmer, name="viewfarmer"),
    path('editshop/<str:id>', views.edit_shop, name="editshop"),
    path('addcategory', views.add_category, name="addcategory"),
    path('viewcategory', views.view_category, name="viewcategory"),
    path('editcategory/<str:id>', views.edit_category, name="editcategory"),
    path('deletecategory/<str:id>', views.delete_category, name="deletecategory"),
    path('additems/<slug:id>', views.add_items, name="additems"),
    path('categoryview', views.category_view, name="categoryview"),
    path('viewitems/<str:id>', views.view_items, name="viewitems"),
    path('edititem/<str:id>', views.edit_item, name="edititem"),
    path('deleteitem/<str:id>', views.delete_item, name="deleteitem"),
    path('viewshoporder',views.view_shop_orders,name="viewshoporder"),
    path('viewshoporder',views.view_shop_orders,name="viewshoporder"),
    path('adminvieworder/<str:id>',views.admin_view_orders,name="adminvieworder"),
    path('feedbackcount',views.view_feedback_count,name="feedbackcount"),
    path('viewfeedback',views.view_feedback,name="viewfeedback"),
    # farmer
    # ------
    path('farmerindex',views.farmer_home,name="farmerindex"),
    path('categorylist',views.category_list,name="categorylist"),
    path('itemsincategory/<str:id>',views.items_in_category,name="itemsincategory"),
    path('addproduct/<str:id>',views.add_product,name="addproduct"),
    path('soldfarmerproduct',views.view_product_farmer,name="soldfarmerproduct"),
    # shop
    # ----
    path('shopindex',views.shop_home,name="shopindex"),
    path('viewnewfarmer',views.view_new_farmer,name="viewnewfarmer"),
    path('approvefarmer/<str:id>',views.approve_farmer,name="approvefarmer"),
    path('deletefarmer/<str:id>',views.delete_farmer,name="deletefarmer"),
    path('deletefarmer1/<str:id>', views.delete_farmer1, name="deletefarmer"),
    path('viewapprovedfarmer',views.view_approved_farmer,name="viewapprovedfarmer"),
    path('viewcategoryinshop',views.view_category_in_shop,name="viewcategoryinshop"),
    path('viewfarmeruploaded/<str:id>',views.view_farmer_uploaded,name="viewfarmeruploaded"),
    path('approverequest/<str:id>/<str:iditem>/<str:qty>',views.approve_request,name="approverequest"),
    path('deleterequest/<str:id>',views.delete_request,name="deleterequest"),
    path('viewproductinshop',views.view_product_in_shop,name="viewproductinshop"),
    path('deleteproduct/<str:id>',views.delete_product,name="deleteproduct"),
    path('vieworder',views.view_order,name="vieworder"),
    path('viewpayment',views.view_payment,name="viewpayment"),
    path('viewstockcategory',views.view_stock_category,name="viewstockcategory"),
    path('viewstock/<str:id>',views.view_stock,name="viewstock"),
    # user
    # ----
    path('userindex', views.user_home, name="userindex"),
    path('userallshops',views.user_all_shops,name="userallshops"),
    path('viewplace',views.view_place,name="viewplace"),
    path('viewshop/<str:id>', views.view_shop, name="viewshop"),
    path('productpage/<str:id>',views.product_page,name="productpage"),
    path('productdetails/<str:id>',views.product_details,name="productdetails"),
    path('allproducts',views.all_products,name="allproducts"),
    path('allproducts/<str:id>', views.all_product, name="allproducts"),
    path('addtocart/<str:id>/<str:iditem>/<str:idshop>',views.add_to_cart,name="addtocart"),
    path('viewcart',views.view_cart,name="viewcart"),
    path('removecart/<str:id>',views.remove_cart,name="removecart"),
    path('checkoutpage',views.check_out_page,name="checkoutpage"),
    path('makepayment',views.make_payment,name="makepayment"),
    path('myorders',views.my_orders,name="myorders"),
    path('successpage',views.success_page,name="successpage"),
    path('emptycart',views.empty_cart,name="emptycart"),
    path('addfeedback/<str:id>',views.add_feedback,name="addfeedback"),





]
from main import app
import category as ct
import tour as tr
import admin as ad
import users as us


app.add_url_rule('/ShowAllCategories', view_func=ct.showAllCategories)
app.add_url_rule("/addCategory",view_func=ct.addCategory,methods=["GET","POST"])
app.add_url_rule("/edit_cat/<cid>",view_func=ct.editCategory,methods=["GET","POST"])
app.add_url_rule("/delete_cat/<cid>",view_func=ct.deleteCategory,methods=["GET","POST"])


app.add_url_rule("/AddTour",view_func=tr.addTour,methods=["GET","POST"])
app.add_url_rule("/ShowAllTours",view_func=tr.showAllTours)
app.add_url_rule("/edit_tour/<tour_id>",view_func=tr.editTour,methods=["GET","POST"])
app.add_url_rule("/delete_tour/<tour_id>",view_func=tr.deleteTour,methods=["GET","POST"])


app.add_url_rule("/adminLogin",view_func=ad.adminlogin,methods=["GET","POST"])
app.add_url_rule("/AdminPage",view_func=ad.adminPage)
app.add_url_rule("/AdminLogout",view_func=ad.adminLogout)


app.add_url_rule("/",view_func=us.homepage)
app.add_url_rule("/showTours/<cid>",view_func=us.showTours)
app.add_url_rule("/ViewDetails/<tour>",view_func=us.ViewDetails)
app.add_url_rule("/AboutUs",view_func=us.AboutUs)
    

app.add_url_rule("/login",view_func=us.login,methods=["GET","POST"])
app.add_url_rule("/signup",view_func=us.signup,methods=["GET","POST"])
app.add_url_rule("/logout",view_func=us.logout,methods=["GET","POST"])
app.add_url_rule("/addToCart",view_func=us.addToCart,methods=["POST","GET"])
app.add_url_rule("/showCart",view_func=us.ShowCart,methods=["GET","POST"])
app.add_url_rule("/none_in_Cart",view_func=us.orderConfirm,methods=["GET","POST"])
app.add_url_rule("/MakePayment",view_func=us.MakePayment,methods=["GET","POST"])
app.add_url_rule("/orderConfirm",view_func=us.orderConfirm,methods=["GET","POST"])
app.add_url_rule("/my_bookings",view_func=us.bookings,methods=["GET","POST"])

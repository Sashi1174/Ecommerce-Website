from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopName"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="contactus"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>/", views.products, name="Productview"),
    path("checkout/", views.checkout, name="CheckOut"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    
    # ✅ Add trailing slash
    path("signup/", views.handleSignUp, name="handleSignUp"),
    path("login/", views.handleLogin, name="handleLogin"),
    path("logout/", views.handleLogout, name="handleLogout"),
]

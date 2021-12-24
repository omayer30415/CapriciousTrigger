from django.urls import path
from .import views
urlpatterns = [

    # Page views
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('choose', views.choose, name="choose"),
    path('credits', views.show_credits, name='credits'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('new_choose/<int:team_id>', views.new_choose, name='new_choose'),
    path('game', views.game, name='game'),
    path('continue', views.con, name='con'),
    path('restart', views.restart, name='restart'),
    path('progress', views.progress, name='progress'),
    path('shop', views.shop, name='shop'),


    # rest framework views
    path('rest_api/user', views.UserView.as_view(), name='user_view'),
    path('rest_api/generals', views.GeneralView.as_view(), name='generals_view'),

    # API
    path('current_user', views.current_user, name='current_user'),
    path('api/generals/<int:pk>', views.general_detail, name='general_detail'),
    path('api/promote/<int:soldier_id>', views.promote, name='promote'),
    path('api/game/gs/<int:general_id>/<int:soldier_id>',
         views.general_vs_soldier, name='general_vs_soldier'),
    path('api/game/gg/<int:general_id>/<int:g_id>',
         views.general_vs_general, name='general_vs_general'),
    path('api/game/ss/<int:soldier_id>/<int:s_id>',
         views.soldier_vs_soldier, name='soldier_vs_soldier'),
    path('api/game/sg/<int:soldier_id>/<int:general_id>',
         views.soldier_vs_general, name='soldier_vs_general'),
    path('api/game/random_attack', views.random_attack, name='random_attack'),
    path('api/game/wl', views.win_or_lose, name='win_or_lose'),
    path('api/shop/g/<int:cap_id>', views.cap_buy, name='cap_buy'),
    path('api/shop/s/<int:helmet_id>', views.helmet_buy, name='helmet_buy'),

    # Extra
    path('favicon.ico', views.fav, name='favicon.ico'),
]

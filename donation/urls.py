# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.donation_index, name='donation_index'),
# ]
# donation/urls.py

from django.urls import path
from . import views

# urlpatterns = [
#     # URL, который будет показывать форму и обрабатывать ее (method="POST")
#     # 'name'="process_donation" мы использовали в <form action="...">
#     path('donation/', views.donation_view, name='process_donation'),
#
#     # URL для страницы "Спасибо", куда мы перенаправляем
#     # path('donation/success', views.donation_success_view, name='donation_success'),
# ]


urlpatterns = [
    # URL для формы отправки (у вас уже должен быть)
    # path('donate/', views.donation_view, name='process_donation'),

    # URL для страницы "Спасибо" (у вас уже должен быть)
    # path('donate/success/', views.donation_success_view, name='donation_success'),

    # НОВЫЙ URL для списка всех донатов
    path('donations-list/', views.donation_index_view, name='donation_list'),

    # Целевые страницы после отправки формы

    path('process_donation/', views.process_donation, name='process_donation'),

    path('to_kids/', views.to_kids_view, name='to_kids'),
    path('to_animals/', views.to_animals_view, name='to_animals'),
    path('to_sick/', views.to_sick_view, name='to_sick'),
]


# from django.shortcuts import render
# from .models import Articles
#
#
# # Create your views here.
# def donation_index(request):
#     donation = Articles.objects.all()
#     # donation = Articles.objects.order_by('-id')
#     return render(request, 'donation/index.html', {'donation': donation})
#
# donation/views.py

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Articles
import uuid
from decimal import Decimal

#
# def donation_view(request: HttpRequest) -> HttpResponse:
#     # --- Обработка POST-запроса (когда пользователь отправил форму) ---
#     if request.method == 'POST':
#         try:
#             # 1. Получаем данные из 'name' атрибутов в HTML
#             category_data = request.POST.get('category')
#             amount_data = request.POST.get('amount')
#
#             # 2. Простая валидация (убедимся, что данные не пустые)
#             if not category_data or not amount_data:
#                 # Если что-то пошло не так, вернем пользователя на форму с ошибкой
#                 context = {'error': 'Пожалуйста, заполните все поля.'}
#                 return render(request, 'donation/donate_form.html', context)
#
#             # 3. Создаем объект модели
#             # Модель ожидает 'amount' как Decimal, не строку
#             # Модель требует 'operation_index', мы его сгенерируем
#             new_donation = Articles(
#                 category=category_data,
#                 amount=Decimal(amount_data),
#                 operation_index=str(uuid.uuid4())  # Генерируем уникальный ID
#             )
#
#             # 4. Сохраняем объект в базу данных
#             new_donation.save()
#
#             # 5. Перенаправляем пользователя на страницу "Успех"
#             # 'donation_success' - это 'name' URL, который мы создадим
#             return redirect('donation_success')
#
#         except (ValueError, TypeError):
#             # Ошибка, если 'amount' не получилось конвертировать в Decimal
#             context = {'error': 'Введена некорректная сумма.'}
#             return render(request, 'donation/donate_form.html', context)
#         except Exception as e:
#             # Общая ошибкаП
#             context = {'error': f'роизошла неизвестная ошибка: {e}'}
#             return render(request, 'donation/donate_form.html', context)
#
#     # --- Обработка GET-запроса (когда пользователь просто открыл страницу) ---
#     else:
#         # Просто показываем пустую форму
#         return render(request, 'donation/donate_form.html')
#

# # Отдельное View для страницы "Спасибо"
# def donation_success_view(request: HttpRequest) -> HttpResponse:
#     # Вам нужно создать шаблон 'donation/success.html'
#     return render(request, 'donation/success.html')


# donation/views.py
# ... (импорты render, redirect, Articles и т.д. у вас уже должны быть)

# ... (ваша view 'donation_view' для ОБРАБОТКИ формы остается здесь) ...

# Новая view для ПОКАЗА списка донатов
def donation_index_view(request):
    # 1. Получаем все статьи, сортируем по дате (сначала новые)
    all_donations = Articles.objects.all().order_by('-created_at')

    # 2. Передаем их в контекст
    context = {
        'donations_list': all_donations
    }

    # 3. Рендерим новый шаблон
    return render(request, 'donation/index.html', context)


from django.shortcuts import render, redirect
from django.http import HttpResponse

# Замените эти ссылки на реальные ссылки на приложение банка
BANK_LINK_KIDS = "https://messenger.online.sberbank.ru/sl/1lt9HNTDoUyTOHPpJ"
BANK_LINK_ANIMALS = "https://messenger.online.sberbank.ru/sl/1lt9HNTDoUyTOHPpJ"
BANK_LINK_SICK = "https://messenger.online.sberbank.ru/sl/1lt9HNTDoUyTOHPpJ"


def process_donation(request):
    """Обрабатывает POST-запрос из формы и перенаправляет на соответствующий URL."""
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')  # Сумма не используется для выбора страницы, но сохраняется

        if category == 'ДЕТИ':
            return redirect('to_kids')
        elif category == 'ЖИВОТНЫЕ':
            return redirect('to_animals')
        elif category == 'БОЛЬНЫЕ':
            return redirect('to_sick')
        else:
            # Опционально: обработка неверной категории или возврат на главную
            return HttpResponse("Неверная категория пожертвования.", status=400)

    # Если это GET-запрос, просто возвращаем 405 Method Not Allowed
    return HttpResponse("Этот URL принимает только POST-запросы.", status=405)


def to_kids_view(request):
    """Страница для категории 'Детям'."""
    context = {
        'title': 'Пожертвование Детям',
        'bank_link': BANK_LINK_KIDS,
        'description': 'Ваш вклад поможет детям, нуждающимся в поддержке.',
    }
    return render(request, 'donation/landing_template.html', context)


def to_animals_view(request):
    """Страница для категории 'Животным'."""
    context = {
        'title': 'Пожертвование Животным',
        'bank_link': BANK_LINK_ANIMALS,
        'description': 'Средства пойдут на помощь бездомным и брошенным животным.',
    }
    return render(request, 'donation/landing_template.html', context)


def to_sick_view(request):
    """Страница для категории 'Больным'."""
    context = {
        'title': 'Пожертвование Больным',
        'bank_link': BANK_LINK_SICK,
        'description': 'Помогите обеспечить лечение и уход тяжелобольным.',
    }
    return render(request, 'donation/landing_template.html', context)
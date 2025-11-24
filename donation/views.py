
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Articles
import uuid
from decimal import Decimal  # Обязательно для поля DecimalField

# Замените эти ссылки на реальные ссылки на приложение банка
BANK_LINK_KIDS = "https://messenger.online.sberbank.ru/sl/1lt9HNTDoUyTOHPpJ"
BANK_LINK_ANIMALS = "https://messenger.online.sberbank.ru/sl/1lt9HNTDoUyTOHPpJ"
BANK_LINK_SICK = "https://messenger.online.sberbank.ru/sl/1lt9HNTDoUyTOHPpJ"


def generate_operation_index():
    """Вспомогательная функция для генерации уникального operation_index."""
    return str(uuid.uuid4())


def process_donation(request):
    """
    Обрабатывает POST-запрос из формы:
    1. Записывает данные в таблицу Articles.
    2. Перенаправляет на соответствующую целевую страницу.
    """
    if request.method == 'POST':
        category = request.POST.get('category')
        amount_str = request.POST.get('amount')

        # --- 1. Логика сохранения данных в базу (НОВАЯ ЛОГИКА) ---
        if not category or not amount_str:
            return HttpResponse("Ошибка: Пожалуйста, выберите категорию и введите сумму.", status=400)

        try:
            # Преобразуем сумму в объект Decimal
            amount = Decimal(amount_str)

            # Создаем и сохраняем новую запись в Articles
            new_donation = Articles(
                category=category,
                amount=amount,
                operation_index=generate_operation_index()
            )
            new_donation.save()

        except (ValueError, TypeError):
            # Ошибка, если 'amount' не получилось конвертировать в Decimal
            return HttpResponse("Ошибка: Введена некорректная сумма.", status=400)
        except Exception as e:
            # Общая ошибка сохранения
            return HttpResponse(f"Произошла ошибка при сохранении данных: {e}", status=500)

        # --- 2. Логика перенаправления (Существующая логика) ---
        if category == 'ДЕТИ':
            return redirect('to_kids')
        elif category == 'ЖИВОТНЫЕ':
            return redirect('to_animals')
        elif category == 'БОЛЬНЫЕ':
            return redirect('to_sick')
        else:
            return HttpResponse("Неверная категория пожертвования.", status=400)

    # Если запрос не POST
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

def donation_index_view(request):
    # 1. Получаем все статьи, сортируем по дате (сначала новые)
    all_donations = Articles.objects.all().order_by('-created_at')

    # 2. Передаем их в контекст
    context = {
        'donations_list': all_donations
    }

    # 3. Рендерим новый шаблон
    return render(request, 'donation/index.html', context)

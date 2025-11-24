# from django.shortcuts import render
# # Импортируем функции для агрегации
# from django.db.models import Sum, Count, Avg
# # Импортируем вашу модель из приложения donation
# from donation.models import Articles
# from decimal import Decimal
#
# # Create your views here.
# # from django.http import HttpResponse
#
# # Create your views here.
# def index(request):
#     return render(request, 'main/index.html')
#
#
# def main_index_view(request):
#     # 1. Статистика для "ДЕТИ"
#     kids_stats = Articles.objects.filter(category='ДЕТИ').aggregate(
#         total_sum=Sum('amount'),
#         total_count=Count('id'),
#         avg_donation=Avg('amount')
#     )
#
#     # 2. Статистика для "ДРУГОЕ" (Животные + Больные)
#     other_stats = Articles.objects.filter(category__in=['ЖИВОТНЫЕ', 'БОЛЬНЫЕ']).aggregate(
#         total_sum=Sum('amount'),
#         total_count=Count('id'),
#         avg_donation=Avg('amount')
#     )
#
#     # 3. Статистика "ВСЕГО"
#     total_stats = Articles.objects.all().aggregate(
#         total_sum=Sum('amount'),
#         total_count=Count('id'),
#         avg_donation=Avg('amount')
#     )
#
#     # 4. Подготовка контекста для шаблона
#     # (Добавляем .get() с default=0, чтобы избежать None, если донатов нет)
#     context = {
#         'kids_sum': kids_stats.get('total_sum') or Decimal('0.00'),
#         'kids_count': kids_stats.get('total_count') or 0,
#         'kids_avg': kids_stats.get('avg_donation') or Decimal('0.00'),
#
#         'other_sum': other_stats.get('total_sum') or Decimal('0.00'),
#         'other_count': other_stats.get('total_count') or 0,
#         'other_avg': other_stats.get('avg_donation') or Decimal('0.00'),
#
#         'total_sum': total_stats.get('total_sum') or Decimal('0.00'),
#         'total_count': total_stats.get('total_count') or 0,
#         'total_avg': total_stats.get('avg_donation') or Decimal('0.00'),
#     }
#
#     return render(request, 'main/index.html', context)
from django.shortcuts import render
# Импортируем модель из другого приложения (замените 'donation' на имя вашего приложения, если оно другое)
from donation.models import Articles
from django.db.models import Sum, Count, Avg, F  # Инструменты для агрегации
from decimal import Decimal  # Для безопасных расчетов


# ... (другие импорты, если есть)

def main_index(request):
    """
    Основная функция для отображения главной страницы и статистики.
    """
    # 1. Запрос к базе данных и агрегация

    # Фильтрация по категориям, которые попадают в 'other'
    other_categories = ['ЖИВОТНЫЕ', 'БОЛЬНЫЕ']

    # 2. Агрегация данных

    # Общая статистика
    total_stats = Articles.objects.aggregate(
        total_sum=Sum('amount'),
        total_count=Count('id'),
        total_avg=Avg('amount')
    )

    # Статистика для "ДЕТИ"
    kids_stats = Articles.objects.filter(category='ДЕТИ').aggregate(
        kids_sum=Sum('amount'),
        kids_count=Count('id'),
        kids_avg=Avg('amount')
    )

    # Статистика для "ДРУГОЕ" (Животные + Больные)
    other_stats = Articles.objects.filter(category__in=other_categories).aggregate(
        other_sum=Sum('amount'),
        other_count=Count('id'),
        other_avg=Avg('amount')
    )

    # 3. Объединение результатов в контекст
    # Используем .get() для безопасного извлечения (может быть None)
    context = {
        # Общая статистика
        'total_sum': total_stats.get('total_sum') or Decimal(0),
        'total_count': total_stats.get('total_count', 0),
        'total_avg': total_stats.get('total_avg') or Decimal(0),

        # Статистика для ДЕТИ
        'kids_sum': kids_stats.get('kids_sum') or Decimal(0),
        'kids_count': kids_stats.get('kids_count', 0),
        'kids_avg': kids_stats.get('kids_avg') or Decimal(0),

        # Статистика для ДРУГОЕ
        'other_sum': other_stats.get('other_sum') or Decimal(0),
        'other_count': other_stats.get('other_count', 0),
        'other_avg': other_stats.get('other_avg') or Decimal(0),
    }

    # 4. Рендеринг шаблона (замените 'main/index.html' на ваш путь к шаблону)
    return render(request, 'main/index.html', context)
from django.shortcuts import render
# Импортируем функции для агрегации
from django.db.models import Sum, Count, Avg
# Импортируем вашу модель из приложения donation
from donation.models import Articles
from decimal import Decimal

# Create your views here.
# from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def main_index_view(request):
    # 1. Статистика для "ДЕТИ"
    kids_stats = Articles.objects.filter(category='ДЕТИ').aggregate(
        total_sum=Sum('amount'),
        total_count=Count('id'),
        avg_donation=Avg('amount')
    )

    # 2. Статистика для "ДРУГОЕ" (Животные + Больные)
    other_stats = Articles.objects.filter(category__in=['ЖИВОТНЫЕ', 'БОЛЬНЫЕ']).aggregate(
        total_sum=Sum('amount'),
        total_count=Count('id'),
        avg_donation=Avg('amount')
    )

    # 3. Статистика "ВСЕГО"
    total_stats = Articles.objects.all().aggregate(
        total_sum=Sum('amount'),
        total_count=Count('id'),
        avg_donation=Avg('amount')
    )

    # 4. Подготовка контекста для шаблона
    # (Добавляем .get() с default=0, чтобы избежать None, если донатов нет)
    context = {
        'kids_sum': kids_stats.get('total_sum') or Decimal('0.00'),
        'kids_count': kids_stats.get('total_count') or 0,
        'kids_avg': kids_stats.get('avg_donation') or Decimal('0.00'),

        'other_sum': other_stats.get('total_sum') or Decimal('0.00'),
        'other_count': other_stats.get('total_count') or 0,
        'other_avg': other_stats.get('avg_donation') or Decimal('0.00'),

        'total_sum': total_stats.get('total_sum') or Decimal('0.00'),
        'total_count': total_stats.get('total_count') or 0,
        'total_avg': total_stats.get('avg_donation') or Decimal('0.00'),
    }

    return render(request, 'main/index.html', context)
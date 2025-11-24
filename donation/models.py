from django.db import models

# Create your models here.

CATEGORY_CHOICES = (
    ('ДЕТИ', 'Дети'),
    ('ЖИВОТНЫЕ', 'Животные'),
    ('БОЛЬНЫЕ', 'Больные'),
)

class Articles(models.Model):
    """
    Модель для хранения записей о пожертвованиях.
    """

    # 1. Категория
    # Используем CharField с 'choices' для выбора одной из трех категорий.
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='ДЕТИ',
        verbose_name='Категория получателя'
    )

    # 2. Сумма
    # Используем DecimalField для точного хранения денежных сумм.
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма пожертвования'
    )

    # 3. Индекс операции
    # Используем CharField для хранения уникального идентификатора операции (например, UUID или хеша).
    operation_index = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Индекс операции'
    )

    # Дополнительное поле для удобства (не обязательно, но полезно)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )

    class Meta:
        verbose_name = 'Запись о пожертвовании'
        verbose_name_plural = 'Записи о пожертвованиях'

    def __str__(self):
        return f'{self.category} - {self.amount} руб.'

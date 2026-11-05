from django.db import models
from django.conf import settings
from django.db.models import Q, CheckConstraint


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название тега"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name


class Mercenary(models.Model):
    class Rank(models.TextChoices):
        BRONZE = 'bronze', 'Бронзовый'
        SILVER = 'silver', 'Серебряный'
        GOLD = 'gold', 'Золотой'
        DIAMOND = 'diamond', 'Алмазный'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mercenery',
        verbose_name="Пользователь"
    )

    rank = models.CharField(
        max_length=10,
        choices=Rank.choices,
        default=Rank.BRONZE,
        verbose_name="Ранг"
    )

    gold = models.PositiveIntegerField(
        default=100,
        verbose_name="Золото"
    )

    is_injured = models.BooleanField(
        default=False,
        verbose_name="Ранен"
    )

    class Meta:
        verbose_name = "Наёмник"
        verbose_name_plural = "Наёмники"

    def __str__(self):
        return f"{self.user.username} ({self.get_rank_display()} {self.gold}з)"  # type: ignore


class Monster(models.Model):
    class Danger(models.TextChoices):
        EASY = 'easy', 'простой'
        MEDIUM = 'medium', 'средний'
        HARD = 'hard', 'сложный'

    name = models.CharField(
        verbose_name="Название монстра",
        max_length=20,
    )

    description = models.CharField(
        verbose_name="Описание монстра",
        blank=True,
    )

    experience_gain = models.PositiveIntegerField(
        default=100,
        verbose_name="Опыт за победу",
    )

    danger = models.CharField(
        choices=Danger.choices,
        default=Danger.EASY,
        max_length=20,
        db_index=True,
        verbose_name="Уровень опасности",
    )

    class Meta:
        verbose_name = "Монстр"
        verbose_name_plural = "Монстры"
        ordering = ["danger"]

    def __str__(self):
        return f"[{self.get_danger_display()}] {self.name} {self.description}"  # type: ignore


class Contract(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Открыт'
        INPROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершён'

    title = models.CharField(
        max_length=100,
        verbose_name="Название контракта"
    )

    description = models.TextField(
        max_length=500,
        verbose_name="Описание контракта"
    )

    monsters = models.ManyToManyField(
        Monster,
        related_name="monsters",
        blank=True,
        verbose_name="Монстры",
    )

    reward = models.PositiveIntegerField(
        verbose_name="Награда",
    )

    status = models.CharField(
        max_length=20,
        verbose_name="Статус",
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True
    )

    assigned_to = models.ForeignKey(
        Mercenary,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contracts",
        verbose_name="Исполнитель"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="Tags",
        verbose_name="Тег",
        blank=True
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания"
        )

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ["-created_at"]
        constraints = [
            CheckConstraint(
                condition=Q(reward__gte=50),
                name="contract_reward_min_50",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "status",
                    "-created_at",
                    ],
                name="contract_status_created_index"
            )
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} - {self.reward}"  # type: ignore

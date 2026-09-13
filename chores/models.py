import secrets
import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def generate_household_code():
	alphabet = string.ascii_uppercase + string.digits
	return ''.join(secrets.choice(alphabet) for _ in range(8))


class Household(models.Model):
	name = models.CharField(max_length=120, default='Our home')
	code = models.CharField(max_length=8, unique=True, default=generate_household_code)
	timezone = models.CharField(max_length=64, default='UTC')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.name} ({self.code})'


class Partner(models.Model):
	household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='partners')
	display_name = models.CharField(max_length=80)
	avatar_color = models.CharField(max_length=7, default='#245c52')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']
		constraints = [
			models.UniqueConstraint(fields=['household', 'display_name'], name='unique_partner_name_per_household'),
		]

	def __str__(self):
		return self.display_name


class Chore(models.Model):
	class Frequency(models.TextChoices):
		ONCE = 'once', 'One time'
		DAILY = 'daily', 'Daily'
		WEEKLY = 'weekly', 'Weekly'
		MONTHLY = 'monthly', 'Monthly'

	household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='chores')
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.WEEKLY)
	due_date = models.DateField()
	effort = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
	is_shared = models.BooleanField(default=False)
	assigned_to = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_chores')
	completed_at = models.DateTimeField(null=True, blank=True)
	completed_by = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_chores')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['completed_at', 'due_date', 'title']

	@property
	def is_overdue(self):
		from django.utils import timezone
		return self.completed_at is None and self.due_date < timezone.localdate()

	def __str__(self):
		return self.title

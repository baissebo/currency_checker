from django.db import models


class CurrencyRate(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Временная метка")
    usd_to_rub = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс доллара к рублю")

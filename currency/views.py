from datetime import timedelta
import requests
from django.http import JsonResponse
from django.utils import timezone

from currency.models import CurrencyRate


def get_current_usd(request):
    last_entry = CurrencyRate.objects.order_by("-timestamp").first()

    if last_entry:
        if (timezone.now() - last_entry.timestamp) < timedelta(seconds=10):
            return JsonResponse({"error": "Еще не прошло 10 секунд, подождите."}, status=429)

    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

    if response.status_code == 200:
        data = response.json()
        usd_to_rub = data["rates"]["RUB"]

        CurrencyRate.objects.create(usd_to_rub=usd_to_rub)

        last_rates = CurrencyRate.objects.order_by("-timestamp")[:10]
        rates = [{"timestamp": rate.timestamp, "usd_to_rub": str(rate.usd_to_rub)} for rate in last_rates]

        return JsonResponse({"current_usd_to_rub": str(usd_to_rub), "last_rates": rates})

    return JsonResponse({"error": "Не удалось получить курсы валют"}, status=500)

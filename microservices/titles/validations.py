from datetime import datetime

from django.core.exceptions import ValidationError


def validate_not_future_year(value):
    year_now = datetime.today()
    if value <= year_now.year:
        return value
    else:
        raise ValidationError("Этот фильм еще не вышел, "
                              "чтобы добавить его в базу")

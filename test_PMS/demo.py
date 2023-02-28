from datetime import date, datetime


def test_get_time():
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = date.today()
    print(today)


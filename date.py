from datetime import datetime
from pytz import timezone
format = "%Y-%m-%d %H:%M:%S"
format2 = "%H:%M"
#  time in UTC
now_utc = datetime.now(timezone('UTC'))
# Convert to Asia/Kolkata time zone
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
print(now_asia.strftime(format2))

today3pm = now_asia.replace(hour=15, minute=30)
if(now_asia < today3pm):
    print(now_asia.strftime(format2))   
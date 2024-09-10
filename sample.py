import time
import pytz  
from datetime import datetime

dt = datetime.now()
timezone_ind= pytz.timezone('Asia/Kolkata')  
ist_local = timezone_ind.localize(datetime.now())  
print("Indian Standard Time:", ist_local.strftime("%d/%m/%Y, %H:%M:%S"))

print(dt.strftime("%d/%m/%Y"))
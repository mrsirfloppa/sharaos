import datetime

def run(sharaos, *args):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"The current time is: {current_time}")
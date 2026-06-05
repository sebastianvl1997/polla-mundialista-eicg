from datetime import datetime

def is_locked(lock_time):

    now = datetime.now()

    lock_dt = datetime.strptime(
        lock_time,
        "%Y-%m-%d %H:%M:%S"
    )

    return now >= lock_dt
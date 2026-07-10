def add_time(start, duration, starting_day=None):
    start_part = start.split()
    start_time = start_part[0]
    am_pm = start_part[1]

    start_hr = int(start_time.split(":")[0])
    start_min = int(start_time.split(":")[1])

    dur_hr = int(duration.split(":")[0])
    dur_min = int(duration.split(":")[1])

    hour = start_hr + dur_hr
    minute = start_min + dur_min

    hour += minute // 60
    minute = minute % 60

    final_hr = hour % 12
    if final_hr == 0:
        final_hr = 12

    final_min = str(minute).zfill(2)

    am_pm_flips = hour // 12

    days_added = 0
    if am_pm == "AM":
        days_added = am_pm_flips // 2
    else:
        days_added = (am_pm_flips + 1) // 2

    if am_pm_flips % 2 == 1:
        if am_pm == "AM":
            am_pm = "PM"
        else:
            am_pm = "AM"

    new_Time = f"{final_hr}:{final_min} {am_pm}"

    if starting_day != None:
        days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = starting_day.lower().capitalize()
        index_day_list = (days_list.index(day) + days_added) % 7
        new_day = days_list[index_day_list]
        new_Time += f", {new_day}"

    if days_added == 1:
        new_Time += " (next day)"
    elif days_added > 1:
        new_Time += f" ({days_added} days later)"

    return new_Time

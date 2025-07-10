import json


def create_timetable():
    days_input = input("Enter days separated by commas (e.g., Monday,Tuesday,Wednesday): ")
    days = [d.strip() for d in days_input.split(',') if d.strip()]
    while True:
        try:
            periods = int(input("Enter number of periods per day: "))
            if periods <= 0:
                print("Please enter a positive integer")
                continue
            break
        except ValueError:
            print("Invalid number. Try again.")

    timetable = {day: {} for day in days}

    for day in days:
        print(f"--- {day} ---")
        for period in range(1, periods + 1):
            subject = input(f"  Period {period}: ")
            timetable[day][f"Period {period}"] = subject

    return timetable


def save_timetable(timetable, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(timetable, f, ensure_ascii=False, indent=2)
    print(f"Timetable saved to {filename}")


def print_timetable(timetable):
    days = list(timetable.keys())
    periods = sorted(next(iter(timetable.values())).keys())
    header = ["Day"] + periods
    row_sep = "+".join(["-" * 15 for _ in header])
    print(row_sep)
    print("|" + "|".join(h.center(15) for h in header) + "|")
    print(row_sep)
    for day in days:
        row = [day] + [timetable[day].get(p, "") for p in periods]
        print("|" + "|".join(str(col).center(15) for col in row) + "|")
        print(row_sep)


def main():
    timetable = create_timetable()
    print_timetable(timetable)
    if input("Save timetable to file? (y/n): ").lower() == 'y':
        filename = input("Filename (default timetable.json): ") or "timetable.json"
        save_timetable(timetable, filename)


if __name__ == "__main__":
    main()

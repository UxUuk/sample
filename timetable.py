import json
from itertools import cycle

PERIODS = ["E", "S", "A", "B", "C"]
MAX_STUDENTS_PER_TEACHER = 2


def create_schedule():
    days_input = input("Enter days separated by commas (e.g., Mon,Tue): ")
    days = [d.strip() for d in days_input.split(',') if d.strip()]
    teachers_input = input("Enter teacher names separated by commas: ")
    teachers = [t.strip() for t in teachers_input.split(',') if t.strip()]
    students_input = input("Enter student names separated by commas: ")
    students = [s.strip() for s in students_input.split(',') if s.strip()]

    # Prepare an endless cycle of student pairs
    pairs = []
    for i in range(0, len(students), MAX_STUDENTS_PER_TEACHER):
        pairs.append(students[i:i + MAX_STUDENTS_PER_TEACHER])
    if not pairs:
        pairs.append([])
    pair_cycle = cycle(pairs)

    schedule = {day: {p: {} for p in PERIODS} for day in days}
    for day in days:
        for period in PERIODS:
            for teacher in teachers:
                schedule[day][period][teacher] = list(next(pair_cycle))
    return schedule


def save_schedule(schedule, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(f"Schedule saved to {filename}")


def print_schedule(schedule):
    for day, periods in schedule.items():
        print(f"=== {day} ===")
        for period in PERIODS:
            print(f"[{period}]")
            for teacher, students in schedule[day][period].items():
                student_names = ', '.join(students) if students else '---'
                print(f"  {teacher}: {student_names}")
        print()


def main():
    schedule = create_schedule()
    print_schedule(schedule)
    if input("Save schedule to file? (y/n): ").lower() == 'y':
        filename = input("Filename (default schedule.json): ") or "schedule.json"
        save_schedule(schedule, filename)


if __name__ == "__main__":
    main()

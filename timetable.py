import json
from typing import List, Dict
from collections import defaultdict

from openpyxl import load_workbook

PERIODS = ["E", "S", "A", "B", "C"]
MAX_STUDENTS_PER_TEACHER = 2


class Teacher:
    def __init__(self, name: str, periods: List[str], subjects: List[str]):
        self.name = name
        self.periods = [p.strip() for p in periods if p.strip() in PERIODS]
        self.subjects = [s.strip() for s in subjects if s.strip()]


class Student:
    def __init__(self, name: str, periods: List[str], count: int, subject: str):
        self.name = name
        self.periods = [p.strip() for p in periods if p.strip() in PERIODS]
        self.count = int(count)
        self.subject = subject.strip()


def load_teachers(filename: str) -> List[Teacher]:
    wb = load_workbook(filename)
    ws = wb.active
    teachers = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        name = str(row[0]).strip()
        periods = str(row[1]).split(',') if row[1] else []
        subjects = str(row[2]).split(',') if row[2] else []
        teachers.append(Teacher(name, periods, subjects))
    return teachers


def load_students(filename: str) -> List[Student]:
    wb = load_workbook(filename)
    ws = wb.active
    students = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        name = str(row[0]).strip()
        periods = str(row[1]).split(',') if row[1] else []
        count = int(row[2]) if row[2] else 0
        subject = str(row[3]) if row[3] else ''
        students.append(Student(name, periods, count, subject))
    return students


def create_schedule(teachers: List[Teacher], students: List[Student]) -> Dict[str, Dict[str, List[str]]]:
    schedule: Dict[str, Dict[str, List[str]]] = {p: {} for p in PERIODS}
    # place teachers
    for teacher in teachers:
        for period in teacher.periods:
            schedule[period][teacher.name] = []
    # assign students
    for student in students:
        assigned = 0
        for period in student.periods:
            if assigned >= student.count:
                break
            # find teacher for subject with room
            for teacher in teachers:
                if period not in teacher.periods:
                    continue
                if student.subject not in teacher.subjects:
                    continue
                current = schedule[period].setdefault(teacher.name, [])
                if len(current) < MAX_STUDENTS_PER_TEACHER:
                    current.append(student.name)
                    assigned += 1
                    break
    return schedule


def print_schedule(schedule: Dict[str, Dict[str, List[str]]]):
    for period in PERIODS:
        print(f"[{period}]")
        if period not in schedule or not schedule[period]:
            print("  (no teachers)")
            continue
        for teacher, students in schedule[period].items():
            student_names = ', '.join(students) if students else '---'
            print(f"  {teacher}: {student_names}")
        print()


def save_schedule(schedule: Dict[str, Dict[str, List[str]]], filename: str = 'schedule.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(f"Schedule saved to {filename}")


def main():
    teachers = load_teachers('teachers.xlsx')
    students = load_students('students.xlsx')
    schedule = create_schedule(teachers, students)
    print_schedule(schedule)
    save_schedule(schedule)


if __name__ == '__main__':
    main()

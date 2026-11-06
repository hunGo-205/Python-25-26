import math
import numpy as np
import curses


class Course:
    def __init__(self, course_id, name, credit):
        self.id = course_id
        self.name = name
        self.credit = credit


class Student:
    def __init__(self, student_id, name, dob):
        self.id = student_id
        self.name = name
        self.dob = dob
        self.marks = {}  # {course_id: mark}
        self.gpa = 0.0

    def add_mark(self, course_id, mark):
        # Round-down score to 1-digit decimal using math.floor
        self.marks[course_id] = math.floor(mark * 10.0) / 10.0

    def calculate_gpa(self, courses_dict):
        if not self.marks:
            self.gpa = 0.0
            return 0.0

        marks_list = []
        credits_list = []

        for course_id, mark in self.marks.items():
            if course_id in courses_dict:
                marks_list.append(mark)
                credits_list.append(courses_dict[course_id].credit)

        if not credits_list or sum(credits_list) == 0:
            self.gpa = 0.0
            return 0.0

        # Calculate weighted average using NumPy arrays
        marks_array = np.array(marks_list)
        credits_array = np.array(credits_list)

        weighted_sum = np.sum(marks_array * credits_array)
        total_credits = np.sum(credits_array)

        self.gpa = float(weighted_sum / total_credits)
        return self.gpa


class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.courses = {}

    def add_student(self, student):
        self.students.append(student)

    def add_course(self, course):
        self.courses[course.id] = course

    def update_all_gpas(self):
        for student in self.students:
            student.calculate_gpa(self.courses)

    def sort_students_by_gpa(self):
        self.update_all_gpas()
        # Sort student list in descending order by GPA
        self.students.sort(key=lambda s: s.gpa, reverse=True)


# --- Curses UI Helper Functions ---

def draw_header(stdscr, title):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(1, 2, f"=== {title} ===", curses.A_BOLD | curses.A_UNDERLINE)


def get_input_str(stdscr, prompt, y, x):
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    curses.echo()
    input_bytes = stdscr.getstr(y, x + len(prompt))
    curses.noecho()
    return input_bytes.decode('utf-8').strip()


def display_message(stdscr, message, y=18, x=2):
    stdscr.addstr(y, x, message, curses.A_BOLD)
    stdscr.addstr(y + 1, x, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()


# --- Curses Main Application Loop ---

def main_curses(stdscr, sms):
    curses.curs_set(1)

    while True:
        draw_header(stdscr, "STUDENT MARK MANAGEMENT SYSTEM")
        stdscr.addstr(3, 4, "1. Input Student Information")
        stdscr.addstr(4, 4, "2. Input Course Information")
        stdscr.addstr(5, 4, "3. Input Marks for Course")
        stdscr.addstr(6, 4, "4. List Courses")
        stdscr.addstr(7, 4, "5. List Students & Calculated GPAs (Sorted Descending)")
        stdscr.addstr(8, 4, "6. Exit")

        choice = get_input_str(stdscr, "Select an option (1-6): ", 10, 4)

        if choice == '1':
            draw_header(stdscr, "INPUT STUDENTS")
            num_str = get_input_str(stdscr, "Enter number of students: ", 3, 2)
            try:
                num = int(num_str)
                for i in range(num):
                    stdscr.addstr(5 + i * 4, 2, f"--- Student {i + 1} ---", curses.A_BOLD)
                    sid = get_input_str(stdscr, "ID: ", 6 + i * 4, 2)
                    sname = get_input_str(stdscr, "Name: ", 7 + i * 4, 2)
                    sdob = get_input_str(stdscr, "DoB (DD/MM/YYYY): ", 8 + i * 4, 2)
                    sms.add_student(Student(sid, sname, sdob))
                display_message(stdscr, "Students added successfully!")
            except ValueError:
                display_message(stdscr, "Invalid number entered.")

        elif choice == '2':
            draw_header(stdscr, "INPUT COURSES")
            num_str = get_input_str(stdscr, "Enter number of courses: ", 3, 2)
            try:
                num = int(num_str)
                for i in range(num):
                    stdscr.addstr(5 + i * 4, 2, f"--- Course {i + 1} ---", curses.A_BOLD)
                    cid = get_input_str(stdscr, "Course ID: ", 6 + i * 4, 2)
                    cname = get_input_str(stdscr, "Course Name: ", 7 + i * 4, 2)
                    credit = float(get_input_str(stdscr, "Credits: ", 8 + i * 4, 2))
                    sms.add_course(Course(cid, cname, credit))
                display_message(stdscr, "Courses added successfully!")
            except ValueError:
                display_message(stdscr, "Invalid input value.")

        elif choice == '3':
            draw_header(stdscr, "INPUT MARKS")
            if not sms.courses:
                display_message(stdscr, "No courses available. Please add courses first.")
                continue
            if not sms.students:
                display_message(stdscr, "No students available. Please add students first.")
                continue

            cid = get_input_str(stdscr, "Enter Course ID to input marks for: ", 3, 2)
            if cid not in sms.courses:
                display_message(stdscr, f"Course ID '{cid}' not found.")
                continue

            y_offset = 5
            for student in sms.students:
                mark_str = get_input_str(
                    stdscr, f"Mark for {student.name} ({student.id}): ", y_offset, 2
                )
                try:
                    raw_mark = float(mark_str)
                    student.add_mark(cid, raw_mark)
                except ValueError:
                    student.add_mark(cid, 0.0)
                y_offset += 1

            display_message(stdscr, "Marks recorded (rounded down to 1 decimal place)!")

        elif choice == '4':
            draw_header(stdscr, "COURSE LIST")
            if not sms.courses:
                stdscr.addstr(3, 2, "No courses found.")
            else:
                stdscr.addstr(3, 2, f"{'ID':<10} {'Course Name':<25} {'Credits':<10}", curses.A_BOLD)
                row = 4
                for c in sms.courses.values():
                    stdscr.addstr(row, 2, f"{c.id:<10} {c.name:<25} {c.credit:<10.1f}")
                    row += 1
            display_message(stdscr, "", y=18, x=2)

        elif choice == '5':
            draw_header(stdscr, "STUDENT GPA LIST (SORTED DESCENDING)")
            if not sms.students:
                stdscr.addstr(3, 2, "No students found.")
            else:
                sms.sort_students_by_gpa()
                stdscr.addstr(3, 2, f"{'ID':<10} {'Name':<20} {'DoB':<12} {'GPA':<8}", curses.A_BOLD)
                row = 4
                for student in sms.students:
                    stdscr.addstr(
                        row, 2,
                        f"{student.id:<10} {student.name:<20} {student.dob:<12} {student.gpa:<8.2f}"
                    )
                    row += 1
            display_message(stdscr, "", y=18, x=2)

        elif choice == '6':
            break


def main():
    sms = StudentManagementSystem()
    curses.wrapper(main_curses, sms)


if __name__ == "__main__":
    main()
import os
import pickle
import gzip
import threading
import time

class StudentManagementSystem:
    def __init__(self):
        self.students = []  # List of students
        self.courses = []   # List of courses
        self.marks = {}     # Mark sheet: {student_id: {course_id: mark}}

    # 1. INPUT FUNCTIONS
    def input_students(self):
        n = int(input("Enter number of students to add: "))
        for _ in range(n):
            student_id = input("  - Enter Student ID: ")
            name = input("  - Enter Student Name: ")
            dob = input("  - Enter Date of Birth (DD/MM/YYYY): ")
            self.students.append({'id': student_id, 'name': name, 'dob': dob})
        print("-> Students added successfully!\n")

    def input_courses(self):
        n = int(input("Enter number of courses to add: "))
        for _ in range(n):
            course_id = input("  - Enter Course ID: ")
            title = input("  - Enter Course Title: ")
            self.courses.append({'id': course_id, 'title': title})
        print("-> Courses added successfully!\n")

    def input_marks(self):
        if not self.students or not self.courses:
            print("(!) You need at least 1 student and 1 course before entering marks.\n")
            return

        print("\n--- SELECT A COURSE TO ENTER MARKS ---")
        for i, c in enumerate(self.courses):
            print(f"{i + 1}. {c['title']} (ID: {c['id']})")
        
        choice = int(input("Select course number: ")) - 1
        selected_course = self.courses[choice]['id']

        for s in self.students:
            mark = float(input(f"  - Enter mark for student {s['name']} (ID: {s['id']}): "))
            if s['id'] not in self.marks:
                self.marks[s['id']] = {}
            self.marks[s['id']][selected_course] = mark
        print("-> Marks recorded successfully!\n")

    # 2. BACKGROUND THREAD PERSISTENCE (PICKLE + GZIP)
    def _save_data_worker(self, filepath, data_snapshot):
        try:
            with gzip.open(filepath, 'wb') as f:
                pickle.dump(data_snapshot, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"\n[Background Thread] Successfully saved data to '{filepath}'!")
        except Exception as e:
            print(f"\n[Background Thread] Error saving data: {e}")

    def save_data_in_background(self, filepath="students_data.pkl.gz"):
        data_snapshot = {
            'students': list(self.students),
            'courses': list(self.courses),
            'marks': dict(self.marks)
        }
        save_thread = threading.Thread(
            target=self._save_data_worker,
            args=(filepath, data_snapshot),
            daemon=True
        )
        save_thread.start()
        print("[Main Thread] Saving data in the background...")

    def load_data(self, filepath="students_data.pkl.gz"):
        if not os.path.exists(filepath):
            print(f"No existing data file '{filepath}' found.\n")
            return

        try:
            with gzip.open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.students = data.get('students', [])
                self.courses = data.get('courses', [])
                self.marks = data.get('marks', {})
            print(f"-> Data successfully loaded from '{filepath}'!\n")
        except Exception as e:
            print(f"Error loading data: {e}\n")


# 3. INTERACTIVE MENU
if __name__ == "__main__":
    system = StudentManagementSystem()
    
    # Auto-load existing data on startup
    system.load_data()

    while True:
        print("================ MENU ================")
        print("1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. Save data (Background Thread)")
        print("0. Exit")
        print("======================================")
        
        choice = input("Your choice: ")

        if choice == '1':
            system.input_students()
        elif choice == '2':
            system.input_courses()
        elif choice == '3':
            system.input_marks()
        elif choice == '4':
            system.save_data_in_background()
            time.sleep(0.5)
        elif choice == '0':
            system.save_data_in_background()
            time.sleep(1)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again!\n")
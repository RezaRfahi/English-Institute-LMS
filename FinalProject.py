from datetime import datetime

def get_student_info():
    code = input("Enter student code: ")
    name = input("Enter student name: ")
    family = input("Enter student family: ")
    birth_date = input("Enter student birth date (YYYY-MM-DD): ")

    return {'code': code, 'name': name, 'family': family, 'birth_date': birth_date, 'level': None, 'grades': []}

def save_student_info(student_info, file_path):
    with open(file_path, 'a') as file:
        file.write(f"{student_info['code']}, {student_info['name']}, {student_info['family']}, {student_info['birth_date']}, {student_info['level']}, {','.join(map(str, student_info['grades']))}\n")

def get_student_grades():
    grade = int(input("Enter student's grade (0-100): "))
    return grade

def save_student_grades(student_info, grade, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    student_exists = any(student_info['code'] in line for line in lines)

    if student_exists:
        new_lines = [f"{student_info['code']}, {student_info['name']}, {student_info['family']}, {student_info['birth_date']}, {student_info['level']}, {','.join(map(str, student_info['grades'] + [grade]))}\n" if student_info['code'] in line else line for line in lines]
    else:
        new_lines = [f"{student_info['code']}, {student_info['name']}, {student_info['family']}, {student_info['birth_date']}, {student_info['level']}, {','.join(map(str, student_info['grades'] + [grade]))}\n"] + lines

    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def search_student_by_code(code, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            if code == parts[0]:
                return {'code': parts[0], 'name': parts[1], 'family': parts[2], 'birth_date': parts[3], 'level': parts[4], 'grades': list(map(int, parts[5:]))}

    return None

def calculate_min_max_grades(level, file_path):
    min_grade = float('inf') 
    max_grade = float('-inf')  
    min_student_info = None
    max_student_info = None

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            if len(parts) >= 6 and parts[4] == level: 
                student_info = {'code': parts[0], 'name': parts[1], 'family': parts[2], 'birth_date': parts[3], 'level': parts[4], 'grades': list(map(int, parts[5:]))}
                grade = student_info['grades'][-1]

                if grade < min_grade:
                    min_grade = grade
                    min_student_info = student_info
                if grade > max_grade:
                    max_grade = grade
                    max_student_info = student_info

    if min_student_info is not None and max_student_info is not None:
        print(f"\nMinimum Grade: {min_grade} (Student: {min_student_info['name']} {min_student_info['family']})")
        print(f"Maximum Grade: {max_grade} (Student: {max_student_info['name']} {max_student_info['family']})")
    else:
        print(f"No students found in Level {level}.")

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            print(f"Invalid date format: {date_str}")
            return datetime(1900, 1, 1)

def display_students(level, file_path):
    students_info = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            if len(parts) >= 5 and parts[4] == level:
                student_info = {'code': parts[0], 'name': parts[1], 'family': parts[2], 'birth_date': parts[3], 'level': parts[4], 'grades': list(map(int, parts[5:]))}
                students_info.append(student_info)

    if not students_info:
        print(f"No students found in Level {level}.")
        return

    print(f"List of Students in Level {level} (Sorted by Birthdate - Descending):")
    students_info.sort(key=lambda x: parse_date(x['birth_date']), reverse=True)
    for student in students_info:
        print(f"{student['name']} - {student['family']} - {student['birth_date']} - {student['level']} - {','.join(map(str, student['grades']))}")


def main_menu():
    print("\n*** English Learning Institute Management System ***")
    print("1. Enter Student Information")
    print("2. Search Student by Code")
    print("3. Display All Students (Sorted by Birthdate)")
    print("4. Calculate Min and Max Grades")
    print("5. Exit")

    choice = input("Select an option (1-5): ")
    return choice

def main():
    while True:
        choice = main_menu()

        if choice == '1':
            level = input("Enter student level (A to E): ").upper()

            if level not in ['A', 'B', 'C', 'D', 'E']:
                print("Invalid level. Please enter a valid level (A to E).")
                continue

            new_info = get_student_info()
            new_info['level'] = level
            save_student_info(new_info, "students_info.txt")

            grade = get_student_grades()
            save_student_grades(new_info, grade, "students_info.txt")

        elif choice == '2':
            code_to_search = input("Enter student code to search: ")

            student_info = search_student_by_code(code_to_search, "students_info.txt")

            if student_info:
                print(f"Student Information: {student_info}")
            else:
                print(f"Student with code {code_to_search} not found.")

        elif choice == '3':
            level_to_display = input("Enter the level to display (A to E): ").upper()
            file_path_to_display = "students_info.txt"
            display_students(level_to_display, file_path_to_display)

        elif choice == '4':
            level_to_calculate = input("Enter the level to calculate min and max grades (A to E): ").upper()
            file_path_to_calculate = "students_info.txt"
            calculate_min_max_grades(level_to_calculate, file_path_to_calculate)

        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


main()

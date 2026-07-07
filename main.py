class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in self.courses_in_progress and
                course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _average_hw_grade(self):

        all_grades = [g for course_grades in self.grades.values() for g in course_grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg = self._average_hw_grade()
        in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else ''
        finished = ', '.join(self.finished_courses) if self.finished_courses else ''
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg:.1f}\n"
                f"Курсы в процессе изучения: {in_progress}\n"
                f"Завершенные курсы: {finished}")

    def __lt__(self, other):
        if isinstance(other, Student):
            return self._average_hw_grade() < other._average_hw_grade()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Student):
            return self._average_hw_grade() <= other._average_hw_grade()
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Student):
            return self._average_hw_grade() == other._average_hw_grade()
        return NotImplemented


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_lecture_grade(self):

        all_grades = [g for course_grades in self.grades.values() for g in course_grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg = self._average_lecture_grade()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg:.1f}")

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self._average_lecture_grade() < other._average_lecture_grade()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Lecturer):
            return self._average_lecture_grade() <= other._average_lecture_grade()
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Lecturer):
            return self._average_lecture_grade() == other._average_lecture_grade()
        return NotImplemented


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"



def average_hw_grade_by_course(students, course_name):

    total = 0
    count = 0
    for student in students:
        if course_name in student.grades:
            total += sum(student.grades[course_name])
            count += len(student.grades[course_name])
    return total / count if count else 0


def average_lecture_grade_by_course(lecturers, course_name):

    total = 0
    count = 0
    for lecturer in lecturers:
        if course_name in lecturer.grades:
            total += sum(lecturer.grades[course_name])
            count += len(lecturer.grades[course_name])
    return total / count if count else 0



student1 = Student('Алексей', 'Смирнов', 'М')
student2 = Student('Мария', 'Иванова', 'Ж')
lecturer1 = Lecturer('Иван', 'Сергеев')
lecturer2 = Lecturer('Елена', 'Петрова')
reviewer1 = Reviewer('Пётр', 'Николаев')
reviewer2 = Reviewer('Ольга', 'Васильева')


student1.courses_in_progress += ['Python', 'Git']
student2.courses_in_progress += ['Python', 'Java']
student1.finished_courses += ['Введение в программирование']
student2.finished_courses += ['Алгоритмы']

lecturer1.courses_attached += ['Python', 'Git']
lecturer2.courses_attached += ['Python', 'Java']

reviewer1.courses_attached += ['Python', 'Git']
reviewer2.courses_attached += ['Python', 'Java']


reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student2, 'Python', 7)
reviewer2.rate_hw(student2, 'Java', 9)

student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Python', 9)
student2.rate_lecture(lecturer2, 'Python', 8)
student2.rate_lecture(lecturer2, 'Python', 7)


print('Студенты')
print(student1)
print(student2)
print()
print(' Лекторы')
print(lecturer1)
print(lecturer2)
print()
print('Проверяющие ')
print(reviewer1)
print(reviewer2)
print()


print('Сравнение студентов:')
print('student1 < student2?', student1 < student2)  # 9.0 < 8.0? False
print('student1 > student2?', student1 > student2)  # True
print()
print('Сравнение лекторов:')
print('lecturer1 < lecturer2?', lecturer1 < lecturer2) # 9.5 < 7.5? False
print('lecturer1 == lecturer1?', lecturer1 == lecturer1) # True
print()


print('Средняя оценка за ДЗ по курсу Python:', average_hw_grade_by_course([student1, student2], 'Python'))
print('Средняя оценка за ДЗ по курсу Java:', average_hw_grade_by_course([student1, student2], 'Java'))
print('Средняя оценка за лекции по курсу Python:', average_lecture_grade_by_course([lecturer1, lecturer2], 'Python'))
print('Средняя оценка за лекции по курсу Git:', average_lecture_grade_by_course([lecturer1, lecturer2], 'Git'))

print('Проверка ошибок:')

res1 = reviewer1.rate_hw(lecturer1, 'Python', 10)
print('reviewer1 оценивает лектора:', res1)

res2 = student1.rate_lecture(reviewer1, 'Python', 10)
print('student1 оценивает проверяющего:', res2)

res3 = reviewer1.rate_hw(student2, 'Java', 10)
print('reviewer1 оценивает student2 за Java (чужой курс):', res3)

res4 = student1.rate_lecture(lecturer2, 'Java', 10)
print('student1 оценивает лектора за Java (не изучает):', res4)
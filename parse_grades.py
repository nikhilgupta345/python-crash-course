def create_empty_grades_dict():
  grades_dict = {
    'A+': 0,
    'A': 0,
    'A-': 0,
    'B+': 0,
    'B': 0,
    'B-': 0,
    'C+': 0,
    'C': 0,
    'C-': 0,
    'D+': 0,
    'D': 0,
    'D-': 0,
    'F': 0
  }

  return grades_dict

def read_grades_file(filename):
  course_to_grades = {}
  with open(filename, 'r') as f:
    lines = f.readlines()
    headers = lines[0].split(',')
    header_grades_keys = headers[-17:-4]
    lines = lines[1:] # Remove first line that has the header information
    for line in lines:
      values = line.split(',')
      subject = values[4]
      number = values[5]
      combined = '{}{}'.format(subject, number)

      if combined not in course_to_grades:
        course_to_grades[combined] = create_empty_grades_dict()

      grades = values[-17:-4]
      for i in range(len(header_grades_keys)):
        key = header_grades_keys[i]
        if grades[i]:
          course_to_grades[combined][key] += int(grades[i])

  return course_to_grades

def calculate_avg_gpas(course_to_grades):
  grades_to_points = {
    'A+': 4.0,
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'D-': 0.7,
    'F': 0
  }

  course_to_gpa = {}
  for course in course_to_grades:
    total_students = 0 # Need to know total number of students to calculate average
    total_points = 0
    for grade in course_to_grades[course]: # Loop through A+, A-, etc.
      total_students += course_to_grades[course][grade]
      total_points += course_to_grades[course][grade] * grades_to_points[grade]

    if total_students != 0:
      course_to_gpa[course] = (total_points / total_students)
    else:
      course_to_gpa[course] = 'N/A'

  return course_to_gpa

def output_avg_to_file(course_to_gpa, filename):
  with open(filename, 'w') as f:
    for course in course_to_gpa:
      val = '{},{}\n'.format(course, course_to_gpa[course])
      print(val)
      f.write(val)

grades = read_grades_file('grades.txt')
course_to_avg_gpa = calculate_avg_gpas(grades)
output_avg_to_file(course_to_avg_gpa, 'output.txt')
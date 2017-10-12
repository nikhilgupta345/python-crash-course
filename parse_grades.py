# This program takes in an input file of grades, and parses
# them to figure out the average GPA of each course.

def create_empty_grades_dict():
  """Create an empty grades dictionary and return
    it for another function to use"""
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
  """Takes in a filename and aggregates all of the grades
    information into the format talked about in the crash course.
    course_to_grades = {
      'CS2110': {
        'A+': 10,
        'A': 4,
        ...
      },
      'APMA1110': {
        ...
      },
      ...
    }
  """

  course_to_grades = {}
  with open(filename, 'r') as f: # open the file in read mode
    lines = f.readlines() # read all the lines
    lines = lines[1:] # Skip the first header line by taking a subset of the list
    for line in lines:
      values = line.split(',') # individual values in a list by splitting the line
      subject = values[4] # subject and num are the 5th and 6th elements
      number = values[5] # subject is 'CS' and number is '2110'
      combined = '{}{}'.format(subject, number) # combine them to get 'CS2110' for example

      # if the key is not already in the dict then we need
      # to create the empty grades dict associated with that course
      # using the function defined earlier that returns an empty grades dict
      if combined not in course_to_grades:
        course_to_grades[combined] = create_empty_grades_dict()

      # Here we can add to the current number of A+, A, etc.
      # using the int() function to convert the string from the
      # file to an integer that we can add with.
      # Note that some of these values may be invalid
      # so one thing we can do is use a try/except, which will allow
      # us to run some function, and then 'except' (or do something when
      # an exception/error occurs)
      try:
        # so we're going to try all of this code (and if it works, then good)
        course_to_grades[combined]['A+'] += int(values[9])
        course_to_grades[combined]['A'] += int(values[10])
        course_to_grades[combined]['A-'] += int(values[11])
        course_to_grades[combined]['B+'] += int(values[12])
        course_to_grades[combined]['B'] += int(values[13])
        course_to_grades[combined]['B-'] += int(values[14])
        course_to_grades[combined]['C+'] += int(values[15])
        course_to_grades[combined]['C'] += int(values[16])
        course_to_grades[combined]['C-'] += int(values[17])
        course_to_grades[combined]['D+'] += int(values[18])
        course_to_grades[combined]['D'] += int(values[19])
        course_to_grades[combined]['D-'] += int(values[20])
        course_to_grades[combined]['F'] += int(values[21])
      except: # but if something goes wrong and an error occurs
        # (maybe if any of the values are empty with bad input data),
        # we can just use 'continue' to move onto the next iteration
        # of the loop, which is the next line in the file
        continue

  # Now that we've gone through all lines in the file and
  # aggregated all the grades data in the format we want,
  # we can now return it to the function who called this.
  return course_to_grades

# This is a function that takes in a course_to_grades dict (like
# we defined above) and returns a dictionary that maps a coursename
# to its GPA in the form:
# course_to_gpa = {
#    'CS2110': 3.6,
#    'APMA1110': 3.3,
#    ...
# }
def calculate_avg_gpas(course_to_grades):

  # first associate each grade with its GPA
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
  # We need to loop through every course in the passed in dictionary
  # (which is the huge dict of all grade frequencies for each course)
  for course in course_to_grades:
    total_students = 0 # Need to know total number of students to calculate average
    total_points = 0 # Need to know total grade points in the class
    for grade in course_to_grades[course]: # Loop through A+, A-, etc.
      # the no. of students is just the frequency, which is how many
      # students got that particular grade, which we can access by
      # accessing dictionary keys one after each other.
      total_students += course_to_grades[course][grade]

      # the points we're adding are weighted based on the grade
      # so we multiple the no. of students with the GPA associated
      # with that grade (based on our grades_to_points dict we created
      # above)
      total_points += course_to_grades[course][grade] * grades_to_points[grade]

    # Make sure we don't try to divide by 0
    if total_students != 0:
      course_to_gpa[course] = (total_points / total_students)
    else:
      # if total_students is 0 then stick 'N/A' in the dict. We could
      # do this or throw an error or whatever we want but N/A seems
      # good enough
      course_to_gpa[course] = 'N/A'

  # return the mappings now that we've calculated it
  return course_to_gpa

# This function takes in a course_to_gpa dictionary (that can be created
# by the function above), and a filename, and outputs each of the
# course/gpa mappings in CSV format "CS2110,3.6" on one line, for
# example
def output_avg_to_file(course_to_gpa, filename):
  f = open(filename, 'w') # open the file to write
  for course in course_to_gpa: # loop through the courses
    # format the output string using the format() function
    # which replaces all {} in the string with the parameter
    # in the same position within the format function. So the value
    # of 'course' will be put into the first {}, and the GPA will
    # be put in the second. We put a newline \n to go to the next line
    # so the next time we write a value its on its own line
    val = '{},{}\n'.format(course, course_to_gpa[course])
    f.write(val) # write it out to the file

  f.close() # remember to close the file, esp. when writing

# THIS IS THE ACTUAL MAIN THAT STARTS THE EXECUTION #
# Since all the other ones were functions, they don't
# get executed until they are called. But, we need to
# defined them before we use them, so we defined them higher
# up in the file.

# Read the grades file grades.txt within the same directory as our python file
grades = read_grades_file('grades.txt')

# Calculate the average GPA for each course
course_to_avg_gpa = calculate_avg_gpas(grades)

# output them to output.txt
output_avg_to_file(course_to_avg_gpa, 'output.txt')
from django.http import HttpResponse
import csv 
from esgpapp.models import CSV_Content


########### 1 ###########

def predict(users):
    for user in users:

        #Taken / Given Quizes Percentage 
        total_quizes = user.total_quizes
        given_quizes = user.given_quizes
        avg_quizes = (given_quizes/total_quizes) * 100

        #Taken / Given Quizes Marks Percentage 
        total_marks_of_quizes = user.total_marks_of_quizes
        obtain_marks_in_quizes = user.obtain_marks_in_quizes
        avg_quizes_marks = (obtain_marks_in_quizes/total_marks_of_quizes)*100

        #Average Quizes Part
        avg_quizes_part = (avg_quizes + avg_quizes_marks)/2

        #Taken / Quizes Remedial Plan
        quiz_remedial_plan = get_quiz_remedial_plan(avg_quizes_part)

        #Taken / Given Assignments Percentage 
        total_assignments = user.total_assignments
        given_assignments = user.given_assignments
        avg_assignments = (given_assignments/total_assignments) * 100

        #Taken / Given Assignmnts Marks Percentage 
        total_marks_of_assignments = user.total_marks_of_assignments
        obtain_marks_in_assignments = user.obtain_marks_in_assignments
        avg_assignments_marks = (obtain_marks_in_assignments / total_marks_of_assignments) *100
        
        #Average Assignments Part
        avg_assignments_part = (avg_assignments + avg_assignments_marks)/2

        #Taken / Assignments Remedial Plan
        assignments_remedial_plan = get_assignments_remedial_plan(avg_assignments_part)

        #Taken Attendance Percentage
        total_classes = user.total_classes
        taken_classes = user.taken_classes
        avg_classes = (taken_classes/total_classes) * 100

        #Taken / Attendance Remedial Plan
        classes_remedial_plan = get_classes_remedial_plan(avg_classes)


        #Taken Previous Relevent Percentage
        avg_previous_percentage = user.last_month_grade

        #Final Calculation
        predicted_grade = (
            avg_quizes_part +
            avg_assignments_part +
            avg_classes +
            avg_previous_percentage
        ) / 4
        
        grade =''
        if predicted_grade >= 84.5:
            grade = 'A+'
        elif predicted_grade >= 79.5 and predicted_grade <= 84.4:
            grade = 'A'
        elif predicted_grade >= 74.5 and predicted_grade <= 79.4:
            grade = 'B+'
        elif predicted_grade >= 69.5 and predicted_grade <= 74.4:
            grade = 'B'
        elif predicted_grade >= 64.5 and predicted_grade <= 69.4:
            grade = 'B-'
        elif predicted_grade >= 59.5 and predicted_grade <= 64.4:
            grade = 'C+'
        elif predicted_grade >= 54.5 and predicted_grade <= 59.4:
            grade = 'C'
        elif predicted_grade >= 49.5 and predicted_grade <= 54.4:
            grade = 'D'
        else:
            grade = 'F'
        
        user.grades = grade
        user.save
        
        #Upadating User Record
        user.predicted_grads = predicted_grade
        user.save()

        #Final Remedial Plan
        if quiz_remedial_plan == 'quizzes' or assignments_remedial_plan == 'assignments' or classes_remedial_plan == "attendence":
            remedial_plan ="This student needs to impover their {} {} {}".format(
                quiz_remedial_plan + ' , ' if quiz_remedial_plan == 'quizzes' else '',
                assignments_remedial_plan + ' , ' if assignments_remedial_plan == 'assignments' else '',
                classes_remedial_plan + ' , ' if classes_remedial_plan == 'attendence' else ''
            )
        elif quiz_remedial_plan == "excellent" and assignments_remedial_plan == "excellent" and classes_remedial_plan == "excellent":
            remedial_plan = "This student will get excellent grades in quizzes, assignments and attendance."
        else:
            remedial_plan = "This student will get good grades in quizzes, assignments and attendance."


        user.remedial_plan = remedial_plan
        user.save()
        
    return

########### 2 ###########

def get_quiz_remedial_plan(avg_quizes_part):
    remedial_plan = ''
    if avg_quizes_part <= 70:
        remedial_plan = 'quizzes'
    elif avg_quizes_part <= 80:
        remedial_plan = 'good'
    else:
        remedial_plan = 'excellent'

    return remedial_plan

########### 3 ###########

def get_assignments_remedial_plan(avg_assignments_part):
    remedial_plan = ''
    if avg_assignments_part <= 70:
        remedial_plan = 'assignments'
    elif avg_assignments_part <= 80:
        remedial_plan = 'good'
    else:
        remedial_plan = 'excellent'
    
    return remedial_plan

########### 4 ###########

def get_classes_remedial_plan(avg_classes):
    remedial_plan = ''

    if avg_classes <= 70:
        remedial_plan = 'attendence'
    elif avg_classes <= 80:
        remedial_plan = 'good'
    else:
        remedial_plan = 'excellent'

    return remedial_plan
########### 5 ###########

def checks(
    total_quizes,
    given_quizes,
    total_marks_of_quizes,
    obtain_marks_in_quizes,
    total_assignments,
    given_assignments,
    total_marks_of_assignments,
    obtain_marks_in_assignments,
    total_classes,
    taken_classes
    ):
    msg = False
    
    if int(given_quizes) > int(total_quizes):
        msg = 'Given quizzes cannot greater then total quizzes'
        
    elif int(obtain_marks_in_quizes) > int(total_marks_of_quizes):
        msg = 'Obtain quizzes marks cannot greater then total quizzes marks'
      
    elif int(given_assignments) > int(total_assignments):
        msg = 'Given assignments cannot greater then total assignments'
     
    elif int(obtain_marks_in_assignments) > int(total_marks_of_assignments):
        msg = 'Obtain assignments marks cannot greater then total assignments marks'
        
    elif int(taken_classes) > int(total_classes):
        msg = 'Taken classes cannot greater then total classes'
    
    return msg
       
########### 6 ###########

def exportCSV_Content(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=predicted_grades.csv"
    writer = csv.writer(response)
    row = [
        'Student ID',
        'Student Name',
        'Total Quizzes',
        'Given Quizzes',
        'Total Marks of Quizzes',
        'Obtain Marks in Quizzes',
        'Total Assignments',
        'Given Assignments',
        'Total Marks of Assignments',
        'Obtain Marks in Assignments',
        'Total Classes',
        'Taken Classes',
        'Previous Grades (%)',
        'Predicted Grades (%)',
        'Grades',
        'Remedial Plan',
    ]
    writer.writerow(row)
    users = CSV_Content.objects.all().values_list(
        'student_id',
        'student_name',
        'total_quizes',
        'given_quizes',
        'total_marks_of_quizes',
        'obtain_marks_in_quizes',
        'total_assignments',
        'given_assignments',
        'total_marks_of_assignments',
        'obtain_marks_in_assignments',
        'total_classes',
        'taken_classes',
        'last_month_grade',
        'predicted_grads',
        'grades',
        'remedial_plan',
    )
    for user in users:
        writer.writerow(user)

    CSV_Content.objects.all().delete()
    return response

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Avg, F
from django.contrib.flatpages.models import FlatPage
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail

from .serializers import ChairmanSerializer, ChairmanDashboardSerializer, TeacherSerializer, CategorySerializer, CourseSerializer, StudentSerializer, StudentCourseEnrollSerializer, TeacherDashboardSerializer, StudentAssignmentSerializer, StudentDashboardSerializer, NotificationSerializer, QuizSerializer, QuestionSerializer, CourseQuizSerializer, AttempQuizSerializer, TeacherStudentChatSerializer
#  ,FlatPagesSerializer
from . import models

from random import randint


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 8


class ChairmanList(generics.ListCreateAPIView):
    queryset = models.Chairman.objects.all()
    serializer_class = ChairmanSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ChairmanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Chairman.objects.all()
    serializer_class = ChairmanSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ChairmanDashboard(generics.RetrieveAPIView):
    queryset = models.Chairman.objects.all()
    serializer_class = ChairmanDashboardSerializer


@csrf_exempt
def chairman_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        chairData = models.Chairman.objects.get(
            email=email, password=password)
    except models.Chairman.DoesNotExist:
        chairData = None
    if chairData:
        return JsonResponse({'bool': True, 'chair_id': chairData.id})
    else:
        return JsonResponse({'bool': False})


@csrf_exempt
def chairman_change_password(request, chair_id):
    password = request.POST['password']

    try:
        chairData = models.Chairman.objects.get(id=chair_id)
    except models.Chairman.DoesNotExist:
        chairData = None
    if chairData:
        models.Chairman.objects.filter(id=chair_id).update(password=password)
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class TeacherList(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes=[permissions.IsAuthenticated]


class TeacherDashboard(generics.RetrieveAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherDashboardSerializer


@csrf_exempt
def teacher_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(
            email=email, password=password)
    except models.Teacher.DoesNotExist:
        teacherData = None
    if teacherData:
        return JsonResponse({'bool': True, 'teacher_id': teacherData.id})
    else:
        return JsonResponse({'bool': False})


class CategoryList(generics.ListCreateAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = CategorySerializer

# Course


class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = models.Course.objects.all().order_by('-id')[:limit]

        if 'category' in self.request.GET:
            category = self.request.GET['category']
            category = models.CourseCategory.objects.filter(
                id=category).first()
            qs = models.Course.objects.filter(category=category)

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            if search:
                qs = models.Course.objects.filter(
                    Q(title__icontains=search) | Q(techs__icontains=search))

        return qs


class CourseDetailView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


# Specific Teacher Course
class TeacherCourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = models.Teacher.objects.get(pk=teacher_id)
        return models.Course.objects.filter(teacher=teacher)


# Specific Teacher Course
class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


# Student Data
class StudentList(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes=[permissions.IsAuthenticated]


class StudentDashboard(generics.RetrieveAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentDashboardSerializer


@csrf_exempt
def student_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        studentData = models.Student.objects.get(
            email=email, password=password)
    except models.Student.DoesNotExist:
        studentData = None
    if studentData:
        return JsonResponse({'bool': True, 'student_id': studentData.id})
    else:
        return JsonResponse({'bool': False})


class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer


def fetch_enroll_status(request, student_id, course_id):
    student = models.Student.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    enrollStatus = models.StudentCourseEnrollment.objects.filter(
        course=course, student=student).count()
    if enrollStatus:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class EnrolledStudentList(generics.ListAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = models.Course.objects.get(pk=course_id)
            return models.StudentCourseEnrollment.objects.filter(course=course)
        elif 'teacher_id' in self.kwargs:
            teacher_id = self.kwargs['teacher_id']
            teacher = models.Teacher.objects.get(pk=teacher_id)
            return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        elif 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.Student.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()


class MyTeacherList(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            sql = f"SELECT * FROM main_course as c,main_studentcourseenrollment as e,main_teacher as t WHERE c.teacher_id=t.id AND e.course_id=c.id AND e.student_id={student_id} GROUP BY c.teacher_id"
            qs = models.Course.objects.raw(sql)
            print(qs)
            return qs


@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST['password']
    try:
        teacherData = models.Teacher.objects.get(id=teacher_id)
    except models.Teacher.DoesNotExist:
        teacherData = None
    if teacherData:
        models.Teacher.objects.filter(id=teacher_id).update(password=password)
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class AssignmentList(generics.ListCreateAPIView):
    queryset = models.StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        teacher_id = self.kwargs['teacher_id']
        student = models.Student.objects.get(pk=student_id)
        teacher = models.Teacher.objects.get(pk=teacher_id)
        return models.StudentAssignment.objects.filter(student=student, teacher=teacher)


class MyAssignmentList(generics.ListCreateAPIView):
    queryset = models.StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = models.Student.objects.get(pk=student_id)
        # Update Notifications
        models.Notification.objects.filter(
            student=student, notif_for='student', notif_subject='assignment').update(notifiread_status=True)
        return models.StudentAssignment.objects.filter(student=student)


class UpdateAssignment(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer


@csrf_exempt
def student_change_password(request, student_id):
    password = request.POST['password']
    try:
        studentData = models.Student.objects.get(id=student_id)
    except models.Teacher.DoesNotExist:
        studentData = None
    if studentData:
        models.Student.objects.filter(id=student_id).update(password=password)
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class NotificationList(generics.ListCreateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = models.Student.objects.get(pk=student_id)
        return models.Notification.objects.filter(student=student, notif_for='student', notif_subject='assignment', notifiread_status=False)


class QuizList(generics.ListCreateAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer

# Specific Teacher Quiz


class TeacherQuizList(generics.ListCreateAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = models.Teacher.objects.get(pk=teacher_id)
        return models.Quiz.objects.filter(teacher=teacher)


class TeacherQuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizQuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        quiz = models.Quiz.objects.get(pk=quiz_id)
        if 'limit' in self.kwargs:
            return models.QuizQuestions.objects.filter(quiz=quiz).order_by('id')[:1]
        elif 'question_id' in self.kwargs:
            current_question = self.kwargs['question_id']
            return models.QuizQuestions.objects.filter(quiz=quiz, id__gt=current_question).order_by('id')[:1]
        else:
            return models.QuizQuestions.objects.filter(quiz=quiz)


class CourseQuizList(generics.ListCreateAPIView):
    queryset = models.CourseQuiz.objects.all()
    serializer_class = CourseQuizSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = models.Course.objects.get(pk=course_id)
            return models.CourseQuiz.objects.filter(course=course)


def fetch_quiz_assign_status(request, quiz_id, course_id):
    quiz = models.Quiz.objects.filter(id=quiz_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    assignStatus = models.CourseQuiz.objects.filter(
        course=course, quiz=quiz).count()
    if assignStatus:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class AttemptQuizList(generics.ListCreateAPIView):
    queryset = models.AttempQuiz.objects.all()
    serializer_class = AttempQuizSerializer

    def get_queryset(self):
        if 'quiz_id' in self.kwargs:
            quiz_id = self.kwargs['quiz_id']
            quiz = models.Quiz.objects.get(pk=quiz_id)
            return models.AttempQuiz.objects.raw(f'SELECT * FROM main_attempquiz WHERE quiz_id={int(quiz_id)} GROUP by student_id')


def fetch_quiz_attempt_status(request, quiz_id, student_id):
    quiz = models.Quiz.objects.filter(id=quiz_id).first()
    student = models.Student.objects.filter(id=student_id).first()
    attemptStatus = models.AttempQuiz.objects.filter(
        student=student, question__quiz=quiz).count()
    print(models.AttempQuiz.objects.filter(
        student=student, question__quiz=quiz).query)
    if attemptStatus > 0:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


def fetch_quiz_result(request, quiz_id, student_id):
    quiz = models.Quiz.objects.filter(id=quiz_id).first()
    student = models.Student.objects.filter(id=student_id).first()
    total_questions = models.QuizQuestions.objects.filter(quiz=quiz).count()
    total_attempted_questions = models.AttempQuiz.objects.filter(
        quiz=quiz, student=student).values('student').count()
    attempted_questions = models.AttempQuiz.objects.filter(
        quiz=quiz, student=student)

    total_correct_questions = 0
    for attempt in attempted_questions:
        if attempt.right_ans == attempt.question.right_ans:
            total_correct_questions += 1

    return JsonResponse({'total_questions': total_questions, 'total_attempted_questions': total_attempted_questions, 'total_correct_questions': total_correct_questions})


@csrf_exempt
def teacher_forgot_password(request):
    email = request.POST.get('email')
    verify = models.Teacher.objects.filter(email=email).first()
    if verify:
        link = f"http://localhost:3000/teacher-change-password/{verify.id}/"
        send_mail(
            'Verify Account',
            'Please verify your account',
            'codeartisanlab2607@gmail.com',
            [email],
            fail_silently=False,
            html_message=f'<p>Your OTP is </p><p>{link}</p>'
        )
        return JsonResponse({'bool': True, 'msg': 'Please check your email'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Invalid Email!!'})


@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST.get('password')
    verify = models.Teacher.objects.filter(id=teacher_id).first()
    if verify:
        models.Teacher.objects.filter(id=teacher_id).update(password=password)
        return JsonResponse({'bool': True, 'msg': 'Password has been changed'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})


@csrf_exempt
def user_forgot_password(request):
    email = request.POST.get('email')
    verify = models.Student.objects.filter(email=email).first()
    if verify:
        link = f"http://localhost:3000/user-change-password/{verify.id}/"
        send_mail(
            'Verify Account',
            'Please verify your account',
            'codeartisanlab2607@gmail.com',
            [email],
            fail_silently=False,
            html_message=f'<p>Your OTP is </p><p>{link}</p>'
        )
        return JsonResponse({'bool': True, 'msg': 'Please check your email'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Invalid Email!!'})


@csrf_exempt
def user_change_password(request, student_id):
    password = request.POST.get('password')
    verify = models.Student.objects.filter(id=student_id).first()
    if verify:
        models.Student.objects.filter(id=student_id).update(password=password)
        return JsonResponse({'bool': True, 'msg': 'Password has been changed'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})


@csrf_exempt
def save_teacher_student_msg(request, teacher_id, student_id):
    teacher = models.Teacher.objects.get(id=teacher_id)
    student = models.Student.objects.get(id=student_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')
    msgRes = models.TeacherStudentChat.objects.create(
        teacher=teacher,
        student=student,
        msg_text=msg_text,
        msg_from=msg_from,
    )
    if msgRes:
        msgs = models.TeacherStudentChat.objects.filter(
            teacher=teacher, student=student).count()
        return JsonResponse({'bool': True, 'msg': 'Message has been send', 'total_msg': msgs})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})


class MessageList(generics.ListAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = TeacherStudentChatSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        student_id = self.kwargs['student_id']
        teacher = models.Teacher.objects.get(pk=teacher_id)
        student = models.Student.objects.get(pk=student_id)
        return models.TeacherStudentChat.objects.filter(teacher=teacher, student=student).exclude(msg_text='')


@csrf_exempt
def save_teacher_student_group_msg(request, teacher_id):
    teacher = models.Teacher.objects.get(id=teacher_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')

    enrolledList = models.StudentCourseEnrollment.objects.filter(
        course__teacher=teacher).distinct()
    for enrolled in enrolledList:
        msgRes = models.TeacherStudentChat.objects.create(
            teacher=teacher,
            student=enrolled.student,
            msg_text=msg_text,
            msg_from=msg_from,
        )
    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'Message has been send'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})


@csrf_exempt
def save_teacher_student_group_msg_from_student(request, student_id):
    student = models.Student.objects.get(id=student_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')

    sql = f"SELECT * FROM main_course as c,main_studentcourseenrollment as e,main_teacher as t WHERE c.teacher_id=t.id AND e.course_id=c.id AND e.student_id={student_id} GROUP BY c.teacher_id"
    qs = models.Course.objects.raw(sql)

    myCourses = qs
    for course in myCourses:
        msgRes = models.TeacherStudentChat.objects.create(
            teacher=course.teacher,
            student=student,
            msg_text=msg_text,
            msg_from=msg_from,
        )
    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'Message has been send'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})

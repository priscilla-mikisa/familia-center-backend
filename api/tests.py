from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from student.models import Student
from .serializers import StudentSerializer
# Create your tests here.

class StudentListAPIViewTest(APITestCase):
    def setUp(self):
         self.student = Student.objects.create(
             first_name = "Canary",
            last_name = "Mugume",
            email = "priscillamikisa@gmail.com",
            student_code = 112,
            country = "Uganda",
            gender = "female",
            bio = "Still moving.......",
            id_number = 21,
            grade_level = 4,
            gurdian_name = "Dakota",
            student_next_of_kin = "Huffy",
            student_national_id_number = "578h0h32808bs",
         )
         
    def test_get_student_list(self):
        url = reversed("student_list_view")
        response = self.client.get(url)
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
from django.db import models

class Student(models.Model):
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]

    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]
    
    college_id = models.CharField(max_length=20, unique=True ,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)
    images = models.ImageField(upload_to='students/',null=True)
    batch = models.CharField(max_length=20, null=True)   # Example: 2022-2026
    year = models.IntegerField(choices=YEAR_CHOICES, null=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=True)

    def __str__(self):
        return f"{self.name} ({self.batch})"

class Subject(models.Model):

    SUBJECT_CHOICES = [
        ('English', 'English'),
        ('Maths', 'Maths'),
        ('Science', 'Science'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Computer', 'Computer'),
    ]

    name = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')]
    )

    class Meta:
        constraints = [
            # ❌ Same subject twice in a day
            models.UniqueConstraint(
                fields=['student', 'date', 'subject'],
                name='unique_subject_per_day'
            ),
            # ❌ Same period twice in a day
            models.UniqueConstraint(
                fields=['student', 'date', 'period'],
                name='unique_period_per_day'
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date}"

    

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks = models.IntegerField()
    result = models.CharField(max_length=10)  
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

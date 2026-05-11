from django.db import models


class Profile(models.Model):
     image = models.ImageField(upload_to='foto/')
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    image = models.ImageField(upload_to='projects/')

    github_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)

    tech_stack = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    title = models.CharField(max_length=200)

    issuer = models.CharField(max_length=200)

    image = models.ImageField(upload_to='certificates/')

    pdf = models.FileField(
        upload_to='certificate_pdfs/',
        blank=True,
        null=True
    )

    issue_date = models.DateField()

    credential_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.IntegerField(default=80)

    def __str__(self):
        return self.name
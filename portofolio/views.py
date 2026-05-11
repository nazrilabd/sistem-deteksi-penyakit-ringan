from django.shortcuts import render, get_object_or_404
from .models import Project, Certificate, Skill, Profile


def home(request):
    projects = Project.objects.all()
    profile = Profile.objects.first()
    certificates = Certificate.objects.all()

    context = {
        'projects': projects,
         'certificates': certificates,
         'profile': profile
    }
    return render(request, 'portofolio/home.html',context)


def projects(request):
    projects = Project.objects.all()

    context = {
        'projects': projects
    }

    return render(request, 'portofolio/projects.html', context)

def project_detail(request, id):

    project = get_object_or_404(Project, id=id)

    return render(request, 'portofolio/project_detail.html', {
        'project': project
    })

def certificates(request):
    certificates = Certificate.objects.all()

    context = {
        'certificates': certificates
    }

    return render(request, 'portofolio/certificates.html', context)

def certificate_detail(request, id):

    certificate = get_object_or_404(Certificate, id=id)

    return render(request, 'portofolio/certificate_detail.html', {
        'certificate': certificate
    })
def skills(request):
    skills = Skill.objects.all()

    context = {
        'skills': skills
    }

    return render(request, 'portofolio/skills.html', context)

def about(request):
    profile = Profile.objects.first()
    context = {
        'profile': profile
    }
    return render(request, 'portofolio/about.html',context)
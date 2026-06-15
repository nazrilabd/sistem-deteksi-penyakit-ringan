from django.urls import path
from .views import (
    home,
    diagnosis,
    about,
    download_pdf
)

urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

    path(
        'diagnosis/',
        diagnosis,
        name='diagnosis'
    ),

    path(
        'tentang/',
        about,
        name='about'
    ),

    path(
        'download-pdf/',
        download_pdf,
        name='download_pdf'
    ),

]
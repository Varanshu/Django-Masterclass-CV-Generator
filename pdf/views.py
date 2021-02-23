from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

# Create your views here.
def accept(request):
    if request.method == "POST":
        name = request.POST.get('name',"")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        school = request.POST.get("school","")
        degree = request.POST.get("degree","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")
        print(name)

        profile = Profile(name = name, email = email, phone = phone, summary = summary, school=school, degree = degree, university = university, previous_work = previous_work, skills = skills)
        profile.save()
    return render(request,'pdf/accept.html')

def resume(request,id):
    user_profile = Profile.objects.get(pk=id)

    # path_wkhtmltopdf=r'‪C:\wkhtmltox\bin\wkhtmltopdf.exe'
    # path_wkhtmltopdf=r'C:\wkhtmltox\bin\wkhtmltopdf.exe'
    #
    # config = pdfkit.configuration(wkhtmltopdf = path_wkhtmltopdf)

    path_wkhtmltopdf = r'C:\wkhtmltox\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile':user_profile})
    options ={
        'page-size':'Letter',
        'encoding':"UTF-8",
    }
    pdf = pdfkit.from_string(html,False,options,configuration=config)

    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename="resume.pdf"

    return response
    # return render(request,'pdf/resume.html',{'user_profile':user_profile})

def list(request):
    profile = Profile.objects.all()
    return render(request,'pdf/list.html',{'profile':profile})

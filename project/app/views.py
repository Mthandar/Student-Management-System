from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import student
from .forms import StudentForm

# Create your views here.
def index(request):
  return render(request, 'students/index.html', {
    'students': student.objects.all()
  })


def view_student(request, id):
  return HttpResponseRedirect(reverse('index'))

def add(request):
  if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
      new_student_number = form.cleaned_data['student_number']
      new_first_name = form.cleaned_data['first_name']
      new_last_name = form.cleaned_data['last_name']
      new_email = form.cleaned_data['email']
      new_field_of_study = form.cleaned_data['field_of_study']
      new_gpa = form.cleaned_data['gpa']

      new_student = student(
        student_number=new_student_number,
        first_name=new_first_name,
        last_name=new_last_name,
        email=new_email,
        field_of_study=new_field_of_study,
        gpa=new_gpa
      )
      new_student.save()
      return render(request, 'students/add.html', {
        'form': StudentForm(),
        'success': True
      })
  else:
    form = StudentForm()
  return render(request, 'students/add.html', {
    'form': StudentForm()
  })

def edit(request, id):
  if request.method == 'POST':
    students = student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=students)
    if form.is_valid():
      form.save()
      return render(request, 'students/edit.html', {
        'form': form,
        'success': True
      })
  else:
    students = student.objects.get(pk=id)
    form = StudentForm(instance=students)
  return render(request, 'students/edit.html', {
    'form': form
  })

def delete(request, id):
  if request.method == 'POST':
    students = student.objects.get(pk=id)
    students.delete()
    return HttpResponseRedirect(reverse('index'))
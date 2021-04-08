from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from .passwords import Special
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        sp = Special(request.POST['password1'])
        #Create a new user
        err1 = "Password too short"
        err2 = "Password can not be Totally Integer"
        err3 = "Password must contain a small letter"
        err4 = "Password must have at least one numeric"
        err5 = "Password must have at least one special character from these [_@$/|?#]"
        err6 = "Password must have at least one Capital Letter"

        if len(request.POST['password1']) <= 7:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":err1})
        elif request.POST['password1'].isdigit():
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":err2})
        elif sp.capitalCheck() == False:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":err6})
        elif sp.smallCheck()==False:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":err3})
        elif sp.numCheck() == False:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":err4})
        elif sp.checkSpecial() == False:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":err5})
        elif request.POST['password1'] == request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":"User Name Taken Already."})
            except Exception as e:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":e})
        else:
            #password did not match
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),"error":"Password did not match"})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            errmsg = "User Name & Password Does Not Match"
            return render(request,'todo/login.html',{'form':AuthenticationForm(),"error":errmsg})
        else:
            try:
                login(request,user)
                return redirect('currenttodo')
            except Exception as e:
                return render(request,'todo/login.html',{'form':AuthenticationForm(),"error":e})

@login_required
def currenttodo(request):
    todos = Todo.objects.filter(user=request.user,completed_at__isnull=True)
    return render(request,'todo/currenttodo.html',{"todos":todos})


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),"error":"Bad Data Passed"})
        except Exception as e:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),"error":e})

@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{"todo":todo,"form":form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todo/viewtodo.html',{"todo":todo,"form":form,"error":"Bad Data Passed"})
        except Exception as e:
            return render(request,'todo/viewtodo.html',{"todo":todo,"form":form,"error":e})

@login_required
def completedtodo(request):
    todos = Todo.objects.filter(user=request.user,completed_at__isnull=False).order_by('-completed_at')
    return render(request,'todo/completedtodo.html',{"todos":todos})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.completed_at = timezone.now()
        todo.save()
        return redirect('currenttodo')
    
@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
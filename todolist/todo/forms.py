from django.forms import ModelForm
from .models import Todo
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "memo","important"]


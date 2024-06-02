from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import NewsForm
from authentication.models import YourModel
import joblib
import numpy as np

# Load the pre-trained model and accuracy
model, accuracy = joblib.load('ml-models/fake_news_detector.pkl')

def predict_news(request):
    result = None
    confidence = None
    fake_percentage = None
    real_percentage = None
    dubious_percentage = None
    textarea_value = None
    char_count = None

    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # Get the news content from the form
            news_content = form.cleaned_data['news_content']
            textarea_value = news_content

            # Get the character count from the POST data
            char_count = request.POST.get('char_count', '0')

            # Make a prediction
            prediction = model.predict([news_content])
            prediction_proba = model.predict_proba([news_content])

            # Define the labels and confidence
            labels = ['FAKE', 'REAL']
            confidence = round(prediction_proba.max() * 100, 2)

            # Set a confidence threshold for the 'dubious' label
            threshold = 50  # Adjust this value as needed

            # Get the probabilities for both classes
            fake_percentage = round(prediction_proba[0][0] * 100, 2)
            real_percentage = round(prediction_proba[0][1] * 100, 2)

            # Determine the result based on the confidence threshold
            if confidence < threshold:
                result = 'DUBIOUS'
                dubious_percentage = round(100 - confidence, 2)
            else:
                result = labels[prediction[0]]
                dubious_percentage = 0  # Not dubious if above threshold

    else:
        form = NewsForm()

    return render(request, 'authentication/verify.html', {
        'form': form,
        'textarea_value': textarea_value,
        'char_count': char_count,
        'result': result,
        'confidence': confidence,
        'fake_percentage': fake_percentage,
        'real_percentage': real_percentage,
        'dubious_percentage': dubious_percentage,
        'accuracy': round(accuracy * 100, 2),
       })

# Create your views here.
def chart_view(request):
    data = YourModel.objects.all().values('category', 'value')
    labels = [item['category'] for item in data]
    values = [item['value'] for item in data]
    return render(request, 'chart_template.html', {'labels': labels, 'values': values})

def homepage(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('verify')
    else:
        form = NewsForm()
    return render(request, 'authentication/homepage.html', {'form': form})

# def homepage(request):
#   # return render(request, 'authentication/homepage.html')
#   if request.method == 'POST':
#     textarea_value = request.POST.get('textarea_name', '')  # Get textarea value from POST data
#     return render(request, 'authentication/verify.html', {'textarea_value': textarea_value})
#   else:
#     return render(request, 'authentication/homepage.html')
  
def result(request):
 return render(request, 'authentication/result.html')

# def verify(request):
#  return render(request, 'authentication/verify.html')

def home(request):
  # return render(request, 'authentication/index.html')
  if request.method == 'POST':
    textarea_value = request.POST.get('textarea_name', '')  # Get textarea value from POST data
    return render(request, 'authentication/verify.html', {'textarea_value': textarea_value})
  else:
    return render(request, 'authentication/index.html')

@login_required
def settings(request):
    fname = request.user.first_name
    lname = request.user.last_name
    return render(request, 'authentication/settings.html', {'fname': fname,'lname': lname})

@login_required
def history(request):
    fname = request.user.first_name
    lname = request.user.last_name
    return render(request, 'authentication/history.html', {'fname': fname, 'lname': lname})

def community(request):
    fname = request.user.first_name
    lname = request.user.last_name
    return render(request, 'authentication/community.html', {'fname': fname, 'lname': lname})

def signup(request):
  if request.method == "POST":
    username = request.POST['username']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']

    if User.objects.filter(username=username):
      messages.error(request, "Username already exists!")
      return redirect('home')

    if User.objects.filter(email=email):
      messages.error(request, "Email already registered!")
      return redirect('home')
    
    if pass1 != pass2:
      messages.error(request, "Passwords didn't match!")

    if not username.isalnum():
      messages.error(request, "Username must be Alpha-Numeric!")
      return redirect('home')

    myuser = User.objects.create_user(username, email, pass1)
    myuser.first_name = fname
    myuser.last_name = lname

    myuser.save()

    messages.success(request, 'Your account has been successfully created.')

    return redirect('signin')

  return render(request, 'authentication/signup.html')


# def signin(request):
#   if request.method == 'POST':
#     email = request.POST['email']
#     pass1 = request.POST['pass1']

#     try:
#       user = User.objects.get(email=email)
#     except User.DoesNotExist:
#       messages.error(request, "User with this email does not exist.")
#       return redirect('home')
    
#     user = authenticate(request, username=user.username, password=pass1)

#     if user is not None:
#       login(request, user)
#       fname = user.first_name
#       return render(request, "authentication/homepage.html", {'fname':fname})

#     else:
#       messages.error(request, "Bad Credentials")
#       return redirect('home')

#   return render(request, 'authentication/signin.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use get() to avoid KeyError
        pass1 = request.POST.get('pass1')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('signin')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect('signin')
        
        user = authenticate(request, username=user.username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/homepage.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, 'authentication/signin.html')


def signout(request):
  logout(request)
  messages.success(request,"Log Out Successfully")
  return redirect('home')
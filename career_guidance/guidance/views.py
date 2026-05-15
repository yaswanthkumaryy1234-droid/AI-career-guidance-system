
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import joblib, os
from django.contrib.auth import update_session_auth_hash
from .models import CareerResult


SECTIONS = {
 "Interest": [
  "I enjoy solving logical problems",
  "I like working with computers",
  "I enjoy creative activities",
  "I like helping people",
  "I am interested in business"
 ],
 "Skills": [
  "I am good at programming",
  "I analyze data easily",
  "I communicate clearly",
  "I manage time effectively",
  "I adapt to new technology"
 ],
 "Aptitude": [
  "I solve numerical problems easily",
  "I understand patterns quickly",
  "I think logically under pressure",
  "I enjoy analytical tasks",
  "I learn technical concepts fast"
 ],
 "Personality": [
  "I am confident in decisions",
  "I like leadership roles",
  "I am patient and focused",
  "I work independently",
  "I take responsibility"
 ],
 "Work Preference": [
  "I prefer desk-based jobs",
  "I prefer flexible hours",
  "I want job stability",
  "I can work long hours",
  "I like teamwork"
 ]
}

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already exists")
            return render(request, "accounts/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ Email already registered")
            return render(request, "accounts/signup.html")

        User.objects.create_user(
            username=username,
            password=request.POST['password'],
            email=email,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name']
        )

        messages.success(request, "✅ Registration successful! You can now login.")
        return render(request, "accounts/signup.html")   # SAME PAGE

    return render(request, "accounts/signup.html")

def login_view(request):
 msg = ''
 if request.method == 'POST':
  user = authenticate(username=request.POST['username'], password=request.POST['password'])
  if user:
   login(request, user)
   return redirect('dashboard')
  msg = 'Invalid username or password'
 return render(request, 'accounts/login.html', {'msg': msg})

def logout_view(request):
 logout(request)
 return redirect('login')

@login_required
def dashboard(request):
 return render(request, 'guidance/dashboard.html')

@login_required
def career_test(request):
    if request.method == 'POST':
        scores = {}
        features = []

        for section in SECTIONS:
            section_score = 0
            for i in range(len(SECTIONS[section])):
                section_score += int(request.POST.get(f"{section}_{i}"))
            scores[section] = section_score
            features.append(section_score)

        model = joblib.load(
            os.path.join(os.path.dirname(__file__), 'ml', 'career_model.pkl')
        )

        prediction = model.predict([features])[0]

        # SAVE RESULT
        result = CareerResult.objects.create(
            user=request.user,
            career=prediction,
            scores=scores
        )

        # 🔁 REDIRECT TO RESULT PAGE
        return redirect('career_result', result_id=result.id)

    return render(request, 'guidance/test.html', {
        'sections': SECTIONS
    })

@login_required
def career_result(request, result_id):
    result = CareerResult.objects.get(id=result_id, user=request.user)
    return render(request, 'guidance/result.html', {'result': result})



@login_required
def profile_view(request):
    return render(request, 'guidance/profile.html')


@login_required
def profile_update(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        messages.success(request, "Profile updated successfully")
        return render(request, 'guidance/profile_update.html')

    return render(request, 'guidance/profile_update.html')




@login_required
def change_password(request):
    if request.method == "POST":
        old = request.POST['old_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if not request.user.check_password(old):
            messages.error(request, "Old password is incorrect")
        elif new != confirm:
            messages.error(request, "Passwords do not match")
        else:
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully")

    return render(request, 'guidance/change_password.html')

@login_required
def career_history(request):
    results = CareerResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "guidance/career_history.html", {"results": results})

@login_required
def delete_result(request, result_id):
    result = CareerResult.objects.get(id=result_id, user=request.user)

    if request.method == "POST":
        result.delete()
        messages.success(request, "Career result deleted successfully")

    return redirect('career_history')

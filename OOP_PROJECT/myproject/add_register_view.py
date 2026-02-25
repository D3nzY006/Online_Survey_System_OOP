#!/usr/bin/env python
import os
import sys

# Add the project directory to sys.path
sys.path.insert(0, r'c:\Users\MarkDenzyManang\OOP_PROJECT\myproject')

viewspath = r'c:\Users\MarkDenzyManang\OOP_PROJECT\myproject\app\views.py'

with open(viewspath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'def register(request):' not in content:
    register_code = '''

def register(request):
    """Register view for new users"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')
        
        if not all([first_name, last_name, email, password]):
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        username = email
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('log_in')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'register.html')
    
    return render(request, 'register.html')
'''
    
    with open(viewspath, 'a', encoding='utf-8') as f:
        f.write(register_code)
    print('Register view added successfully')
else:
    print('Register view already exists')

#!/usr/bin/env python
# Script to add register view to views.py

with open('app/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check if register already exists
content = ''.join(lines)
if 'def register(request):' not in content:
    # Find the first log_out function and insert register before it
    insert_index = -1
    
    for i, line in enumerate(lines):
        if 'def log_out(request):' in line and insert_index == -1:
            insert_index = i
            break
    
    if insert_index > 0:
        register_code = '''def register(request):
    """Register view for new users"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'student')
        
        # Validate inputs
        if not all([first_name, last_name, email, password]):
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'register.html')
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        # Create new user - use email as username
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
        lines.insert(insert_index, register_code)
        
        # Write back
        with open('app/views.py', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("✓ Register view added successfully!")
    else:
        print("✗ Could not find insertion point")
else:
    print("ℹ Register view already exists")

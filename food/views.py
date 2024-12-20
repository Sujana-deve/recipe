from django.shortcuts import render, redirect
from .models import Recipe
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
# View to display and add recipes
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")

        # Create the recipe object
        Recipe.objects.create(
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description,
        )
        return redirect('/recipes/')

    queryset = Recipe.objects.all()
    context = {'recipes': queryset}

    return render(request, 'recipes.html', context)

# View to update recipes
def update_recipe(request, id):
    try:
        queryset = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found.", status=404)

    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")

        # Update the fields
        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        if recipe_image:
            queryset.recipe_image = recipe_image
        queryset.save()
        return redirect('/recipes/')

    context = {'recipe': queryset}
    return render(request, 'update_recipes.html', context)

# View to delete recipes
def delete_recipe(request, id):
    try:
        queryset = Recipe.objects.get(id=id)
        queryset.delete()
        return redirect('/recipes/')
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found.", status=404)

# Login view
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # matches form input name
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Successful authentication
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/recipes/')
        else:  # Authentication failed
            messages.error(request, 'Invalid username or password.')
            return redirect('/login/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

# Registration view
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('/register/')

        # Create the user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password  # Proper password hashing
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('/login/')

    return render(request, 'register.html')

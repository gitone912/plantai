from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Plant

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def plant_scan(request):
    if request.method == 'POST':
        # Process the scanned plant image and retrieve plant information using AI model
        name = "Sample Plant"
        description = "This is a sample plant."
        scientific_name = "Plantus sampleus"
        watering_instructions = "Water the plant once a week."
        disinfection_instructions = "Disinfect the plant every month."
        image_url = "https://example.com/sample-plant.jpg"

        # Create a new Plant instance with the retrieved information
        plant = Plant(name=name, description=description, scientific_name=scientific_name,
                      watering_instructions=watering_instructions, disinfection_instructions=disinfection_instructions,
                      image_url=image_url, user=request.user)
        plant.save()

        return redirect('plant_save')
    return render(request, 'scan.html')

def plant_save(request):
    if request.method == 'POST':
        # Save the scanned plant information to the user's profile
        # Associate the scanned plant with the currently logged in user
        return redirect('dashboard')
    return render(request, 'save.html')

def contribution_system(request):
    # Retrieve information about planting locations, growth details, and green points
    locations = ["Location A", "Location B", "Location C"]
    growth_details = ["Growth detail 1", "Growth detail 2", "Growth detail 3"]
    green_points = 100

    return render(request, 'contribution.html', {'locations': locations, 'growth_details': growth_details,
                                                 'green_points': green_points})

def dashboard(request):
    # Retrieve the user's saved plants and their status
    saved_plants = Plant.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'saved_plants': saved_plants})

def tree_map(request):
    # Retrieve tree locations and display them on a map
    tree_locations = ["Location X", "Location Y", "Location Z"]
    return render(request, 'treemap.html', {'tree_locations': tree_locations})

def plant_library(request):
    # Retrieve plant data and videos for user knowledge
    plants = Plant.objects.all()
    return render(request, 'library.html', {'plants': plants})

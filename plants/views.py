from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Plant_details as Plant
import base64
import requests

from django.shortcuts import redirect, render

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





def encode_file(file):
    return base64.b64encode(file.read()).decode("ascii")


def identify_plant(file_names):
    params = {
        "images": [encode_file(img) for img in file_names],
        "latitude": 49.1951239,
        "longitude": 16.6077111,
        "datetime": 1582830233,
        "modifiers": ["crops_fast", "similar_images"],
        "plant_language": "en",
        "plant_details": [
            "common_names",
            "edible_parts",
            "gbif_id",
            "name_authority",
            "propagation_methods",
            "synonyms",
            "taxonomy",
            "url",
            "wiki_description",
            "wiki_image",
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": "jfv3A4l2CwtF2Bs5b7XSoz5DdgDeKFqNnKSS7UwyGnnGozcvF7",
    }

    response = requests.post("https://api.plant.id/v2/identify", json=params, headers=headers)

    return response.json()


def plant_scan(request):
    if request.method == 'POST':
        # Retrieve the uploaded image file
        image_file = request.FILES['plant-image']

        # Identify the plant based on the uploaded image
        identified_plant = identify_plant([image_file])

        if identified_plant.get('suggestions'):
            # Retrieve the identified plant details
            plant_details = identified_plant['suggestions'][0]['plant_details']
            
            # Retrieve the relevant plant information
            common_names = plant_details.get('common_names')
            edible_parts = plant_details.get('edible_parts')
            gbif_id = plant_details.get('gbif_id')
            name_authority = plant_details.get('name_authority')
            propagation_methods = plant_details.get('propagation_methods')
            synonyms = plant_details.get('synonyms')
            taxonomy = plant_details.get('taxonomy')
            url = plant_details.get('url')
            wiki_description = plant_details.get('wiki_description')
            wiki_image = plant_details.get('wiki_image')


            # Save the plant information to the database
            plant = Plant(
                common_names=common_names,
                edible_parts=edible_parts,
                gbif_id=gbif_id,
                name_authority=name_authority,
                propagation_methods=propagation_methods,
                synonyms=synonyms,
                taxonomy=taxonomy,
                url=url,
                wiki_description=wiki_description,
                wiki_image=wiki_image,
                user=request.user
            )

            plant.save()

            return redirect('plant_save')
        else:
            # Handle the case when the plant cannot be identified
            return HttpResponse('Plant identification failed.')

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

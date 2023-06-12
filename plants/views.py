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
            try:
                if len(common_names) == 0 and common_names is not None:
                    common_names_str = common_names[0]
                elif common_names is None:
                    common_names_str = "None"
                else:
                    common_names_str = ', '.join(common_names)
            except Exception:
                common_names_str = ""

            try:
                if len(edible_parts) == 0 and edible_parts is not None:
                    edible_parts_str = edible_parts[0]
                elif edible_parts is None:
                    edible_parts_str = "None"
                else:
                    edible_parts_str = ', '.join(edible_parts)
            except Exception:
                edible_parts_str = ""

            try:
                if len(propagation_methods) == 0 and propagation_methods is not None:
                    propagation_methods_str = propagation_methods[0]
                elif propagation_methods is None:
                    propagation_methods_str = "None"
                else:
                    propagation_methods_str = ', '.join(propagation_methods)
            except Exception:
                propagation_methods_str = ""

            taxonomy_str = ', '.join([f"{key}: {value}" for key, value in taxonomy.items()])
            wiki_description_str = ', '.join([f"{key}: {value}" for key, value in wiki_description.items()])

            plant = Plant(
                common_names=common_names_str,
                edible_parts=edible_parts_str,
                gbif_id=gbif_id,
                name_authority=name_authority,
                propagation_methods=propagation_methods_str,
                synonyms=synonyms,
                taxonomy=taxonomy_str,
                url=url,
                wiki_description=wiki_description_str,
                wiki_image=wiki_image['value'],
                real_image=image_file,
                user=request.user
            )


            plant.save()

            return redirect('plant_save')
        else:
            # Handle the case when the plant cannot be identified
            return HttpResponse('Plant identification failed.')

    return render(request, 'scan.html')


def plant_save(request):
    user_plants = Plant.objects.filter(user=request.user)

    context = {
        'user_plants': user_plants,
    }
    
    return render(request, 'save.html',context)

def contribution_system(request):
    # Retrieve information about planting locations, growth details, and green points
    locations = ["Location A", "Location B", "Location C"]
    growth_details = ["Growth detail 1", "Growth detail 2", "Growth detail 3"]
    green_points = 100

    return render(request, 'contribution.html', {'locations': locations, 'growth_details': growth_details,
                                                 'green_points': green_points})



def tree_map(request):
    # Retrieve tree locations and display them on a map
    tree_locations = ["Location X", "Location Y", "Location Z"]
    return render(request, 'treemap.html', {'tree_locations': tree_locations})

def plant_library(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        api_key = 'sk-JOi7648733bf8684b1232'
        url = f'https://perenual.com/api/species-list?key={api_key}&q={query}'

        try:
            response = requests.get(url)
            data = response.json()
            json_data = data['data'][0]
            json_data2 = data['data'][1]
            json_data3 = data['data'][2]
            # context = {'species_list': species_list}
            print(json_data)
            try :
                t = json_data['image_links']['thumbnail']
            except Exception:
                t = "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg"
            context = {
        'common_name': json_data['common_name'],
        'scientific_name': json_data['scientific_name'],
        'other_name': json_data['other_name'],
        'cycle': json_data['cycle'],
        'watering': json_data['watering'],
        'sunlight': json_data['sunlight'],
        'image_links': {
            
            'thumbnail': t
            

        }}
            context1 = {
            'common_name': json_data['common_name'],
            'scientific_name': json_data['scientific_name'],
            'other_name': json_data['other_name'],
            'cycle': json_data['cycle'],
            'watering': json_data['watering'],
            'sunlight': json_data['sunlight']
            }
            
            context2 = {
            'common_name': json_data['common_name'],
            'scientific_name': json_data['scientific_name'],
            'other_name': json_data['other_name'],
            'cycle': json_data['cycle'],
            'watering': json_data['watering'],
            'sunlight': json_data['sunlight']
           
        }
        except requests.exceptions.RequestException as e:
            # Handle API request errors
            context = {'error_message': 'Failed to retrieve species data.'}
    else:
        context = {}
        context1 = {}
        context2 = {}
        

    return render(request, 'library.html', {
        'context': context,
        'context1': context1,
        'context2': context2
    })
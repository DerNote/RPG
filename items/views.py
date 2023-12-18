from django.shortcuts import render, redirect, get_object_or_404
from .models import Items_collection, Feats_collection, Flaws_collection, Player_collection
from django.http import HttpResponse, JsonResponse, QueryDict
from django.template import loader
from django.contrib import messages
import random, time, json
from .forms import PlayerForm

# Create your views here.

Feat_stuff = list(Feats_collection.find())
Active_stuff = list(Items_collection.find({}, {'_id': 0, 'Name': 1, 'Description': 1, 'Tag': 1}))

def index(request):
    Items = Items_collection.find()
    Players = Player_collection.find()
    Players2 = Player_collection.find()
    return render(request, 'base.html', {'Items': Items, 'Feats': Feat_stuff, 'Players':Players, 'Players2':Players2, "room_name": "RPG"})

def login(request):
    return render(request, 'items/login.html')

def rederect(request):
    response = redirect('RPG/')
    return response

def compendium(request):
    Items = Items_collection.find()
    items_exist = bool(Items) if Items is not None else False
    Feats = Feats_collection.find()
    feats_exist = bool(Feats) if Feats is not None else False
    Flaws = Flaws_collection.find()
    flaws_exist = bool(Flaws) if Flaws is not None else False
    return render(request, 'items/compendium.html', {'Items': Items, 'items_exist': items_exist, 'Feats': Feats, 'feats_exist':feats_exist, 'Flaws':Flaws, 'flaws_exist':flaws_exist})

def randominium(request):
    random.seed(time.time())
    rand = random.randrange(20)
    response_data = {'message': rand}
    return JsonResponse(response_data)

def Player(request, name):
    player_data = Player_collection.find_one({'Player': name})
    return render(request, "items/Player_view.html", {'player_data':player_data})  

def Edit_character(request, name):
    player_data = Player_collection.find_one({'Player': name})
    player_name = player_data['Player']
    Test_data = (Player_collection.find_one({'Player': name}, {'_id': 0, 'Name': 1,'Feats':1,'Equipment':1,'Pouch':1,'Hp_current':1,'Hp_max':1}))
    initial_data = {'name':Test_data['Name'],'hp_current':Test_data['Hp_current'], 'hp_max':Test_data['Hp_max'], 'main': Test_data['Equipment']['Gear']['Main'], 'secondary':Test_data['Equipment']['Gear']['Secondary']}
    for index, item in enumerate(Test_data['Pouch'], start=1):
        initial_data[f'knap{index}'] = item['Name']
    for index, feat in enumerate(Test_data['Feats'], start=1):
        initial_data[f'Feats{index}'] = feat['Name']
    for index, active in enumerate(Test_data['Equipment']['Active'], start=1):
        initial_data[f'Active{index}']= active['Name']
    form = PlayerForm(initial=initial_data)
    return render(request, "items/Player_edit.html", {"form": form,'player_data':player_data, 'player_name': player_name})

def update(request, name):  
    if request.method == 'POST':
        Test=request.POST

        def update_description(feats_key, Feat_stuff):
            feats_values = [{"Name": value} for key, value_list in Test.lists() if key.startswith(feats_key) for value in value_list]
            for feat_value in feats_values:
                for feat_stuff in Feat_stuff:
                    if "Name" in feat_value and feat_value["Name"] == feat_stuff["Name"]:
                        feat_value["Description"] = feat_stuff.get("Description", "")
            return feats_values
        
        def find_desc(name, list):
            desc=''
            for items in list:
                if items["Name"] == name:
                    desc=items["Description"]
            return desc
        
        feat_list=update_description("Feats", Feat_stuff)     
        active_list=update_description("Active", Active_stuff)
        main_name=Test.get('Main_weapon', '')
        main_desc=find_desc(main_name, Active_stuff)
        secondary_name=Test.get('Secondary_weapon', '')
        secondary_desc=find_desc(secondary_name, Active_stuff)
        Pouch = [{"Name": value} for key, value_list in Test.lists() if key.startswith('knap') for value in value_list]
        
        json_data = {
            'Name': Test.get('name', ''),
            'Feats': feat_list,
            'Equipment': {
                'Gear': {
                    'Main': main_name,
                    'MainDescription':main_desc,
                    'Secondary': secondary_name,
                    'SecondaryDescription':secondary_desc
                },
                'Active': active_list
            },
            'Pouch': Pouch,
            'Player': name,
            'Hp_current': Test.get('hp_current', 0),
            'Hp_max': Test.get('hp_max', 0)
        } 
        query = {'Player': name}
        new_values = {'$set': json_data}
        Player_collection.update_one(query, new_values)
        player_datax = Player_collection.find_one({'Player': name}, {'_id': 0, 'Player': 1})
        return redirect('view', player_datax["Player"])
    else:
        player_datax = Player_collection.find_one({'Player': name}, {'_id': 0, 'Name': 1,'Feats':1,'Equipment':1,'Pouch':1,'Hp_current':1,'Hp_max':1, 'Player': 1})
        return redirect('view', player_datax["Player"])
    
def iframe_test(request):
    return render(request, 'items/iframe_test.html')
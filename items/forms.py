from django import forms
from .models import Player, Feats_collection, Items_collection


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

        # Create form fields based on the JSON data structure
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.get('initial', None)
        super().__init__(*args, **kwargs)

        # Create form fields based on the JSON data structure
        for i in range(5):
            field_name = f'knap{i+1}'  # Create field names like pouch_0, pouch_1, ..., pouch_4
            self.fields[field_name] = forms.CharField(label=f'Pouch {i+1}')
            
        feats_collection= Feats_collection.find({}, {'_id': 0, 'Name': 1})
        items_collection= list(Items_collection.find({}, {'_id': 0, 'Name': 1, 'Tag': 1}))
        # Get the Feats names from the collection and create choices for dropdown fields
        feats_data = [{'Name': feat['Name']} for feat in feats_collection]
        items_data = [{'Name': item['Name']} for item in items_collection]

        # Create form fields for Feats dropdowns
        feats_fields = [key for key in initial_data if key.startswith('Feats')]
        for idx, field_name in enumerate(feats_fields, start=1):
            field_value = initial_data.get(field_name)
            choices = [(feat['Name'], feat['Name']) for feat in feats_data]
            self.fields[field_name] = forms.ChoiceField(
                label=f'Feat {idx}',
                choices=choices,
                initial=field_value,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
            
        Active_fields = [key for key in initial_data if key.startswith('Active')]
        for idx, field_name in enumerate(Active_fields, start=1):
            field_value = initial_data.get(field_name)
            choices = [(active['Name'], active['Name']) for active in items_data]
            self.fields[field_name] = forms.ChoiceField(
                label=f'Active {idx}',
                choices=choices,
                initial=field_value,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        main_weapon_data = [{'Name': item['Name']} for item in items_collection if item['Tag'] in ['1', '3']]
        main_weapon_choices = [(item['Name'], item['Name']) for item in main_weapon_data]
        Main_fields = initial_data.get('main') if initial_data else None,
        self.fields['Main_weapon'] = forms.ChoiceField(
            label='Main',
            choices=main_weapon_choices,
            initial=Main_fields,
            widget=forms.Select(attrs={'class': 'form-control'})
            )
        secondary_weapon_data = [{'Name': item['Name']} for item in items_collection if item['Tag'] in ['2', '3']]
        secondary_weapon_choices = [(item['Name'], item['Name']) for item in secondary_weapon_data]
        Secondary_fields = initial_data.get('secondary') if initial_data else None,
        self.fields['Secondary_weapon'] = forms.ChoiceField(
            label='Secondary',
            choices=secondary_weapon_choices,
            initial=Secondary_fields,
            widget=forms.Select(attrs={'class': 'form-control'})
            )
        
        
    def clean(self):
        cleaned_data = super().clean()
        pouch_data = []

        # Gather cleaned data back into JSON format
        for i in range(5):
            field_name = f'knap{i+1}'
            pouch_item = {'Name': cleaned_data.get(field_name, '')}
            pouch_data.append(pouch_item)

        cleaned_data['pouch'] = pouch_data
        return cleaned_data

# your_app/management/commands/fetch_heroes.py
import requests
from django.core.management.base import BaseCommand
from core.models import Hero, Transformation, Costume, Ability
from decouple import config
import pdb

class Command(BaseCommand):
    help = 'Fetch hero data from the API and store it in the database'

    def handle(self, *args, **kwargs):

        url = 'https://marvelrivalsapi.com/api/v1/heroes'
        api_key = config('API_KEY')

        # Set up the header with the API key
        headers = {
            'x-api-key': f'{api_key}',
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            heroes_data = response.json()  # Assuming response is in JSON format
            for hero in heroes_data:  # The root is an array of heroes
                # Create or update hero
                hero_obj, created = Hero.objects.update_or_create(
                    id=hero['id'],
                    defaults={
                        'name': hero['name'],
                        'real_name': hero['real_name'],
                        'image_url': hero['imageUrl'],
                        'role': hero['role'],
                        'attack_type': hero['attack_type'],
                        'team': hero['team'],
                        'difficulty': hero['difficulty'],
                        'bio': hero['bio'],
                        'lore': hero['lore'],
                    }
                )
                # Handle transformations
                for transformation in hero['transformations']:
                    # Check if 'id' exists in the transformation data
                    if 'id' not in transformation:
                        self.stdout.write(self.style.ERROR(f"Missing 'id' field in transformation data for hero {hero['name']}"))
                        continue  # Skip if 'id' is missing
                    # Use the 'id' to get or create the transformation
                    transformation_obj, created = Transformation.objects.get_or_create(
                        id=transformation['id'],  # Use the 'id' from the API
                        defaults={
                            'name': transformation.get('name', ''),  # Name field, could be empty
                            'icon': transformation.get('icon', ''),
                            'health': transformation.get('health', 0),
                            'movement_speed': transformation.get('movement_speed', 0),
                            'hero': hero_obj  # Link transformation to hero,
                        }
                    )
                    transformation_obj.save()
                    # Output result for each transformation
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Transformation {transformation['id']} added."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Transformation {transformation['id']} updated."))
                    
                # Handle costumes
                for costume in hero.get('costumes', []):
                    if 'id' not in costume:
                        continue  # Ensure ID exists before processing
                    quality = costume.get('quality', {})
                    costume_obj, _ = Costume.objects.update_or_create(
                        id=costume['id'],
                        defaults={
                            'hero': hero_obj,  # Link to the correct hero
                            'name': costume.get('name', ''),
                            'image_url': costume.get('imageUrl', ''),
                            'description': costume.get('description', 'No description available'),
                            'appearance': costume.get('appearance', 'No appearance data available'),
                            'quality_name': quality.get('name', 'Unknown'),
                            'quality_color': quality.get('color', 'gray'),
                            'quality_value': quality.get('value', 1),
                            'quality_icon': quality.get('icon', ''),
                        }
                    )
                    # Add the costume to the hero's costumes
                    hero_obj.costumes.add(costume_obj)

                # Handle abilities
                for ability in hero.get('abilities', []):
                    if 'id' not in ability:
                        continue  # Ensure ID exists before processing
                    additional_fields = ability.get('additional_fields', {})
                    ability_obj, _ = Ability.objects.update_or_create(
                        id=ability['id'],
                        defaults={
                            'hero': hero_obj,  # Link to the correct hero
                            'name': ability.get('name', ''),
                            'icon': ability.get('icon', ''),
                            'type': ability.get('type', 'Normal'),
                            'is_collab': ability.get('isCollab', False),
                            'key': additional_fields.get('Key', ''),
                            'damage': additional_fields.get('Damage', '0'),
                            'casting': additional_fields.get('Casting', ''),
                            'cooldown': additional_fields.get('Cooldown', '0s'),
                            'projectile_speed': additional_fields.get('Projectile Speed', '0m/s'),
                        }
                    )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Hero {hero['name']} added."))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Hero {hero['name']} updated."))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from the API'))

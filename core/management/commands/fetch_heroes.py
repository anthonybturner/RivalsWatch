import requests
import json
from django.core.management.base import BaseCommand
from core.models import Hero, Transformation, Costume, Ability
from decouple import config

class Command(BaseCommand):
    help = "Fetch hero data from the API and store/update it in the database"

    def handle(self, *args, **kwargs):
        url = "https://marvelrivalsapi.com/api/v1/heroes"
        api_key = config("API_KEY")

        headers = {"x-api-key": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an error for non-200 responses
            heroes_data = response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"API Request failed: {e}"))
            return

        for hero in heroes_data:
            try:
                hero_obj, created = Hero.objects.update_or_create(
                    id=hero["id"],
                    defaults={
                        "name": hero["name"],
                        "real_name": hero["real_name"],
                        "image_url": hero["imageUrl"],
                        "role": hero["role"],
                        "attack_type": hero["attack_type"],
                        "team": hero["team"],
                        "difficulty": hero["difficulty"],
                        "bio": hero["bio"],
                        "lore": hero["lore"],
                    },
                )

                self.stdout.write(self.style.SUCCESS(f"Hero {'added' if created else 'updated'}: {hero['name']}"))

                # Process transformations
                for transformation in hero.get("transformations", []):
                    if "id" not in transformation:
                        self.stderr.write(self.style.WARNING(f"Skipping transformation for {hero['name']} (missing ID)"))
                        continue
                    Transformation.objects.update_or_create(
                        id=transformation["id"],
                        defaults={
                            "name": transformation.get("name", ""),
                            "icon": transformation.get("icon", ""),
                            "health": transformation.get("health", 0),
                            "movement_speed": transformation.get("movement_speed", 0),
                            "hero": hero_obj,
                        },
                    )

                # Process costumes
                for costume in hero.get("costumes", []):
                    if "id" not in costume:
                        continue
                    Costume.objects.update_or_create(
                        id=costume["id"],
                        defaults={
                            "hero": hero_obj,
                            "name": costume.get("name", ""),
                            "image_url": costume.get("imageUrl", ""),
                            "description": costume.get("description", "No description available"),
                            "appearance": costume.get("appearance", "No appearance data available"),
                            "quality_name": costume.get("quality", {}).get("name", "Unknown"),
                            "quality_color": costume.get("quality", {}).get("color", "gray"),
                            "quality_value": costume.get("quality", {}).get("value", 1),
                            "quality_icon": costume.get("quality", {}).get("icon", ""),
                        },
                    )

                # Process abilities
                for ability in hero.get("abilities", []):
                    if "id" not in ability:
                        continue
                    Ability.objects.update_or_create(
                        id=ability["id"],
                        defaults={
                            "hero": hero_obj,
                            "name": ability.get("name", ""),
                            "icon": ability.get("icon", ""),
                            "type": ability.get("type", "Normal"),
                            "is_collab": ability.get("isCollab", False),
                            "key": ability.get("additional_fields", {}).get("Key", ""),
                            "damage": ability.get("additional_fields", {}).get("Damage", "0"),
                            "casting": ability.get("additional_fields", {}).get("Casting", ""),
                            "cooldown": ability.get("additional_fields", {}).get("Cooldown", "0s"),
                            "projectile_speed": ability.get("additional_fields", {}).get("Projectile Speed", "0m/s"),
                        },
                    )

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing hero {hero['name']}: {e}"))

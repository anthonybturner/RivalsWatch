import requests
from django.core.management.base import BaseCommand
from core.models import DeveloperDiary
from decouple import config
from datetime import datetime

class Command(BaseCommand):
    help = "Fetch news data from the API and store/update it in the database"

    def handle(self, *args, **kwargs):
        url = "https://marvelrivalsapi.com/api/v1/dev-diaries"
        api_key = config("API_KEY")
        headers = {"x-api-key": api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an error for non-200 responses
            data = response.json()
            dev_diaries_data = data.get("formatted_entries", [])
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"API Request failed: {e}"))
            return
        for diary in dev_diaries_data:
            try:
                # Convert the date format from YYYY/MM/DD to YYYY-MM-DD
                date_str = diary.get("date", "")
                try:
                    # Try to convert the date
                    date_obj = datetime.strptime(date_str, "%Y/%m/%d")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    # If the conversion fails, print an error and continue
                    self.stderr.write(self.style.ERROR(f"Invalid date format for diary: {diary['title']}"))
                    continue
                # Use update_or_create() with a unique identifier (like title or id)
                diary_obj, created = DeveloperDiary.objects.update_or_create(
                    title=diary.get("title", ""),  # Use title to look up existing records
                    defaults={
                        "date": formatted_date,
                        "overview": diary.get("overview", ""),
                        "image_path": diary.get("imagePath", ""),
                        "full_content": diary.get("fullContent", ""),
                    },
                )
                self.stdout.write(self.style.SUCCESS(f"Diary {'added' if created else 'updated'}: {diary['title']}"))
            except KeyError as e:
                self.stderr.write(self.style.ERROR(f"Missing key {e} in diary data"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing diary {diary.get('title', 'Unknown')}: {e}"))


import requests
from django.core.management.base import BaseCommand
from core.models import MatchHistory, Player, ScoreInfo, Hero
from decouple import config
from utilities.converter import seconds_minutes
from core.models.match_history import MatchPlayer, IsWin
import ast
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = "Fetch match history data from the API and store/update it in the database"
    
    def save_score_info(match):
        score_info_data = match.get("score_info", {})

        # Check if score_info_data is a valid dictionary and contains numeric values
        if isinstance(score_info_data, dict):
            # Ensure all values are integers and the keys are valid
            try:
                scores = {key: int(value) for key, value in score_info_data.items()}
            except ValueError:
                raise ValidationError("Invalid score data. All values should be integers.")
            
            score_total = sum(scores.values())  # Aggregate the total score from the dictionary

            # Store in the database (example logic, modify as needed)
            score_info_obj, created = ScoreInfo.objects.update_or_create(
                match_uid=match.get("match_uid", ""),  # Use match_uid as a unique identifier
                defaults={"score": score_total, "score_info": str(scores)}  # Store as a string representation of the dictionary
            )
        else:
            # In case of invalid data format (e.g., not a dictionary)
            score_total = 0
            score_info = "{}"  # Store an empty dictionary as a string
            score_info_obj, created = ScoreInfo.objects.update_or_create(
                match_uid=match.get("match_uid", ""),  # Ensure match_uid is present
                defaults={"score": score_total, "score_info": score_info}
            )

    def handle(self, *args, **kwargs):
        url = "https://marvelrivalsapi.com//api/v1/player/SilentCoder/match-history?season=2&skip=20&game_mode=0"
        api_key = config("API_KEY")
        headers = {"x-api-key": api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an error for non-200 responses
            data = response.json()
            match_history_data = data.get("match_history", [])
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"API Request failed: {e}"))
            return

        for match in match_history_data:
            try:
                # Handle score_info
                score_info_data = match.get("score_info", {})
                # Check if score_info_data is a valid dictionary and contains numeric values
                if isinstance(score_info_data, dict):
                    # Ensure all values are integers and the keys are valid
                    try:
                        scores = {key: int(value) for key, value in score_info_data.items()}
                    except ValueError:
                        raise ValidationError("Invalid score data. All values should be integers.")
                    
                    score_total = sum(scores.values())  # Aggregate the total score from the dictionary

                    # Store in the database (example logic, modify as needed)
                    score_info_obj, created = ScoreInfo.objects.update_or_create(
                        match_uid=match.get("match_uid", ""),  # Use match_uid as a unique identifier
                        defaults={"score": score_total, "score_info": str(scores)}  # Store as a string representation of the dictionary
                    )
                else:
                    # In case of invalid data format (e.g., not a dictionary)
                    score_total = 0
                    score_info = "{}"  # Store an empty dictionary as a string
                    score_info_obj, created = ScoreInfo.objects.update_or_create(
                        match_uid=match.get("match_uid", ""),  # Ensure match_uid is present
                        defaults={"score": score_total, "score_info": score_info}
                    )
                
                player_obj, _ = Player.objects.update_or_create(
                    player_uid=match.get("match_player", {}).get("player_uid", ""),
                )
                 
                 # Handle match player data
                is_win_data = match.get("match_player", {}).get("is_win", {})
                is_win_instance = IsWin.objects.create(
                    score=is_win_data.get("score", 0),  # Default to 0 if "score" doesn't exist
                    is_win=is_win_data.get("is_win", False)  # Default to False if "is_win" doesn't exist
                )
                match_player = MatchPlayer.objects.update_or_create(
                    player=player_obj,
                    assists=match.get("match_player", {}).get("assists", 0),  # Default to 0 if "assists" is not present
                    kills=match.get("match_player", {}).get("kills", 0),  # Default to 0 if "kills" is not present
                    deaths=match.get("match_player", {}).get("deaths", 0),  # Default to 0 if "deaths" is not present
                    is_win=is_win_instance  # Linking to the IsWin instance
                )
                
                # Handle player data
                player_hero_data = match.get("player_hero", {})
                # Assuming you already have a Hero with a matching `hero_id`
                try:
                    player_hero = Hero.objects.get(id=player_hero_data.get("hero_id"))
                except Hero.DoesNotExist:
                    player_hero = None  # Set to None if hero doesn't exist

               
                
                # Handle match history data
                match_camp = match.get("camp", 0),
                # Ensure camp is a valid integer, or set a fallback value if necessary
                if match_camp not in [0, 1]:  # Assuming camp can only be 0 or 1
                    match_camp = 0  # Default to 0 if the value is invalid
                # Now handle match history object and link player
                match_obj, created = MatchHistory.objects.update_or_create(
                    match_uid=match.get("match_uid", ""),
                    defaults={
                        "match_map_id": match.get("match_map_id", 0),
                        "map_thumbnail": match.get("map_thumbnail", ""),
                        "match_play_duration": seconds_minutes(match.get("match_play_duration", "")),
                        "match_season": match.get("match_season", 0),
                        "match_uid": match.get("match_uid", ""),
                        "match_winner_side": match.get("match_winner_side", -1),
                        "mvp_uid": match.get("mvp_uid", ""),
                        "svp_uid": match.get("svp_uid", ""),
                        "score_info": score_info_obj,
                        "match_time_stamp": match.get("match_time_stamp", 0),
                        "play_mode_id": match.get("play_mode_id", 0),
                        "game_mode_id": match.get("game_mode_id", 0),
                      # "match_player": match_player,
                        "disconnected": match.get("disconnected", False),
                        "camp": match_camp,
                        "player_hero": player_hero,
                        "player": player_obj,
                    },
                )

                self.stdout.write(self.style.SUCCESS(f"Match {'added' if created else 'updated'}: {match['match_uid']}"))

            except KeyError as e:
                self.stderr.write(self.style.ERROR(f"Missing key {e} in match data"))
            except Hero.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Hero with ID {player_hero_data.get('hero_id')} does not exist"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing match {match.get('match_uid', 'Unknown')}: {e}"))

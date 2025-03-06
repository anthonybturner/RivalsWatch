import requests
from django.core.management.base import BaseCommand
from core.models import MatchHistory, Player, ScoreInfo, Hero
from decouple import config

class Command(BaseCommand):
    help = "Fetch match history data from the API and store/update it in the database"

    def handle(self, *args, **kwargs):
        url = "https://marvelrivalsapi.com//api/v1/player/1737805188/match-history?season=1&skip=20&game_mode=0"
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
                if score_info_data:
                    score = score_info_data.get("score", 0)  # Default to 0 if score is missing
                    score_info = score_info_data.get("score_info", "")  # Default to empty string if not available
                    score_info_obj, _ = ScoreInfo.objects.update_or_create(
                        score=score, defaults={"score_info": score_info}
                    )
                else:
                    score = 0
                    score_info = ""
                    score_info_obj, _ = ScoreInfo.objects.update_or_create(
                        score=score, defaults={"score_info": score_info}
                    )

                # Handle player data
                player_data = match.get("match_player", {})
                if player_data:
                    player_hero_data = player_data.get("player_hero", {})
                else:
                    player_hero_data = {}

                # Assuming you already have a Hero with a matching `hero_id`
                try:
                    player_hero = Hero.objects.get(id=player_hero_data.get("hero_id"))
                except Hero.DoesNotExist:
                    player_hero = None  # Set to None if hero doesn't exist

                player_obj, _ = Player.objects.update_or_create(
                    player_uid=player_data.get("player_uid", ""),
                    defaults={
                        "assists": player_data.get("assists", 0),
                        "kills": player_data.get("kills", 0),
                        "deaths": player_data.get("deaths", 0),
                        "is_win": player_data.get("is_win", False),
                        "disconnected": player_data.get("disconnected", False),
                        "camp": player_data.get("camp", ""),
                        "score_info": score_info_obj,
                        "player_hero": player_hero,
                    },
                )

                # Now handle match history object and link player
                match_obj, created = MatchHistory.objects.update_or_create(
                    match_uid=match.get("match_uid", ""),
                    defaults={
                        "match_map_id": match.get("match_map_id", 0),
                        "map_thumbnail": match.get("map_thumbnail", ""),
                        "match_play_duration": match.get("match_play_duration", ""),
                        "match_season": match.get("match_season", 0),
                        "match_winner_side": match.get("match_winner_side", ""),
                        "mvp_uid": match.get("mvp_uid", ""),
                        "svp_uid": match.get("svp_uid", ""),
                        "score_info": score_info_obj,
                        "match_time_stamp": match.get("match_time_stamp", 0),
                        "play_mode_id": match.get("play_mode_id", 0),
                        "game_mode_id": match.get("game_mode_id", 0),
                        "match_player": player_obj,
                    },
                )

                self.stdout.write(self.style.SUCCESS(f"Match {'added' if created else 'updated'}: {match['match_uid']}"))

            except KeyError as e:
                self.stderr.write(self.style.ERROR(f"Missing key {e} in match data"))
            except Hero.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Hero with ID {player_hero_data.get('hero_id')} does not exist"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing match {match.get('match_uid', 'Unknown')}: {e}"))

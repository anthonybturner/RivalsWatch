import requests
from django.core.management.base import BaseCommand
from core.models import MatchHistory, MatchDetails, ScoreInfo, Hero,Player, PlayerHero, MatchesPlayer, MatchPlayer, IsWin, GameMode
from decouple import config
from utilities.converter import seconds_minutes
from django.core.exceptions import ValidationError

class PlayerDataFetcher:
    def __init__(self):
        self.api_key = config("API_KEY")
        self.headers = {"x-api-key": self.api_key}  # Instance attribute

    def fetch_match_data(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

class Command(BaseCommand):
    help = "Fetch match history data from the API and store/update it in the database"
   
    def handle(self, *args, **kwargs):
        fetcher = PlayerDataFetcher()
        url = "https://marvelrivalsapi.com/api/v1/player/SilentCoder/match-history?season=2&skip=20&game_mode=0"
        data = fetcher.fetch_match_data(url)
        match_history_data = data.get("match_history", [])
        for match in match_history_data:
            try:
                match_details = self.get_match_details(fetcher, match)
                
                # Handle score_info
                # Check if score_info_data is a valid dictionary and contains numeric values
                score_info_obj = self.get_score_info(match)
                
                player_obj = self.get_player(match)
                 
                 # Handle match player data
                is_win_instance = self.get_win_data(match)
                    
                matches_player = MatchesPlayer.objects.create(
                    player=player_obj,  # The player to associate with
                    assists=match.get("match_player", {}).get("assists", 0),
                    kills=match.get("match_player", {}).get("kills", 0),
                    deaths=match.get("match_player", {}).get("deaths", 0),
                    is_win=is_win_instance,  # Link to the is_win instance for this match
                )
                
                # Handle player data
                player_hero_data = match.get("match_player", {}).get("player_hero", {})
                # Assuming you already have a Hero with a matching `hero_id`
                hero = self.get_hero_data(matches_player, player_hero_data)
              
                # Handle match history data
                match_camp = match.get("camp", 0)
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
                        "match_details":  match_details,
                        "match_winner_side": match.get("match_winner_side", -1),
                        "mvp_uid": match.get("mvp_uid", ""),
                        "svp_uid": match.get("svp_uid", ""),
                        "score_info": score_info_obj,
                        "match_time_stamp": match.get("match_time_stamp", 0),
                        "play_mode_id": match.get("play_mode_id", 0),
                        "game_mode_id": match.get("game_mode_id", 0),
                        "matches_player": matches_player,
                        "disconnected": match.get("disconnected", False),
                        "camp": match_camp,
                        "player_hero": hero,
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

    def get_hero_data(self, matches_player, player_hero_data):
        try:
            hero = Hero.objects.get(id=player_hero_data.get("hero_id"))
                    # Assuming `PlayerHero` is a model that links the `Hero` to the player in a match
            player_hero, created = PlayerHero.objects.get_or_create(
                        hero_id=hero.id,  # Unique identifier for the hero
                        hero_name=hero.name,  # Name of the hero
                        hero_type=hero.image_url,  # URL to the hero's image or type
                        defaults={
                            'kills': player_hero_data.get('kills', 0),
                            'deaths': player_hero_data.get('deaths', 0),
                            'assists': player_hero_data.get('assists', 0),
                            'play_time': player_hero_data.get('play_time', 0),
                            'total_hero_damage': player_hero_data.get('total_hero_damage', 0),
                            'total_damage_taken': player_hero_data.get('total_damage_taken', 0),
                            'total_hero_heal': player_hero_data.get('total_hero_heal', 0),
                        }
                    )

                    # Now assign the PlayerHero instance to the MatchesPlayer
            matches_player.player_hero = player_hero
            matches_player.save()
                
        except Hero.DoesNotExist:
            player_hero = None  # Set to None if the hero doesn't exist
            matches_player.player_hero = player_hero
            matches_player.save()
        return hero

    def get_player(self, match):
        player_obj, _ = Player.objects.update_or_create(
                    player_uid=match.get("match_player", {}).get("player_uid", ""),
                )
        
        return player_obj

    def get_win_data(self, match):
        is_win_data = match.get("match_player", {}).get("is_win", {})
        is_win_instance = IsWin.objects.create(
                    score=is_win_data.get("score", 0),  # Default to 0 if "score" doesn't exist
                    is_win=is_win_data.get("is_win", False)  # Default to False if "is_win" doesn't exist
                )
        
        return is_win_instance

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

    def get_match_details(self, fetcher, match):  
        match_uid=match.get("match_uid", "")
        url = f"https://marvelrivalsapi.com/api/v1/match/{match_uid}"
        data = fetcher.fetch_match_data(url)
        
        match_details_data = data.get("match_details", [])
        game_mode = self.get_game_mode(match_details_data)

        match_details, created = MatchDetails.objects.update_or_create(
            match_uid=match_details_data.get("match_uid", ""),
            defaults={
                "game_mode": game_mode, 
                "replay_id": match_details_data.get("replay_id", ""),
                "mvp_uid": match_details_data.get("mvp_uid", 0),
                "mvp_hero_id": match_details_data.get("mvp_hero_id", 0),
                "svp_uid": match_details_data.get("svp_uid", 0),
                "svp_hero_id": match_details_data.get("svp_hero_id", 0),
                "match_uid": match_uid,
            }
        )
        
        match_players = match_details_data.get("match_players", [])
        for match_player in match_players:
             # Try to fetch the Player object by player_uid
            try:
                player_uid = match_player.get("player_uid")
                player_obj = Player.objects.get(player_uid=player_uid)
            except Player.DoesNotExist:
                # Create the player if not exists
                player_obj = Player.objects.create(player_uid=player_uid, 
                                                name=match_player.get("nick_name", ""),
                                                )
                print(f"Created new player with player_uid {player_uid}.")
                
            # Update or create MatchesPlayer
            MatchPlayer.objects.update_or_create(
                player=player_obj,
                defaults={
                    "nick_name": match_player.get("nick_name"),
                    "player_icon": match_player.get("player_icon"),
                    "camp": match_player.get("camp", 0),
                    "cur_hero_id": match_player.get("cur_hero_id"),
                    "is_win": bool( match_player.get("is_win")),
                    "kills": match_player.get("kills", 0),  # Default to 0 if not present
                    "deaths": match_player.get("deaths", 0),  # Default to 0 if not present
                    "assists": match_player.get("assists", 0),  # Default to 0 if not present
                    "total_hero_damage": match_player.get("total_hero_damage", 0.0),  # Default to 0 if not present
                    "total_hero_heal": match_player.get("total_hero_heal", 0.0),  # Default to 0 if not present
                    "total_damage_taken": match_player.get("total_damage_taken", 0.0),  # Default to 0 if not present
                    "match" : match_details,
                    "player"  : player_obj,
                }
            )
        return match_details

    def get_game_mode(self, match_details):
        created_game_mode = None
        game_mode = match_details.get("game_mode", {})
        try:     
            game_mode_id = game_mode.get("game_mode_id", 0)
            game_mode_name = game_mode.get("game_mode_name", "")
            created_game_mode, _ = GameMode.objects.update_or_create(
                        game_mode_id=game_mode_id,
                        defaults={"game_mode_name": game_mode_name}
                    )
        except GameMode.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Game mode with ID {game_mode_id} does not exist"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error processing game mode: {e}"))
        return created_game_mode                

    def get_score_info(self, match):
        match_details_uid=match.get("match_uid", ""),  # Use match_uid as a unique identifier
        score_info_data = match.get("score_info", {})
        if isinstance(score_info_data, dict):
                    # Ensure all values are integers and the keys are valid
            try:
                scores = {key: int(value) for key, value in score_info_data.items()}
            except ValueError:
                raise ValidationError("Invalid score data. All values should be integers.")
                    
            score_total = sum(scores.values())  # Aggregate the total score from the dictionary

                    # Store in the database (example logic, modify as needed)
            score_info_obj, created = ScoreInfo.objects.update_or_create(
                        match_uid=match_details_uid,  # Use match_uid as a unique identifier
                        defaults={"score": score_total, "score_info": str(scores)}  # Store as a string representation of the dictionary
                    )
        else:
                    # In case of invalid data format (e.g., not a dictionary)
            score_total = 0
            score_info = "{}"  # Store an empty dictionary as a string
            score_info_obj, created = ScoreInfo.objects.update_or_create(
                        match_uid=match_details_uid,  # Ensure match_uid is present
                        defaults={"score": score_total, "score_info": score_info}
                    )
            
        return score_info_obj
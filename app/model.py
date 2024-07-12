from pydantic import BaseModel

class Score(BaseModel):
    home_team: int
    away_team: int
    class Config:
        schema_extra = {
            "example": {
                "home_team": 0,
                "away_team": 0
            }
        }

class Match(BaseModel):
    id: int
    sport: str
    tournament: str
    game_id: int
    game: str
    home_team: str
    away_team: str
    date_event: str
    status: int
    period: int
    firsthalf_score: Score
    fulltime_score: Score
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "sport": "Soccer",
                "tournament": "La Liga",
                "game_id": 1,
                "game": "Barcelona vs Real Madrid",
                "home_team": "Barcelona",
                "away_team": "Real Madrid",
                "date_event": "2021-09-01",
                "status": 0,
                "period": 0,
                "firsthalf_score": {
                    "home_team": 0,
                    "away_team": 0
                },
                "fulltime_score": {
                    "home_team": 0,
                    "away_team": 0
                }
            }
        }

class User(BaseModel):
    user: str
    password: str
    class Config:
        schema_extra = {
            "example": {
                "user": "user",
                "password": "password"
            }
        }


from typing import List
from fastapi import APIRouter, status, Request, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from model import Match

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
async def homepage():
    return "wellcome to the bbsw homepage"

@router.get("/api", response_description="All game", response_model=List[Match], tags=["Live"])
def retrieval(request: Request, token: str = Depends(oauth2_scheme)):
    matchs = list(request.app.collection.find(limit=100))
    return matchs

@router.get("/api/game_id/{game_id}", response_description="Get a game by id", response_model=Match)
def retrieval_by_game_id(game_id: int, request: Request):
    try:
        match = request.app.collection.find_one({"game_id": game_id})
        if not match:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
        return match
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/api/date/{date}", response_description="Get all game by date", response_model=List[Match])
def retrieval_by_date(date: str, request: Request):
    matchs = list(request.app.collection.find({"date_event": date}))
    if matchs == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return matchs

@router.post("/api/add", response_description="Add a new match", status_code=status.HTTP_201_CREATED, response_model=Match)
def insert_match(request: Request, match: Match):
    if request.app.collection.find_one({"game_id": match.game_id}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game_id already exists")
    match = jsonable_encoder(match)
    new_match = request.app.collection.insert_one(match)
    created_match = request.app.collection.find_one(
        {"_id": new_match.inserted_id}
    )
    return created_match
    
@router.put("/api/update/game_id/{game_id}", response_description="Update score", response_model=Match)
def update(game_id: int, request: Request, match: Match = Body(...)):
    match = {k: v for k, v in match.dict().items() if v is not None}
    if len(match) >= 1:
        update_result = request.app.collection.update_one(
            {"game_id": game_id}, {"$set": match}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    updated_match = request.app.collection.find_one({"game_id": game_id})
    return updated_match

@router.patch("/api/upsert/game_id/{game_id}", response_description="Upsert a game", response_model=Match)
def upsert(game_id: int, request: Request, match: Match = Body(...)):
    # match = {k: v for k, v in match.dict().items() if v is not None}
    match = jsonable_encoder(match)
    if match:
        update_result = request.app.collection.update_one(
            {"game_id": game_id}, {"$set": match}, upsert=True
        )
    if update_result.matched_count == 1:
        return request.app.collection.find_one({"game_id": game_id})
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail=match)

@router.patch("/api/upsert/date/{date}", response_description="Add multiple matches by date", status_code=status.HTTP_201_CREATED, response_model=List[Match])
def upsert_multi_game_id_by_date(date: str, request: Request, matchs: List[Match] = Body(...)):
    for match in matchs:
        match = jsonable_encoder(match)
        request.app.collection.update_one(
            {"game_id": match["game_id"], "date_event": date}, {"$set": match}, upsert=True
        )
    return matchs

@router.delete("/api/del/game_id/{game_id}", response_description="Delete a game")
def delete_match(game_id: int, request: Request):
    delete_result = request.app.collection.delete_one({"game_id": game_id})
    if delete_result.deleted_count == 1:
        return {"status": f"deleted game_id: {game_id}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game_id: {game_id} not found")

@router.delete("/api/del", response_description="Delete all game")
def delete_match_status(request: Request):
    delete_result = request.app.collection.delete_many({"status": 0})
    return {"status": f"deleted {delete_result.deleted_count} games"}

@router.delete("/api/delall", response_description="Delete all game")
def delete_all_match(request: Request):
    delete_result = request.app.collection.delete_many({})
    return {"status": f"deleted {delete_result.deleted_count} games"}


@router.patch("/api/updateall", response_description="Update all game", status_code=status.HTTP_201_CREATED, response_model=List[Match], tags=["Live"])
def update_all(request: Request, matches: List[Match], token: str = Depends(oauth2_scheme)): # , token: str = Depends(oauth2_scheme)
    ids = []
    if matches == []:
        return {"status": "No data to update"}
    for match in matches:
        match = jsonable_encoder(match)
        ids.append(match["id"])
        request.app.collection.update_one(
            {"game_id": match["game_id"]}, {"$set": match}, upsert=True
        )
    _ = request.app.collection.delete_many({"id": {"$nin": ids}})
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail=match)
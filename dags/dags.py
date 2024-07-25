from kingbets import fetch_kingbets_data, test
from livescore import fetch_livescore_data
from refresh_build_id import refresh
from merge_data import merge
from post_api import post
from utils import read_json

fetch_kingbets_data()
refresh()
fetch_livescore_data()
merge()
post()
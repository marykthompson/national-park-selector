import os
from dotenv import load_dotenv
import streamlit as st
import requests
import random

from typing import Union

from PIL import Image
from io import BytesIO

load_dotenv()

API_KEY = os.getenv("API_KEY")
HEADERS = {"X-Api-Key": API_KEY}

STATES_JSON = "states.json"
BASE_URL = "https://developer.nps.gov/api/v1/"
AREA = "parks"
SUBSET = "?stateCode="

# https://adamj.eu/tech/2021/06/14/python-type-hints-3-somewhat-unexpected-uses-of-typing-any-in-pythons-standard-library/
JSON = Union[int, str, float, bool, None, dict[str, "JSON"], list["JSON"]]
JSON_Object = dict[str, JSON]


@st.cache_data
def run_state_query(state: str) -> str:
    """Query the API and return json data"""
    endpoint = f"{BASE_URL}{AREA}{SUBSET}{state}"
    req = requests.get(endpoint, headers=HEADERS)
    reqdata = req.json()["data"]
    return reqdata


def run_image_query(url: str) -> Image:
    """Tries to retrieve an image, handling error if 404 not found"""
    image = Image.open(BytesIO(requests.get(url).content))
    return image


def get_random_image(reqdata: JSON_Object) -> Image:
    image_data = reqdata["images"]
    rand_N = random.randint(0, len(image_data) - 1)
    print(f"random N: {rand_N}")
    url = image_data[rand_N]["url"]
    image = run_image_query(url)
    return image

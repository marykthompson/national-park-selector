import json
import streamlit as st
import pandas as pd

STATES_JSON = "states.json"


@st.cache_data
def get_states() -> dict[str, str]:
    with open(STATES_JSON, "r") as f:
        states = json.load(f)

    states2 = {v: k for k, v in states.items()}
    return states2


def query_2_df(reqdata: dict[str, str], keys: list[str]) -> pd.DataFrame:
    data_sub = [{k: v for k, v in d.items() if k in keys} for d in reqdata]
    df = pd.DataFrame.from_records(data_sub)
    return df

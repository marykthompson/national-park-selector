import streamlit as st
from images import get_crop_box
from api import run_state_query, get_random_image
from utils import get_states, query_2_df

# Names of Columns for each park to display in the Streamlit app
DF_COLUMNS = {"fullName": "Park Name", "designation": "Park Type"}

# The number of images wide to use when displaying the selected parks
N_IMAGES_WIDE = 3

st.title("US National Parks By State")
states_dict = get_states()

option = st.selectbox(
    "Please select state",
    (states_dict.keys()),
)

st.write("You selected:", option)

query_data = run_state_query(states_dict[option])
# the JSON format returned is a list of dictionaries, one per park
# fullName = name of the park, parkCode=code of the park, images = list of images
# each image is a dictionary, with the data source in 'url'

df = query_2_df(query_data, list(DF_COLUMNS.keys()))
df.rename(columns=DF_COLUMNS, inplace=True)
df["Select?"] = False

df = st.data_editor(df, key="my_key", hide_index=True)

# Get the edited rows
edited_rows = st.session_state["my_key"]["edited_rows"]
index_selected = [int(row) for row in edited_rows if edited_rows[row]["Select?"]]
parks = df.iloc[index_selected]["Park Name"].values

# Get an image of each selected park and place in a grid
cols = st.columns(N_IMAGES_WIDE, vertical_alignment="bottom")

# in order to get images of the park, we need to know where in the JSON list
# is the data for that park
# this should correspond to the index in the park dataframe

i = 0
for idx in index_selected:
    park_data = query_data[idx]
    park_name = park_data["fullName"]
    image = get_random_image(park_data)
    crop_box = get_crop_box(image.size)
    image = image.crop(crop_box)

    col_num = i % N_IMAGES_WIDE
    # This puts the title on it, but it is really big
    # cols[col_num].title(park_name)

    # https://discuss.streamlit.io/t/change-font-size-and-font-color/12377/3
    TITLE_STRING = (
        '<p style="font-family:sans-serif; color:Green; font-size: 20px;">{TITLE}</p>'
    )
    cols[col_num].markdown(TITLE_STRING.format(TITLE=park_name), unsafe_allow_html=True)
    cols[col_num].image(image)
    i += 1

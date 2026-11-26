import streamlit as st
import pickle
import requests
import numpy as np

st.set_page_config(page_title="GOT Personality Matcher")

st.title("Game Of Thrones Personality Matcher")

# Fetch character data from API
try:
    response = requests.get(
        "https://thronesapi.com/api/v2/Characters",
        timeout=15
    )
    response.raise_for_status()
    api_data = response.json()

except requests.RequestException as e:
    st.error(f"Unable to fetch character images: {e}")
    st.stop()


# Load processed dataset
try:
    with open('data.pkl', 'rb') as file:
        df = pickle.load(file)

except Exception as e:
    st.error(f"Unable to load data.pkl: {e}")
    st.stop()


# Select top 25 characters
df = df.head(25).copy()

# Correct character names
df['character'] = df['character'].str.replace(
    'Jaime', 'Jamie', regex=False
)
df['character'] = df['character'].str.replace(
    'Lord Varys', 'Varys', regex=False
)
df['character'] = df['character'].str.replace(
    'Bronn', 'Lord Bronn', regex=False
)
df['character'] = df['character'].str.replace(
    'Sandor Clegane', 'The Hound', regex=False
)
df['character'] = df['character'].str.replace(
    'Robb Stark', 'Rob Stark', regex=False
)


# Fetch character image
def fetch_image(name, api_data):

    for item in api_data:

        if item['fullName'].strip().lower() == name.strip().lower():

            return item['imageUrl']

    return None


# Character selection
characters = df['character'].values

selected_character = st.selectbox(
    "Select a character",
    characters
)


# Calculate closest match
character_id = np.where(
    df['character'].values == selected_character
)[0][0]

x = df[['x', 'y']].values

distances = []

for i in range(len(x)):
    distances.append(
        np.linalg.norm(x[character_id] - x[i])
    )


recommended_id = sorted(
    list(enumerate(distances)),
    key=lambda x: x[1]
)[1][0]

recommended_character = df['character'].values[recommended_id]


# Fetch images
image_url = fetch_image(selected_character, api_data)

recommended_image_url = fetch_image(
    recommended_character, api_data
)


# Display results
col1, col2 = st.columns(2)

with col1:
    st.header(selected_character)

    if image_url:
        st.image(image_url)
    else:
        st.warning("Character image not found.")

with col2:
    st.header(recommended_character)

    if recommended_image_url:
        st.image(recommended_image_url)
    else:
        st.warning("Character image not found.")
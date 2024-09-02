
#"""
#Actually made in .ipynb Colab's Format then Converted into this .py Format too for Streamlit use.

#The Colab's "Project_Sonifyr.ipynb" Code is located at:
#    https://colab.research.google.com/drive/15v7xhWBH0s3Yq0f6fpg7wMNnf9qurVOz?usp=sharing
#"""

import streamlit as st
import requests
from transformers import pipeline

# Load the MusicGen model
pipe = pipeline("text-to-audio", model="facebook/musicgen-small")

# Define Deezer API search endpoint
DEEZER_API_URL = "https://api.deezer.com/search"

# Function to search for songs
def search_song(query):
    try:
        params = {'q': query}
        response = requests.get(DEEZER_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while searching for songs: {e}")
        return []

# Function to generate music
def generate_music(prompt):
    try:
        inputs = pipe(prompt)
        return inputs
    except Exception as e:
        st.error(f"An error occurred while generating music: {e}")
        return None

# Create Streamlit interface
st.title("# Project Sonifyr")

# Search bar for song or artist
query = st.text_input(label="Search for a song or artist:")

# Button to search for songs
if st.button("Search Songs"):
    try:
        songs = search_song(query)
        if songs:
            results = f"Found {len(songs)} results for '{query}':\n"
            for song in songs:
                song_title = song['title']
                artist_name = song['artist']['name']
                preview_url = song['preview']
                results += f"- {song_title} by {artist_name}\n"
                results += f"[Listen Preview]({preview_url})\n"
            st.write(results)
        else:
            st.write("No songs found. Try a different search term.")
    except Exception as e:
        st.error(f"An error occurred while displaying search results: {e}")

# Button to generate music
if st.button("Generate Music"):
    try:
        generated_music = generate_music(query)
        if generated_music:
            st.write(f"Generated Music:\n{generated_music}")
    except Exception as e:
        st.error(f"An error occurred while generating music: {e}")

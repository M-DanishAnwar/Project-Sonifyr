# -*- coding: utf-8 -*-
"""
Actually made in .ipynb Colab's Format then Converted into this .py Format too for Streamlit use.

The Colab's "Project_Sonifyr.ipynb" Code is located at:
    https://colab.research.google.com/drive/15v7xhWBH0s3Yq0f6fpg7wMNnf9qurVOz?usp=sharing
"""

import streamlit as st
import requests
from transformers import pipeline

# Load the MusicGen model
pipe = pipeline("text-to-audio", model="facebook/musicgen-small")

# Define Deezer API search endpoint
DEEZER_API_URL = "https://api.deezer.com/search"

# Function to search for songs
def search_song(query):
    params = {'q': query}
    response = requests.get(DEEZER_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return []

# Function to generate music
def generate_music(prompt):
    inputs = pipe(prompt)
    return inputs

# Create Streamlit interface
st.title("# Project Sonifyr")

# Search bar for song or artist
query = st.text_input(label="Search for a song or artist:")

# Button to search for songs
if st.button("Search Songs"):
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

# Button to generate music
if st.button("Generate Music"):
    generated_music = generate_music(query)
    st.write(f"Generated Music:\n{generated_music}")
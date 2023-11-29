from flask import Flask, request, url_for, redirect, session, jsonify
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json  


from app import create_app 

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8008, debug=True) 

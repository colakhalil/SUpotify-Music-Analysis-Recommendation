### SUpotify - Music Analysis and Recommendation System

## General Information##
Project Title
SUpotify

Team Leader
Halil İbrahim Umut Çolak

Team Members
Backend Group: Yusuf Eren Akgün, Berçin Saba Güngör, Atakan Demirel
Web App Group: İdil Güler, Ümit Erkut Çolak
Mobile App Group: Halil İbrahim Deniz, Ayça Ataer, Furkan Emre Güler
Date
15.10.2023

## Technology Stack
Project-Configuration Management: Jira, GitHub
Backend Stack: RestAPI, MySQL, Python, Flask
Web Stack: CSS, JS, HTML, ReactJS
Mobile Stack: Swift, SwiftUI

## MVP Features
Data Format:

Collects song information as part of an album, single, or other media.
Includes track name, performers, album/media, and user rating.
Handles challenges like multiple performers, different versions of the same song, and unifying these during analysis.
Data Collection:

Manual User Input: Via a user-friendly interface in the web/mobile application.
Batch Input: Allows uploading multiple songs via text file, CSV, JSON, etc.
Database Transfer: Users can import song data from a cloud or self-hosted database.
Rating Capability: Users can rate or update ratings for songs, albums, or performers.
Song Removal: Option to remove songs, albums, performers from the system in a cascading manner.
External System Integration: Ability to transfer song information from platforms like Spotify, last.fm, etc.
Analysis of Musical Choices:

Provides statistical analysis and visualization (tables, charts) on user preferences.
Filters based on date constraints (e.g., favorite albums from the 90s).
Allows viewing of data according to pre-determined criteria and customizations.
Recommendations:

Recommends music based on user ratings, temporal properties, and possibly friend activities.
Offers recommendations at song, album, and performer levels.
Can incorporate genre-based recommendations and activity-based suggestions (e.g., suggesting artists not recently listened to).
Additional Basic Features:

Authentication: Supports basic password-based authentication.
Friends and Friendship Management: Allows adding friends and managing how much of their activities influence recommendations.
Result Sharing: Ability to share analysis results on social media.
Data Exporting: Export song ratings and other data in various file formats.

## Additional Features
Extended Song Information:

Includes additional properties like song length, lyrics, tempo, genres, mood, recording type, instruments, play count, release year, and addition date to the user's database.
Customizable Analysis Interface:

Users can create pivot tables, edit charts interactively, and select different types of charts for a personalized analysis experience.
Visual Experience Customization:

Offers a choice between light and dark mode for user interface personalization.
Third-party Authenticators:

Integrates with services like Spotify or Google for user authentication, enhancing security and convenience.
Advanced Recommendations:

Utilizes a broader range of data, including geolocation, genre preferences, and performer preferences for more tailored recommendations.
Friends' Activity View:

Allows users to see and potentially use their friends' activities for recommendations, subject to permissions.
App Tutorial:

Provides guidance for new users and remains accessible for reference, enhancing user experience and accessibility.
Playlist Merging:

Enables users to combine their playlists, offering flexibility in playlist management.
Automatic Playlist Creation:

Generates playlists that resemble the user's own, simplifying the process of discovering and organizing music.


## Effort Estimation
Duration: 12 weeks
Team: 9 members
Total: ~11 man-months


## Project Milestones
Milestone/Deliverable	Date
Graphical Design of UI and Backend-Database Diagrams	22.10.2023
User Authentication and Database Setup	6.11.2023
Data Collection in JSON Format	20.11.2023
UI Completion for Mobile App and Website	4.12.2023
Recommendation System and API Creation	16.12.2023
Implementation of Additional Features	30.12.2023
Testing and Debugging	14.01.2023

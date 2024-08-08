# Concerts Database Manager
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)


A simple app to keep track of all the concerts you've been to. Made for my own personal use.

I am currently using this app to learn how to use the SQLAlchemy ORM.


## Data model

### Concert
- id
- Artist
- Venue
- date
- setlist
- notes
- rating
- photos
- videos
- ticket

### Artist
- id
- name

### Venue
- id
- name
- Address

### Address
- id
- street
- city
- state
- zip
- country
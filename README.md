# Dexistant
The Future of E-hailing Assistance.

# What does it do?
Dexistant is an AI voice-based assistant that provides guidance and help to drivers who are on the road.
Users do not need to interact with the interface much as most of the instructions can be given out vocally.
This greatly improves the safety of drivers on the road.

# How does this work?
Dexistant uses a bunch of python libraries co-existing in harmony to deliver responses to users. 
User's audio is recorded as the app is running and then sent for audio processing. Audio is sent through a noise suppression filter and then
sent through a second layer of filtering by cutting off further background noise below a certain threshold. The audio is then transcribed into text before
being sent to a Language Learning Model (GPT). The model processes the information and then is sent back as a response.

# Test data
Coming Soon

# Installation Guide
## Prerequisities
- Python 3.8 and above
- pip

## Steps to install
1. Clone the repository
```
git clone https://github.com/Mutton9558/CannotCode
cd CannotCode
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run application
```
python app.py
```

# Credits
1. Shawn Huang (Mutton9558): Coding the app
2. Muhammad Yusuf bin Riduan (yusufriduan): Providing data and testing.

# Work in progress features
1. User interface
<br>
Sneak peek 😉:
<br>
<img src="https://github.com/user-attachments/assets/07b2c113-df11-4299-a04a-d973610722b0">


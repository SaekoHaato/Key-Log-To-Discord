# Key Log To Discord

## WARNING USING THE ACCOUNT VERSION IS AGAINST DISCORD TOS; USE AT YOUR OWN RISK

## Description

This program will log your keys when you click the caps lock button. Once you press the caps lock key for the second time, it will send it to Discord. This program will not steal any data. This was made with CustomTkinter for the UI

## Installation

### Exe

Download the exe-main if you don't have python installed. Nothing else is needed  If you don't use the TTS option. If you do want TTS, you need to install **VB-CABLE Virtual Audio Device** at https://vb-audio.com/Cable/ (Check TTS section)

### Python

Download the python-main. Copy the directory for the requirements.txt and run this command in command terminal: `pip install -r <path-to-requirements.txt>` if you don't use the TTS option. If you do want TTS, you need to install **VB-CABLE Virtual Audio Device** at https://vb-audio.com/Cable/ (Check TTS section)

## HOW TO USE:

### Account Path:

1. Import the **Link** of the **Channel** you want to send to
   1. Go to **Discord** on **Web Browser**
   2. Turn on **Developer Mode**
   3. Go the **Channel** you want to send messages to, and press "ctrl + shift + I"
   4. Go to the Network Tab at the top of the Developer Interface
   5. Send a message
   6. Click the Messages Tab under the Name Tab
   7. Copy the request URL and paste it into the Channel Textbox
2. Import the Account Code
   1. Go to **Discord** on **Web Browser**
   2. Turn on **Developer Mode**
   3. Press "ctrl + shift + I"
   4. Go to the **Network Tab** at the top of the **Developer Interface**
   5. Send a message
   6. Click the **Messages Tab** under the **Name Tab**
   7. Scroll down to **Authorization**
   8. Import the **Authorization** to  the **Account** **Input**
3. Press the **Activate Button** and press the **Start Key** when u want to type and the **Stop Key** to send

### Webhook Path:

1. Import the **Link** of the **Discord Webhook**
2. Import the **Name** you want the **Webhook** to have
3. Press the **Activate Button** and press the **Start Key** when u want to type and the **Stop Key** to send

### Creating Quick Send:

Go Into Settings.Ini
Under [quick send], add the message you want to send and set it equal to a key (ig: help me = d)

### TTS

1. To get TTS started, you need to install **VB-CABLE Virtual Audio Device** at https://vb-audio.com/Cable/
2. Turn **TTS** in the settings of  KeyLogToDiscord
3. Switch the **Input** **Device** of your call to "CABLE Input (VB-Audio Virtual Cable)" (If the name is different, you will have to go to line 125 and paste the name there)

For TTS, you don't have to put any info in the entries.

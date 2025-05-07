#
# Voice Chat Recorder allows you to record your Roblox Voice Chats that are made in-game!
# Made by EfazDev
# v1.1.0
# 

# Python Modules
from pvrecorder import PvRecorder
import threading
import wave
import datetime
import struct
import promptlib
import os

# Load Bootstrap API
import OrangeAPI as orange; OrangeAPI = orange.OrangeAPI()
debugMode = OrangeAPI.getDebugMode()
apiVersion = OrangeAPI.about()
    
# Printing Functions
def printMainMessage(mes): # White System Console Text
    OrangeAPI.printMainMessage(mes)
def printErrorMessage(mes): # Error Colored Console Text
    OrangeAPI.printErrorMessage(mes)
def printSuccessMessage(mes): # Success Colored Console Text
    OrangeAPI.printSuccessMessage(mes)
def printYellowMessage(mes): # Yellow Colored Console Text
    OrangeAPI.printWarnMessage(mes)
def printDebugMessage(mes): # Debug Console Text
    OrangeAPI.printDebugMessage(mes)

# Main Handler
recording_stream = None
recording_folder_path = ""
streaming_file_path = ""
received_audio = []
is_muted = False

alleged_path = OrangeAPI.getConfiguration("saveFolderPath")
if alleged_path and os.path.isdir(alleged_path):
    recording_folder_path = alleged_path
else:
    if OrangeAPI.getIfRobloxLaunched() == False:
        printMainMessage("Please select a directory to save voice chat recordings to!")
        prompter = promptlib.Files()
        selected_dir = prompter.dir()
        if selected_dir:
            recording_folder_path = selected_dir
            OrangeAPI.setConfiguration("saveFolderPath", recording_folder_path)
            printSuccessMessage(f"Saved selected directory to settings! Path: {recording_folder_path}")
        else:
            printErrorMessage("No directory was given. Disabled voice chat recording.")
    else:
        printErrorMessage("Directory is unable to be asked for. Disabled voice chat recording.")

def onRobloxVoiceChatStart(data):
    global streaming_file_path
    global recording_stream
    global received_audio
    if recording_folder_path:
        recording_stream = PvRecorder(device_index=-1, frame_length=512)
        recording_stream.start()
        streaming_file_path = os.path.join(recording_folder_path, f"{datetime.datetime.now().strftime("%B_%d_%Y_%H_%M_%S_%f")}.wav")
        def record():
            global received_audio
            while recording_stream:
                if is_muted == False:
                    frame = recording_stream.read()
                    received_audio.extend(frame)
            if len(received_audio) > 1:
                with wave.open(streaming_file_path, "w", encoding="utf-8") as f:
                    f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                    f.writeframes(struct.pack("h" * len(received_audio), *received_audio))
                printYellowMessage(f"The voice chat had ended! File Path: {streaming_file_path}")
                OrangeAPI.sendDiscordWebhookMessage("Voice Chat Recording Saved!", f"Your voice chat recording was saved!", 28415, [OrangeAPI.DiscordWebhookField("Voice Recording Location", streaming_file_path, True)], "https://cdn.efaz.dev/cdn/png/orange_microphone.png")
            else:
                printYellowMessage(f"The voice chat had ended! No audio file was made due to the recording being empty.")
        threading.Thread(target=record, daemon=True).start()
        printSuccessMessage(f"Started a new voice chat recording! Expected File Path: {streaming_file_path}")
def onRobloxVoiceChatLeft(data):
    global recording_stream
    if recording_stream:
        recording_stream.stop()
        recording_stream = None
    else:
        printDebugMessage("The voice chat recording was already cleared before the voice chat ended!")
def onRobloxVoiceChatMute(data):
    global is_muted
    is_muted = True
    printDebugMessage("The voice chat microphone was muted!")
def onRobloxVoiceChatUnmute(data):
    global is_muted
    is_muted = False
    printDebugMessage("The voice chat microphone was unmuted!")
import speech_recognition
# from vosk import Model, KaldiRecognizer  # offline recognize
# import wave
import os
import json
import keyboard
import locale
from subprocess import run

import vlc
import random
from time import sleep as sl

class VoiceAssistant:
    """
    settings voice assistant, his/her name, gender, language speech
    """
    name = ""
    gender = ""
    speech_language = ""
    recognition_language = ""

"""
def use_offline():
    recognized_data = ""
    # noinspection PyBroadException
    try:
        if not os.path.exists("models/vosk-model-small-ru-0.4"):
            print("Please download the model from:\n",
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        # analyse
        wave_audiofile = wave.open("microphone_result.wav", "rb")
        model = Model("models/vosk-model-small-ru-0.4")
        # noinspection PyShadowingNames
        recognizer = KaldiRecognizer(model, wave_audiofile.getframerate())

        data = wave_audiofile.readframes(wave_audiofile.getnframes())
        if len(data) > 0:
            if recognizer.AcceptWaveform(data):
                # get data from JSON-string
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Sorry speech service is unavaliable. Try again later")

    return recognized_data
"""

# noinspection PyUnusedLocal
def record_and_recognize_audio():  # *args: tuple):
    """
    запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # уровень окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            audio = recognizer.listen(microphone, 5, 10)
            with open("microphone_result.wav", "wb") as file:
                file.write(audio.get_wav_data())
        except speech_recognition.WaitTimeoutError:
            # чего вы пытаетесь добиться, сэр? у вас на исходе и время и варианты решения проблемы
            return

        try:
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError:
            print("Check Internet connection")
            # recognized_data = use_offline()

        return recognized_data

# noinspection PyUnusedLocal
def run_command(k, commands, *key1):
    """
    run commands
    :param k: key of command
    :param key1: second key for command
    :param commands: other part of command
    :return: None
    """
    if k == "change" and commands[1] == "язык":
        keyboard.send("alt + shift")  # смена языка
    elif k == "find":
        if commands[1] == "в":
            if commands[2] == "гугле":
                k = "google"  # поиск в гугле
            elif commands[2] == "яндексе":
                k = "yandex"  # поиск в яндексе
#####################################################################################
        elif " ".join(commands[1:3]) == "на компьютере":
            # поиск на компьютере
            if lang == "ru":
                keyboard.press_and_release("left windows + а")
            elif lang == "en":
                keyboard.press_and_release("left windows + f")
            sl(5)
            keyboard.write(" ".join(commands[3:len(commands)]), delay = 0.1)
            sl(2)
            keyboard.send("enter")
    elif k == "build" and commands[1] == "проект":
        # определить текущее открытое окно и путь к нему
        pass
    elif k == "shutdown" and commands[1] == "компьютер":
        vlc.MediaPlayer(os.path.sep.join([".", "voices", "yes_sir"])).play()
        run(args=["shutdown", "/s", "/t", "1"])


class Recognizer:
    @staticmethod
    def commands_recognizer(data, command, i = 1):
        """
        Definition for recognize commands
        :param data: data from JSON
        :param command: command for recognize
        :param i: number command in JSON
        :return: None
        """
        if command[0] == "Джарвис":
            command = command[1:]
        elif command[0] == '':
            return

        key = None
        key1 = None
        for value in data.values():
            if i == 1:
                for k, v in value.items():
                    if type(v) is list:
                        for j in v:
                            if command[0] == str(j):
                                print(k)
                                key = k
                                if key != ("find" or "change"):
                                    i = 2
                                break
                        if key is not None:
                            break
                    else:
                        if command[0] == str(v):
                            key = k
                            i = 2
                            break
                    if key is not None:
                        break
            elif i == 2:
                for k, v in value.items():
                    for k1, v1 in v.items():
                        if type(v1) is list:
                            for j in v1:
                                if command[1] == str(j):
                                    print(k)
                                    key1 = k1
                                    i = 2
                                    break
                            if key1 is not None:
                                break
                        else:
                            if command[1] == str(v1):
                                key1 = k1
                                i = 2
                                break
                            if key1 is not None:
                                break

        if key is None:
            # чего вы пытаетесь добиться, сэр
            vlc.MediaPlayer(os.path.sep.join([".", "voices", "what_do_you_want_sir.wav"])).play()
            return
        run_command(key, command, key1)

# noinspection PyPep8
if __name__ == "__main__":

    # language
    lang = locale.getdefaultlocale()[0].split("_")[0]

    # инструменты распознавания
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    assistant = VoiceAssistant()
    assistant.name = "Jarvis"
    assistant.gender = "male"
    assistant.speech_language = "ru"

    variables = ["At_your_service_sir.wav", "Good_morning.wav", "Jarvis_greeting.wav"]
    path = os.path.sep.join([".", "voices", "start", variables[random.randint(0, len(variables) - 1)]])
    vlc.MediaPlayer(path).play()

    while 1:
        # loading JSON
        try:
            # noinspection PyUnboundLocalVariable
            del data_load
        except NameError:
            pass
        with open("config.json", "r", encoding="utf-8") as f:
            data_load = json.load(f)
        voice_input = record_and_recognize_audio()
        print(voice_input)
        
        try:
            os.remove("microphone_result.wav")
        except FileNotFoundError:
            pass

        voice_input = "найди на компьютере *.txt"

        Recognizer.commands_recognizer(data_load, voice_input.split(" "))

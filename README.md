# Ask ChatGPT for a voice

## Introduction

The program who decode you voice and send query to openai ChatGPT, after this show answer in tkinter window

## Requirements

- Linux
- [wihsper](https://github.com/openai/whisper)
- [chatgpt-shell-cli](https://github.com/0xacx/chatGPT-shell-cli)
- You OpenAI key
- Festival TTS

## Installation

1. Install whisper
2. Install chat-shell-cli
3. Select size languge model in main file ask_cli.py (default is medium) in line 91 (MODEL parametr)
4. Setup decode language in ask_cli.py in function decode() line 64

## Usage

Start programm in shell "python ask_cli.py" and wait voice sounde from file "im_listen.txt" ask anything and wait result. Logs in voice_gpt_log.log.
I bind 8'th button mouse via xbindkeys, and ask GPT very easy.
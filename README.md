# VoiceAssistant

# Known issues
## Linux
### PyAudio installation
Possible error
```
ERROR: Could not build wheels for PyAudio, which is required to install pyproject.toml-based projects
```

Install next
```
sudo apt-get install portaudio19-dev
```
Do installation again
```
pip3 install PyAudio==0.2.13
```
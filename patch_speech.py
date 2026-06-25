import os, re

# Patch le SpeechRecognitionPlugin Android pour augmenter le silence timeout
path = "node_modules/@capgo/capacitor-speech-recognition/android/src/main/java/app/capgo/speechrecognition/SpeechRecognitionPlugin.java"

if not os.path.exists(path):
    print("Plugin not found, skipping patch")
    exit(0)

content = open(path).read()

# Ajouter setPauseThreshold et setSpeechTimeout après recognizer init
# On cherche le endOfSpeech ou onReadyForSpeech pour injecter après la création du recognizer
patch = """
        // PATCH: augmenter le silence threshold natif Android
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
            android.os.Bundle params = new android.os.Bundle();
            params.putFloat(android.speech.SpeechRecognizer.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 5000f);
            params.putFloat(android.speech.SpeechRecognizer.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 5000f);
            params.putFloat(android.speech.SpeechRecognizer.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 500f);
        }
"""

# Cherche la ligne startListening ou recognizer.startListening
if "recognizer.startListening" in content:
    content = content.replace(
        "recognizer.startListening(",
        "// patched\n        android.os.Bundle patchParams = new android.os.Bundle();\n"
        "        patchParams.putFloat(\"android.speech.extra.SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS\", 5000f);\n"
        "        patchParams.putFloat(\"android.speech.extra.SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS\", 5000f);\n"
        "        patchParams.putFloat(\"android.speech.extra.SPEECH_INPUT_MINIMUM_LENGTH_MILLIS\", 500f);\n"
        "        recognizer.startListening(",
        1
    )
    open(path, 'w').write(content)
    print("Patch applied successfully")
else:
    print("Pattern not found, dumping recognizer lines:")
    for i, line in enumerate(content.split('\n')):
        if 'recognizer' in line.lower() or 'listen' in line.lower():
            print(f"  {i}: {line}")

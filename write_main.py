# ── MainActivity.java ──
code = (
    "package com.tilawa.sourate;\n"
    "import com.getcapacitor.BridgeActivity;\n"
    "import android.os.Bundle;\n"
    "import android.webkit.PermissionRequest;\n"
    "import android.webkit.WebChromeClient;\n"
    "import android.webkit.WebView;\n"
    "import app.capgo.speechrecognition.SpeechRecognitionPlugin;\n"
    "public class MainActivity extends BridgeActivity {\n"
    "    @Override\n"
    "    public void onCreate(Bundle savedInstanceState) {\n"
    "        registerPlugin(SpeechRecognitionPlugin.class);\n"
    "        super.onCreate(savedInstanceState);\n"
    "        WebView webView = getBridge().getWebView();\n"
    "        webView.setWebChromeClient(new WebChromeClient() {\n"
    "            @Override\n"
    "            public void onPermissionRequest(PermissionRequest request) {\n"
    "                request.grant(request.getResources());\n"
    "            }\n"
    "        });\n"
    "    }\n"
    "}\n"
)
open('android/app/src/main/java/com/tilawa/sourate/MainActivity.java', 'w').write(code)

# ── Patch du timeout silence Capgo ──
import os, glob

# Chercher le fichier Java du plugin Capgo
pattern = 'node_modules/@capgo/capacitor-speech-recognition/android/**/*.java'
java_files = glob.glob(pattern, recursive=True)

for path in java_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # La ligne clé où le plugin démarre l'écoute
    target = 'speechRecognizer.startListening(intent);'
    patch = (
        'intent.putExtra(android.speech.RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 10000L);\n'
        '        intent.putExtra(android.speech.RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 10000L);\n'
        '        intent.putExtra(android.speech.RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 3000L);\n'
        '        ' + target
    )

    if target in content and 'EXTRA_SPEECH_INPUT_COMPLETE_SILENCE' not in content:
        patched = content.replace(target, patch)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(patched)
        print(f"✅ Patché: {path}")
    elif 'EXTRA_SPEECH_INPUT_COMPLETE_SILENCE' in content:
        print(f"ℹ️ Déjà patché: {path}")
    else:
        print(f"⚠️ Target non trouvé dans: {path}")

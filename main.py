from flask import Flask, request, render_template_string, send_file
from gtts import gTTS

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Voice Generator</title>
</head>
<body style="text-align:center; padding:50px;">
    <h1>🗣️ AI Voice Generator</h1>
    <form action="/voice" method="post">
        <textarea name="text" rows="5" cols="50" placeholder="Enter text..."></textarea><br><br>
        <select name="lang">
            <option value="en">English</option>
            <option value="ur">Urdu</option>
            <option value="hi">Hindi</option>
            <option value="ar">Arabic</option>
            <option value="fr">French</option>
            <option value="es">Spanish</option>
        </select><br><br>
        <button type="submit">Generate Voice</button>
    </form>
</body>
</html>
'''
@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/voice', methods=['POST'])
def voice():
    text = request.form.get('text')
    lang = request.form.get('lang', 'en')
    if not text:
        return "❌ Please enter some text."

    try:
        tts = gTTS(text=text, lang=lang)
        filename = "static/output.mp3"
        tts.save(filename)

        # Return audio player
        return f'''
            <h2>✅ Voice Generated!</h2>
            <audio controls autoplay>
                <source src="/{filename}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <br><br>
            <a href="/">🔙 Go Back</a>
        '''
    except Exception as e:
        return f"Error generating voice: {e}"

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(f"static/{filename}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify, send_from_directory
from music21 import stream, note, instrument, tempo
import random
import os
from datetime import datetime

app = Flask(__name__)

OUTPUT_FOLDER = "generated_music"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def generate_music(style):
    melody = stream.Stream()

    melody.append(tempo.MetronomeMark(number=120))

    if style == "Piano":
        melody.append(instrument.Piano())
        scale = ["C4", "D4", "E4", "G4", "A4", "C5", "E5"]

    elif style == "Classical":
        melody.append(instrument.Piano())
        scale = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

    elif style == "Jazz":
        melody.append(instrument.ElectricPiano())
        scale = ["C4", "Eb4", "F4", "Gb4", "G4", "Bb4", "C5"]

    else:
        melody.append(instrument.Piano())
        scale = ["C4", "D4", "E4", "G4", "A4"]

    for _ in range(40):
        n = note.Note(random.choice(scale))
        n.quarterLength = random.choice([0.5, 1, 1.5])
        melody.append(n)

    filename = f"music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    melody.write("midi", fp=filepath)

    return filename


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    style = data.get("style", "Piano")

    try:
        filename = generate_music(style)

        return jsonify({
            "success": True,
            "filename": filename,
            "download": f"/download/{filename}"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(
        OUTPUT_FOLDER,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
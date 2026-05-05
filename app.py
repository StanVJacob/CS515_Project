
from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)


@app.route("/")
def index():
    """SHow the UI,"""
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
# THis is a POST method, we are sending the text to the server and getting back the translated response.

def translate():
    """
    Translate an English string into Simplified Chinese.

    Request JSON:
        {"text": "<english text>"}
    Response JSON:
        {"translation": "<translated text>"}

    Empty input short-circuits to "" so we do not waste an API call on
    silence coming out of the speech recognizer.
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"translation": ""})

    try:
        translated = GoogleTranslator(source="en", target="zh-CN").translate(text)
    except Exception as exc:
        # Return the error message so the browser can show it inline.
        return jsonify({"error": str(exc)}), 500

    return jsonify({"translation": translated or ""})


if __name__ == "__main__":
    # debug=True gives us auto-reload while developing.
    app.run(debug=True, port=5001)

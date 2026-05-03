from flask import Flask, render_template, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    text_to_analyse = request.args.get('textToAnalyse', '').strip()

    if not text_to_analyse:
        return jsonify({'error': 'Invalid text! Please try again.'}), 400

    result = emotion_detector(text_to_analyse)

    if result['dominant_emotion'] is None:
        return jsonify({'error': 'Invalid text! Please try again.'}), 400

    response = {
        'anger':    result['anger'],
        'disgust':  result['disgust'],
        'fear':     result['fear'],
        'joy':      result['joy'],
        'sadness':  result['sadness'],
        'dominant_emotion': result['dominant_emotion'],
        'message': (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

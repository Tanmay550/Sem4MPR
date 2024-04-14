from flask import Flask, jsonify, redirect, url_for
import webbrowser

app = Flask(__name__)

@app.route('/search-google-maps')
def search_google_maps():
    try:
        query = 'Cardiologist in Mumbai'
        url = f'https://www.google.com/maps/search/{query.replace(" ", "+")}'
        webbrowser.open(url)
        # return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return 'Google Maps search initiated.'

if __name__ == '__main__':
    app.run(debug=True)

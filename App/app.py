from flask import Flask, render_template, request
from anki2pgn import main

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    source_pgn = request.form['source']
    color_pick = request.form['color']
    main(source_pgn, color_pick)
    return 'Anki deck generated successfully!'

if __name__ == '__main__':
    app.run(debug=True)


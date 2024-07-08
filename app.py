from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Store chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/chatbot.html') 
def chatbot():
    return render_template('chatbot.html' , chat_history = chat_history) 

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    # Here you can process the user message and generate a response
    bot_response = f"Echo: {user_message}"
    chat_history.append({'user': user_message, 'bot': bot_response})
    return jsonify(chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)

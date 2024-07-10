from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore



app = Flask(__name__)
cred = credentials.Certificate("C:/Users/Aman/Downloads/chatbot-zing-e77df-firebase-adminsdk-nelvr-66994cf765.json")
firebase_admin.initialize_app(cred)

# Store chat history
chat_history = []

@app.route('/') 
@app.route('/index.html')
def index():
    return render_template('index.html') 

@app.route('/chatbot.html') 
def chatbot():
    return render_template('chatbot.html' , chat_history = chat_history) 

@app.route('/registrationPage.html') 
def regPage():
    return render_template('registrationPage.html')  

@app.route('/signup' , methods=['POST']) 
def signup(): 
    try: 
        username = request.form['username'] 
        fname = request.form['fname']
        lname = request.form['lname'] 
        email = request.form['email']  
        password = request.form['pass']  

        user = auth.create_user(
            uid = username,
            email=email,
            password=password, 
        )

        db = firestore.client()
        db.collection('users').document(user.uid).set({
        'username': username,
        'first_name': fname, 
        'last_name' : lname, 
        }) 
        return jsonify({'message': 'User created successfully!'}), 201

    except ValueError as e:
        # Handle invalid user input (e.g., missing fields, invalid email format)
        return jsonify({'error': 'Invalid user input: ' + str(e)}), 400

    except firebase_admin.exceptions.FirebaseAuthError as e:
        # Handle Firebase Authentication errors (e.g., email already in use)
        return jsonify({'error': 'Firebase Authentication error: ' + str(e)}), 400

    except Exception as e:  # Catch any other unexpected errors
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500


@app.route('/login' , methods=['GET'])  
def login(): 
    try: 
        username = request.form['username'] 
        email = request.form['email'] 
        password = request.form['password']

        user = auth.sign_in_with_email_and_password(email , password) ; 
        db = firestore.client() ; 
        if (user) :
            doc_ref = db.collection('users').document(username)
            doc = doc_ref.get() ; 
        
            if doc.exists:  
                return jsonify({'message': 'Signed in successfully!'}), 200
            else : 
                return jsonify({'message': 'Invalid login credentials'}), 401
                
        else: 
            return jsonify({'message': 'Invalid login credentials'}), 401 
    except firebase_admin.exceptions.FirebaseAuthError as e: 
        error_code = e.error_code
        error_message = e.message   

    

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    # Here you can process the user message and generate a response
    bot_response = f"Echo: {user_message}"
    chat_history.append({'user': user_message, 'bot': bot_response})
    return jsonify(chat_history=chat_history)



if __name__ == '__main__':
    app.run(debug=True)

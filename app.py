from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Aquí puedes llamar al modelo para generar una respuesta basada en user_input
    # Utiliza el código que proporcionaste para cargar y ejecutar el modelo

    return render_template('index.html', user_input=user_input, model_output=model_output)

if __name__ == '__main__':
    app.run(debug=True)

# from app import app

# app.run(host = 'localhost', port = '9000',debug=True)


from app import app
from pow_show import pow_show_bp  # Import the pow_show blueprint

app.register_blueprint(pow_show_bp)  # Register the blueprint with the app

app.run(host='localhost', port=9000, debug=True)

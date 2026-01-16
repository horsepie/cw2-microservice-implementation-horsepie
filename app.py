import connexion
import pathlib
from config import db, configure_app

# Get the base directory for the project
basedir = pathlib.Path(__file__).parent.resolve()

# Create Connexion app instance
app = connexion.FlaskApp(__name__, specification_dir=basedir)

# Configure the underlying Flask app
configure_app(app.app)

# Initialize SQLAlchemy with the underlying Flask app
db.init_app(app.app)

# Load API specification from swagger.yml to auto-generate routes
app.add_api("swagger.yml")

@app.route("/")
def home():
    return {"message": "API is running"}

if __name__ == "__main__":
    # Start the Flask development server on port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)
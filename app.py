import connexion

# Create Connexion app instance
app = connexion.App(__name__, specification_dir="./")

# Load API specification from swagger.yml to auto-generate routes
app.add_api("swagger.yml")

@app.route("/")
def home():
    return {"message": "API is running"}

if __name__ == "__main__":
    # Start the Flask development server on port 8000
    app.run(host="0.0.0.0", port=8000, debug=True)
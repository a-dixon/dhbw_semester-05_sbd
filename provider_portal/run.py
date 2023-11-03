from app import create_app

app = create_app()

if __name__ == '__main__':
    # Starten Sie die Flask-Anwendung
    app.run(debug=True)
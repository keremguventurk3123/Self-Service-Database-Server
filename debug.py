from api import create_app

if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5100)

from src.app import app


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=3000,
        access_log=True,
        debug=True,
        auto_reload=True
    )

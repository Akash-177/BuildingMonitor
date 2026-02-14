from app import create_app
import time
import sys

app = create_app()

if __name__ == '__main__':
    # wait a bit for mysql to be ready when using docker
    if '--docker' in sys.argv:
        print("Waiting for database...")
        time.sleep(5)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
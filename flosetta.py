
from app import app

if __name__ == '__main__':
    print('SAYING SOMETHING ELSE')
    app.run(host='localhost', port=8000, debug=True)
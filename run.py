#from app import myapp_obj
#myapp_obj.run(debug=True)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


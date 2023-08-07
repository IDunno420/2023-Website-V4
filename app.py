from website import create_app # Imports website and imports the create app function

if __name__ == "__main__": 
    app = create_app() # Defines app for the create_app() function
    app.run(debug=True) # Loads and activates the app, this makes the website load

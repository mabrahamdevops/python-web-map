from flask import Flask
app = Flask (__name__)
 

@app.route("/")
def hello():
    return "Yes, this works!"

if __name__ == "__main__":
    app.run(debug=True)
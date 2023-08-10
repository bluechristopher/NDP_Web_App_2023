from flask import Flask, render_template, request, send_from_directory, flash
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'my#secret+key'

db = sqlite3.connect("album.db")
db.execute("CREATE TABLE IF NOT EXISTS photos(pid INTEGER PRIMARY KEY, photo TEXT);")
db.commit()
db.close()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST" and request.files and "photo" in request.files:
        photo = request.files["photo"]

        if not photo.filename:
            flash("Please select a photo before submitting.", "danger")
        else:
            filename = secure_filename(photo.filename)
            path = os.path.join("uploads", filename)
            photo.save(path)

            db = sqlite3.connect("album.db")
            db.execute("INSERT INTO photos(photo) VALUES(?)", (filename,))
            db.commit()
            db.close()
          
            flash("Photo posted successfully! Click on View Photos to see the photo gallery.", "success")

    return render_template("index.html")

      
@app.route('/view')
def view():
  db = sqlite3.connect("album.db")
  recs = db.execute("SELECT * FROM photos;")
  pics = []
  for rec in recs:
    print(rec)
    pics.append(rec[1])
  db.close()
  return render_template("view.html", pics=pics)

@app.route('/photos/<filename>')
def get_file(filename):
  return send_from_directory("uploads", filename)

@app.route('/message', methods=["GET", "POST"])
def message():
    if request.method == "POST":
        message = request.form['message']

        if message == "Clear_All_Messages_Now":
            with open('message.txt', 'w') as file:
                file.write("")

        elif len(message.strip()) >= 5:
            with open('message.txt', 'a') as file:
                file.write(message + '\n')

    with open('message.txt', 'r') as file:
        posts = file.readlines()

    return render_template('message.html', posts=posts)



app.run(host='0.0.0.0', port=81)

from flask import Flask,render_template,redirect,url_for,request,session,g,url_for
import os
cap1=os.path.join('static', 'images')
app = Flask(__name__)
app.config['upload1']=cap1
@app.route("/")
def po():
    return render_template('loginn.html')
@app.route("/iotpoc")
def home1():
    filename1=os.path.join(app.config['upload1'], 'sam.jpg')
    filename2=os.path.join(app.config['upload1'], 'track.jpg')
    filename3=os.path.join(app.config['upload1'], 'stock.jpg')
    filename4=os.path.join(app.config['upload1'], 'pass.jpg')
    filename5=os.path.join(app.config['upload1'], 'pass1.jpg')
    return render_template("style.html",user_image1=filename1,user_image2=filename2,user_image3=filename3,user_image4=filename4,user_image5=filename5)



    



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')




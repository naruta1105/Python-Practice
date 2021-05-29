from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from bokehpractice import script1, div1, cdn_css, cdn_js
    return render_template("plot.html", 
            script1=script1, 
            div1= div1,
            cdn_css= cdn_css,
            cdn_js= cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)

from asyncio import tasks
from django.http import QueryDict
from flask import Flask, render_template, request
from src.QueryProcessor import QueryProcessor

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')

# route to return result set
@app.route("/results", methods=["POST", "GET"])
def results():
    if request.method == 'POST':
        query = request.form['query']

        q = QueryProcessor()
        result_set = q.ProcessQuery(query)
        return render_template("result.html",tasks = result_set)

    else:
        return render_template("result.html")

# route to show result
@app.route("/showDoc/<string:id>", methods=["POST", "GET"])
def showDoc(id):
    return render_template(id + ".txt")
    


if __name__ == "__main__":
    app.run(debug=True)

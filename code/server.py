import recommend_svd
from flask import Flask, render_template, Response


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', name='Joe')


@app.route('/api/<user_id>')
def api(user_id):
    sanitised_user_id = int(user_id)
    already_rated, predictions = recommend_svd.get_recommendations_for_user(sanitised_user_id)

    json_already_rated = already_rated.to_json(orient='records')
    json_predictions = predictions.to_json(orient='records')

    json = f"""{{
    "already_rated": {json_already_rated},
    "predictions": {json_predictions}
}}"""

    return Response(json, mimetype='text/json')


if __name__ == '__main__':
    recommend_svd.setup()
    app.run()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import plotly.graph_objs as go
import plotly.offline as pyo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

def create_graph():
    data = [go.Bar(
        x=['Category A', 'Category B', 'Category C'],
        y=[10, 20, 15]
    )]
    layout = go.Layout(
        title='Sample Bar Chart',
        height=500
    )
    fig = go.Figure(data=data, layout=layout)
    graph = pyo.plot(fig, output_type='div')
    return graph

@app.route('/', methods=['GET', 'POST'])
def index():
    graph = create_graph()
    if request.method == 'POST':
        name = request.form['username']  # Capture username from the form
        return render_template('index.html', graph=graph, name=name)
    
    return render_template('index.html', graph=graph)

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)

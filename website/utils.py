from ast import Bytes
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

def get_plot(x,y):
    plt.switch_backend('AGG')
    
    graph= get_graph()
    return graph
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from wordcloud import WordCloud, STOPWORDS
import sqlite3
from datetime import datetime, timezone
import os

# get data
def generate_cloud():
    # fetch data & process
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('SELECT name from sqlite_master where type= "table"')
    buffer=cur.fetchall()
    tables=[table[0] for table in buffer]
    words = []
    for i in range(len(tables)):
        cur.execute("SELECT word from "+tables[i]+";")
        buffer=cur.fetchall()
        filter=[word[0] for word in buffer]
        for word in filter:
            words.append(word)
    con.close()
    text = ' '.join(word for word in words)
    print(text)

    # makes the circle using numpy
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    # Generate word cloud
    wordcloud = WordCloud(width = 6000, height = 6000, random_state=1, background_color='white', colormap='plasma',mask=mask, collocations=False, stopwords = STOPWORDS).generate(text)
    wordcloud.to_file('static/wordcloud1.png')
    fig = Figure(figsize=(10, 7), dpi=100)
    
    # instantiating the canvas with the figure as
    # argument.
    canvas = FigureCanvasAgg(fig)
    
    # Do some plotting
    ax = fig.add_subplot(111)
    ax.imshow(wordcloud)
    ax.axis('off')
    
    # Save the figure to a file
    image_name = "wordcloud_{}.png".format(datetime.now(timezone.utc))
    fig.savefig('static/images/{}'.format(image_name))
    
    # delete previous files
    for filename in os.listdir("static/images/"):
        if filename != image_name: 
            print(filename)
            os.remove("static/images/{}".format(filename))
        else:
            continue

    return image_name

generate_cloud()


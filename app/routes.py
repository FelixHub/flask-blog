from flask import render_template,request,url_for,redirect,flash
from app import app,db,rap_model,indices_word,word_indices
from app.models import Post,MD_Post
import markdown
from datetime import datetime
import re
import numpy as np

def sample(preds, temperature=1):
    # sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # posts =  MD_Post.query.limit(3).all()
    filenames = os.listdir(url_for('static', filename='posts/'))
    posts = [{} for _ in range(len(filenames))]
    for filename in filenames :
        with open(filename, 'r') as f:  
        post.body = markdown.markdown(post.body,    
                                      extensions=['mdx_math'])
        post.timestamp = post.timestamp.strftime('%Y-%m-%d')
    return render_template('index.html', title='Home', posts=posts)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    # posts =  MD_Post.query.all()

    for post in posts :
        post.body = markdown.markdown(post.body,    
                                      extensions=['mdx_math'])
        post.timestamp = post.timestamp.strftime('%Y-%m-%d')
    return render_template('blog.html', title='Blog posts', posts=posts)

@app.route('/blog_post/<id>', methods=['GET', 'POST'])
def blog_post(id):
    # posts =  MD_Post.query.filter_by( id = id )
    
    for post in posts :
        post.body = markdown.markdown(post.body,    
                                      extensions=['mdx_math'])
    return render_template('blog_post.html',posts=posts)


@app.route('/video', methods=['GET', 'POST'])
def video():
    return render_template('video.html', title='Video Projects')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About me')

@app.route('/models', methods=['GET', 'POST'])
def models():
    return render_template('ML/models.html', title='fun ML models')

'''
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST' : 
        post = MD_Post(body= request.form['content'],title=request.form['title'])
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))

    return render_template('create.html', title='create a blog post')
'''

@app.route('/models/rap_bot', methods=['GET', 'POST'])
def rap_bot():
    
    output = []
    sentence = []
    ''' 
    Yo voici le retour du rap de robot
    Un max de flow tu le sais
    '''
    if request.method == 'POST' : 
        sentence = request.form['lyric']
        sentence = re.findall(r'\S+|\n',sentence)

        print(sentence)

        sentence = [i for i in sentence if i in word_indices  ]
        
        while len(sentence) < 15 :
            sentence.append("yo")
        if len(sentence) > 15 :
            sentence = sentence[:15]

        print(sentence)

        for i in range(75):
            x_pred = np.zeros((1, 15))
            for t, word in enumerate(sentence):
                x_pred[0, t] = word_indices[word]
            preds = rap_model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, 0.5)
            next_word = indices_word[next_index]

            sentence = sentence[1:]
            sentence.append(next_word)
            output.append(next_word)
        print(output)

    output = " ".join(output)
    sentence = " ".join(sentence)

    return render_template('ML/rap_bot.html',
                            used_seed = sentence,
                            generated_lyrics= output,
                            title='Rap-bot 3000')
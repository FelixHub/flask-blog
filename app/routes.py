from flask import render_template,request,url_for,redirect,flash
from app import app
import markdown
from datetime import datetime
import os
import collections
import re

class Post:
    """
    An instance contains metadata about a blog post as well as the body of the
    blog post written in Markdown. Upon instantiation, the Markdown content is
    additionally converted into HTML.
    """
    def __init__(self, title, date, tags, summary, href, content_md):
        self.title = title
        self.date = date
        self.tags = tags
        self.summary = summary
        self.href = href
        self.content_md = content_md
        self.content_html = markdown.markdown(content_md,extensions=['mdx_math'])

def parse_markdown_post(md_path):
    """
    Use a regular expression to parse the components of a Markdown post's
    header and the post body. Return an assembled Post object,
    """
    with open(md_path, 'rb') as f:
        markdown = f.read().decode('utf-8')
    re_pat = re.compile(r'title: (?P<title>[^\n]*)\sdate: (?P<date>\d{2}-\d{2}-\d{4})\s'
                        r'tags: (?P<tags>[^\n]*)\ssummary: (?P<summary>[^\n]*)')
    match_obj = re.match(re_pat, markdown)
    title = match_obj.group('title')
    date = match_obj.group('date') 
    summary = match_obj.group('summary')
    tags = sorted([tag.strip() for tag in match_obj.group('tags').split(',')])
    print(md_path)
    href = url_for('blog_post', post_title = md_path.rsplit('\\', 1)[-1][:-3])
    content_md = re.split(re_pat, markdown)[-1]
    return Post(title, date, tags, summary, href, content_md)
  
 
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    posts = []
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        posts.append(post_obj)
    sorted_posts = sorted(posts, 
        key=lambda x: datetime.strptime(x.date, '%d-%m-%Y'), reverse=True)
    return render_template('index.html', title='Home', posts=sorted_posts)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    tag_dict = dict()
    posts = []
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        posts.append(post_obj)
        for tag in post_obj.tags:
            if tag not in tag_dict.keys():
                tag_dict[tag] = 0
            tag_dict[tag] += 1
    sorted_tag_dict = collections.OrderedDict()
    for key in sorted(tag_dict.keys()):
        sorted_tag_dict[key] = tag_dict[key]
    sorted_posts = sorted(posts, 
        key=lambda x: datetime.strptime(x.date, '%d-%m-%Y'), reverse=True)
    return render_template('blog.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict)    

@app.route('/blog_post/<post_title>')
def blog_post(post_title):
    md_path  = os.path.join(app.root_path, 'content', '%s.md' % post_title)
    post = parse_markdown_post(md_path)
    print(post.title)
    return render_template('blog_post.html', post=post)


@app.route('/video', methods=['GET', 'POST'])
def video():
    return render_template('video.html', title='Video Projects')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About me')

@app.route('/models', methods=['GET', 'POST'])
def models():
    return render_template('ML/models.html', title='fun ML models')


@app.route('/models/rap_bot', methods=['GET', 'POST'])
def rap_bot():
    return("Coming soon...")

'''
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


@app.route('/models/rap_bot', methods=['GET', 'POST'])
def rap_bot():
    
    output = []
    sentence = []

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

'''
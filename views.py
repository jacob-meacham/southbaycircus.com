from __future__ import with_statement

import os.path
import re

from datetime import date, datetime
from unicodedata import normalize

from app import app, pages
from forms import EditPageForm, AddPostForm, ContactForm, BookingForm
from app.auth import LoginForm
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask.ext.login import login_user, login_required
from werkzeug import secure_filename

def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def page_helper(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)

@app.route('/')
def index():
    page = pages.get('index')
    return render_template('index.html', page=page)

@app.route('/classes/')
def classes():
    return page_helper('classes')

@app.route('/teachers/')
def teachers():
    return page_helper('teachers')

@app.route('/contact/', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        form.send()
        flash('Thanks for contacting us! We promise to get back to you soon.', 'contact')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', form=form)

@app.route('/booking/', methods=["GET", "POST"])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        form.send()
        flash('Thanks for contacting us! We promise to get back to you soon.', 'booking')
        return redirect(url_for('booking'))
    return render_template('booking.html', title='Booking', form=form)

@app.route('/about/')
def about():
    return render_template('about.html', title='About')

@app.route('/blog/')
def blog():
    posts = [p for p in pages if 'blog' in p.path]
    posts = sorted(posts, reverse=True, key=lambda p: p.meta.get('published', date.today()))
    return render_template('blog_index.html', title='Blog', posts=posts)

# Fallback on loading the flatpage.
@app.route('/<path:path>/')
def post_detail(path):
    post = pages.get_or_404(path)
    recent_posts = [p for p in pages if 'blog' in p.path]
    recent_posts = sorted(recent_posts, reverse=True, key=lambda p: p.meta.get('published', date.today()))
    recent_posts = recent_posts[:5]
    return render_template('blog_post.html', title=post['title'], post=post, recent_posts=recent_posts)

interest_images = [
    'img/bg/acro1.png',
    'img/bg/acro2.png'
]

@app.errorhandler(404)
def error_404(error):
    reasons = [
        "this page is currently being sat on by an elephant!",
        "this page is on the high-wire right now - we don't want to break its concentration!",
        "the carnies are still putting this part of the Big Top up, check back later!",
        "this page has a ton of lion slobber on it. We'll need to let it dry out.",
        "this page is getting costume and makeup put on - we'll let you know when it's ready for its performance",
        "one of our fire-eaters accidentally burned this page up!"
    ]

    return render_template('404.html', reasons=reasons, interest_images=interest_images), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', interest_images=interest_images), 500


# Admin functionality
@app.route('/admin/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember = True)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin_page_list.html', pages=pages)

@app.route('/admin/blog/new/', methods=["GET", "POST"])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        slug = slugify(form.title.data)
        page_path = os.path.join(app.root_path, app.config['FLATPAGES_ROOT'], 'blog', slug) + app.config['FLATPAGES_EXTENSION']

        # Add some metadata for the user:
        blog_post = ('title: ' + form.title.data.replace(':', '') + '\n' +
                     'published: ' + datetime.today().strftime('%Y-%m-%d') + '\n\n' +
                     form.page.data)

        with open(page_path, 'w') as page_file:
            page_file.write(blog_post)
        return redirect(url_for('post_detail', path='blog/' + slug))

    return render_template('admin_add_page.html', form=form)

@app.route('/admin/edit/<path:path>/', methods=["GET", "POST"])
@login_required
def edit_page(path):
    page = pages.get_or_404(path)
    form = EditPageForm()
    if form.validate_on_submit():
        # Save over the page, and force a reload.
        page_path = os.path.join(app.root_path, app.config['FLATPAGES_ROOT'], path) + app.config['FLATPAGES_EXTENSION']

        with open(page_path, 'w') as page_file:
            page_file.write(form.page.data)
        return redirect(url_for('post_detail', path=path))
    else:
        # Construct the full page, including meta:
        full_page = ''
        for k, v in page.meta.iteritems():
            full_page += str(k) + ': ' + str(v) + '\n'
        full_page += '\n'
        full_page += page.body
        form.page.data = full_page
    return render_template('admin_edit_page.html', form=form, page=page)

@app.route('/admin/media/library')
@login_required
def media_library_json():
    valid_files = []
    for root, _, names in os.walk(os.path.join(app.root_path, 'static', 'img', 'blog')):
        files = [('img/blog/' + n, os.path.getmtime(os.path.join(root, n)))
                 for n in names if n[0] != '.']
        valid_files.extend(files)
    valid_files.sort(key=lambda x: x[1], reverse=True)
    return jsonify({
        'media': [f[0] for f in valid_files]
    })

@app.route('/admin/media/upload', methods=['POST'])
@login_required
def upload_image():
    data_file = request.files['file']
    filename = secure_filename(data_file.filename)
    data_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    return jsonify(name=filename,
                   size=0,
                   url=url_for('media_library'),
                   thumbnail=url_for('media_library'))

@app.route('/admin/media')
@login_required
def media_library():
    valid_files = []
    for root, _, names in os.walk('static/img/blog'):
            files = ['img/blog/' + n  # Use + instead of os.path.join because we always want to use / when we send it to jinja.
                     for n in names if n[0] != '.']
            valid_files.extend(files)
    return render_template('library_test.html', files=valid_files)

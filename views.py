from __future__ import with_statement

import os.path
import re

from datetime import date, datetime
from unicodedata import normalize

from app import app, pages
from forms import EditPageForm, AddPostForm
from app.auth import LoginForm
from flask import render_template, flash, redirect, session, url_for, request
from flask.ext.login import login_user, login_required

def slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
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

def interest_images():
	return [
		'img/bg/acro1.png',
		'img/bg/acro2.png'
	]

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

@app.route('/contact/')
def contact():
	return render_template('contact.html', title='Contact Us')

@app.route('/booking/')
def booking():
	return page_helper('booking')

@app.route('/about/')
def about():
	return render_template('about.html', title='About')

@app.route('/blog/')
def blog():
	posts = [p for p in pages if 'blog' in p.path]
	posts = sorted(posts, reverse=True, key=lambda p: p.meta.get('published',
        date.today()))
	return render_template('blog_index.html', title='Blog', posts=posts)

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
		blog_post = 'title: ' + form.title.data + '\n' + \
					'published: ' + datetime.today().strftime('%Y-%m-%d') + '\n' + \
					form.page.data

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
		for k,v in page.meta.iteritems():
			full_page += str(k) + ': ' + str(v) + '\n'
		full_page += '\n'
		full_page += page.body
		form.page.data = full_page
	return render_template('admin_edit_page.html', form=form, page=page)

# Fallback on a simple loading of the flatpage.
@app.route('/<path:path>/')
def post_detail(path):
	post = pages.get_or_404(path)
	recent_posts = [p for p in pages if 'blog' in p.path]
	recent_posts = sorted(recent_posts, reverse=True, key=lambda p: p.meta.get('published',
        date.today()))
	recent_posts = recent_posts[:5]
	return render_template('blog_post.html', title=post['title'], post=post, recent_posts=recent_posts)

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

	return render_template('404.html', reasons=reasons, interest_images=interest_images()), 404

@app.errorhandler(500)
def error_500(error):
	return render_template('500.html', interest_images=interest_images()), 500
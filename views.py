from datetime import date, datetime
from app import app, pages
from flask import render_template, flash, redirect, session, url_for, request

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

@app.route('/about')
def about():
	return page_helper('about')

@app.route('/classes')
def classes():
	return page_helper('classes')

@app.route('/teachers')
def teachers():
	return page_helper('teachers')

@app.route('/contact')
def contact():
	return page_helper('contact')

@app.route('/about')
def about():
	return page_helper('about')

@app.route('/blog/')
def blog():
	posts = [p for p in pages if 'blog' in p.path]
	posts = sorted(posts, reverse=True, key=lambda p: p.meta.get('published',
        date.today()))
	return render_template('blog_index.html', title='Blog', posts=posts)

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
	return render_template('500.html'), 500
from app import app, pages
from flask import render_template, flash, redirect, session, url_for, request

@app.route('/')
def index():
	page = pages.get('index')
	return render_template('page.html', page=page)

@app.route('/blog')
def blog():
	# TODO: Render blog paths, blog index
	return render_template('404.html'), 404

def page_helper(path):
	page = pages.get_or_404(path)
	template = page.meta.get('template', 'page.html')
	return render_template(template, page=page)

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

@app.route('/<path:path>/')
def page(path):
	return page_helper(path)

@app.errorhandler(404)
def error_404(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(error):
	return render_template('500.html'), 500
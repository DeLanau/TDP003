from flask import Flask, render_template, request, abort

import data

import logging
# from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route('/')
def index():
    """ Renders index.html with latest project. """
    
    db = data.load('data.json')
    latest_project = data.search(db)[0]
    
    return render_template('index.html', latest_project=latest_project)

@app.route('/project/<id>')
def project(id):
    """ Renders project.html by <id>. """
    
    db = data.load('data.json')
    proj = data.get_project(db, id)

    if proj is None:
        abort(404)
        # app.logger.error('projektet kunde inte hittas [id]: %s', id)
    return render_template('project.html', project=proj)

@app.route('/list/')
def list():
    """ Renders list.html by GET-arguments. """
    db = data.load('data.json')
    if request.args:
        sort_by = request.args.get('sort_by', 'project_id')
        sort_order = request.args.get('sort_order', 'asc')
        techniques = request.args.getlist('techniques')
        if not techniques:
            techniques = None
        search = request.args.get('search', None)
        search_fields = request.args.getlist('search_fields')
        if not search_fields:
            search_fields = None
        project_list = data.search(db, sort_by, sort_order, techniques, search, search_fields)
    else:
        project_list = db
    
    techniques_list = data.get_techniques(db)
    # app.logger.info('sökte efter: "%s" med "%s"', request.args, techniques_list) 
    return render_template('list.html', project_list=project_list, techniques_list=techniques_list)

@app.route('/techniques/')
def techniques():
    """Renders techniques.html with all techniques used and corresponding projects"""
    
    db = data.load('data.json')
    techniques_stats = data.get_technique_stats(db)
    return render_template('techniques.html', techniques_stats=techniques_stats)

@app.errorhandler(404)
def page_not_found(e):
    """ Renders a custom 404 page (error.html) """
    
    return render_template('error.html', error_id=404,
                           error_text="The page you requested does not exist"), 404

@app.errorhandler(500)
def server_error(e):
    """ Renders a custom 500 page (error.html) """
    return render_template('error.html', error_id=500,
                           error_text="An internal server error occured."), 500

if __name__ == "__main__":
    # formatter = logging.Formatter( "%(asctime)s | %(funcName)s | %(levelname)s | %(message)s ")
    # handler = RotatingFileHandler('server.log', maxBytes=0)                                      
    # handler.setLevel(logging.INFO)                                                                  
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)
    # if not app.debug:
    #     logging.basicConfig(filename='server.log',level=logging.INFO)
    app.run()

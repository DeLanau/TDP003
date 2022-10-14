#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def load(filename):
    """ Load filename and returns list of projects without dublicates. """        
    try:
        ids = []
        new_list = []
        
        with open(filename, encoding="utf-8") as f:
            db = json.load(f)

            for p in db:
                if p["project_id"] not in ids:
                    ids.append(p["project_id"])
                    new_list.append(p)
            
            new_list = sort_list(new_list, order="asc", dictkey="project_id")                   
        return new_list
    except:
        return None

#projects_list = sort_list(projects_list, order="asc", dictkey="name")
    
def get_project_count(db):
    """ Counts and return total projects.  """
    return len(db)

def get_project(db, id):
    """ Search and return project by id.  """
    try:
        for dict in db:
            if int(dict["project_id"]) == int(id):
                return dict
    except:
        return None


def get_techniques(db):
    """ Get list of all used techniques without dublicates and alphabeticly sorted. """
    try:
        
        tech_list = []

        for proj in db:
            for tech in proj['techniques_used']:
                if tech.lower() not in tech_list:
                    tech_list.append(tech)
        tech_list.sort()
        return tech_list
    except:
        return None

def get_technique_stats(db):
    """ Get techniques used statistics sorted after name of technique. """
    tech_stats = {}
    techniques_list = get_techniques(db)

    for tech in techniques_list:
        projects_list = []
        for proj in db:
            if tech in proj["techniques_used"]:
                projects_list.append({'id': proj['project_id'], 'name': proj['project_name']})
        projects_list = sort_list(projects_list, order="asc", dictkey="name")
        tech_stats[tech] = projects_list
    return tech_stats

def sort_list(lista, order, dictkey):
    """ Sort list by order and dictkey. """ 
 
    if order == "asc":
        lista = sorted(lista, key=lambda x: x[dictkey], reverse=False)    
    else:
        lista = sorted(lista, key=lambda x: x[dictkey], reverse=True)
    
    return lista

def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    """ Search in db by folowing parametrs: sort_by, sord_order, techniques, search and search_fields. """
    
    results =  []
    #if search is none, search = empty = match all projects 
    if search is None:
        search = ''
        
    if sort_order not in ['desc', 'asc']:
        raise ValueError

    #iterate over project in db, if techniques != none, iterater over tech in techniques and check if not in project. Not in project = break loop. not ok continue with next project.  
    for project in db:
        if techniques is not None:
            ok = True
            for tech in techniques:
                if tech not in project['techniques_used']:
                    ok = False
                    break     
            if not ok:
                continue

        #if true = set field to all fields, in current iteration. if search_field exists in project, compare search to key in project and then append results. if not break go to next field in project. 
        if search_fields is None:
            search_fields = [field for field in project]
        for field in search_fields:
            try:
                if type(project[field]) is list:
                    for item in project[field]:
                        if search.lower() in str(item).lower():
                            results.append(project)
                            break
                        else: continue
                        break
                elif search.lower() in str(project[field]).lower():
                    results.append(project)
                    break
            except KeyError:
                pass
                        
    try:
        reverse = True if sort_order=='desc' else False	        
        results.sort(key=lambda project: project[sort_by], reverse=reverse)
    except KeyError:
	    pass #dont sort if sort_by is invalid
    return results

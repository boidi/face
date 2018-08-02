# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Boidi)s
"""
print('_doc_')

from flask import Flask, redirect, url_for, request, render_template
import numpy as np
from requete import *

app = Flask(__name__)


@app.route('/' ,methods=['GET', 'POST'])
def index():
    result =select_data()

    if request.method == 'GET':
        return render_template('formulaire.html',data = result)
  

    elif request.method == 'POST':
        user_name = request.form['full_name']
        res = get_best_matches(user_name,result,3)
        print(res[0])
        res1 = search_data(str(res[0]), str(res[1]), str(res[2]))
        return render_template('formulaire.html',data=result, query_result=res1, has_res1=True)

        
        
        
#if __name__ == '__main__':
app.run(debug = False)
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Boidi)s
"""
print('_doc_')
import numpy as np
import mysql.connector 
from mysql.connector import errorcode
from pyxdameraulevenshtein import damerau_levenshtein_distance_ndarray, normalized_damerau_levenshtein_distance_ndarray
import os
import csv
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


#%%
def connection_bd():
    try:
        cnx = mysql.connector.connect(user='root',
                                      password= 'root',
                                      host= '127.0.0.1',
                                      database='dbase')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return(cnx)
     
def select_data():
    cnx =  connection_bd()                        
    cursor = cnx.cursor()
    query_string = "SELECT fullname  from personne;"
    cursor.execute(query_string)
    data = np.array(cursor.fetchall()).ravel()
    #print()
    cnx.commit() 
    cursor.close()
    cnx.close()
    return data
def get_best_matches(fullname, data, limit):
     res = normalized_damerau_levenshtein_distance_ndarray(fullname, data)  
     return data[res.argsort()][:limit]
    

# 
def search_data(elem,elm1,elm2):
    cnx = connection_bd()
    cursor=cnx.cursor()
    query=" SELECT fullname,father_name,mother_name,genre,age from face.personne where fullname in (%s,%s,%s);"
    cursor.execute(query,(elem,elm1,elm2))
    resultat = cursor.fetchall()
    cnx.commit() 
    cursor.close()
    cnx.close()
    return resultat
  

def add_data():

    if request.method == 'POST':

        # Get the file from post request
        f = request.files['csv']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        cnx = connection_bd()
        cursor = cnx.cursor()

        def change_path(path):
            return path.replace("\\", "/")

        correct_path = change_path(file_path)


        query_add_data = r"""LOAD DATA LOCAL INFILE '{}' INTO TABLE face.personne  CHARACTER SET utf8 FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n' 
            set face.personne.birthday = STR_TO_DATE(face.personne.birth, '%d/%m/%Y')"""

        cursor.execute(query_add_data.format(correct_path))

        cnx.commit()
        cursor.close()

        return  "Data added successfully"


# =============================================================================

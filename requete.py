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
  

# =============================================================================

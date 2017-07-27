'''
Created on Jun 23, 2016
filename: database_.py

@author: gmaturan
'''

import sqlite3 as sql
import errors as ers
import string
from numpy import record
import numpy as np



class database:
    
    DB_NAME = 'patient1.db'
    
    def __init__(self):
        
        '''
        '''
        
    def databse(self, db_name = DB_NAME):
        # Create a database to store blood sugar levels of patient
        table = sql.connect(db_name)
        cursor = table.cursor()
        
        # CREATES TABLE IF DOES NOT EXIST
        cursor.execute('''CREATE TABLE IF NOT EXISTS PATIENT (
                           ID                     KEY     NOT NULL,
                           NAME                   TEXT    NOT NULL,
                           LASTNAME               TEXT    NOT NULL,
                           MINITIAL               TEXT    NOT NULL,
                           AGE                    INT     NOT NULL,
                           NEXTOFKIN              TEXT    NOT NULL,
                           CONTACTINFO            INT     NOT NULL);''')
        table.commit()
        
        table.close()
        
    def patient_tables(self, db_name):
        # Create a database to store blood sugar levels of patient
        table = sql.connect(db_name)
        cursor = table.cursor()
        
        # CREATES TABLE IF DOES NOT EXIST        
        cursor.execute('''CREATE TABLE IF NOT EXISTS PATIENT_HIST (
                           PATIENT_ID                    KEY  NOT NULL,
                           GENDER                       TEXT  NOT NULL,
                           WEIGHT                       INT   NOT NULL,
                           DIAGNOSIS                    TEXT  NOT NULL,
                           DATE                         TEXT  NOT NULL,
                           ETHNICITY                    TEXT  NOT NULL,
                           ALERGIES                     TEXT  NOT NULL);''')
        
        # A table storing patient
        cursor.execute('''CREATE TABLE IF NOT EXISTS PATIENT_DATA (
                            ID_KEY_PRIMARY                KEY   NOT NULL,
                            BLOODSUGARLEVEL               INT   NOT NULL,
                            BLOODPRESSURE                TEXT   NOT NULL,
                            EXERCIRSE                 CHAR(3)   NOT NULL,
                            FREQUENCY                    INT    NOT NULL,
                            HOURS                        TEXT   NOT NULL);''')
        table.commit()
        
        table.close()
        
    def insert_record_patient(self, db_name, record):
        #insert items into PATIENT table
        table = sql.connect(db_name)
        table.execute('INSERT INTO PATIENT VALUES (?,?,?,?,?,?,?)', record)
        table.commit()
    
    def insert_comments(self, db_name, record):
        #insert items into COMMENTS table
        table = sql.connect(db_name)
        table.execute('INSERT INTO PATIENT VALUES (?,?,?)', record)
        table.commit()
    
    # This function works correctly
    def update_patient_record(self, db_name,record):
        table = sql.connect(db_name)
        statement = '''UPDATE PATIENT SET NAME  = '%s', 
                                       LASTNAME = '%s',
                                       MINITIAL = '%s',
                                            AGE = '%d', 
                                    NEXTOFKIN = '%s',
                                    CONTACTINFO = '%d' 
                                       WHERE ID = '%d' ''' %record
        table.execute(statement )
        table.commit()
    
    # This function updates the record in the patient database
    def update_patient_record_(self,db_name, x, record):
        table = sql.connect(db_name)
        table.execute('UPDATE PATIENT SET WHERE NAME = ?', )
        table.commit()
    
    # This function does not work correctly
    def update_comments(self, db_name, record):
        table = sql.connect(db_name)
        statement = '''UPDATE PATIENT SET DATE = %s,
                                     COMMENTS_ = %s, ''' %record
        table.execute(statement)
        table.commit()
        
    def insert_record_patient_history(self, db_name, record):
        #insert items into BLSUGGAR table
        table = sql.connect(db_name)
        table.execute('INSERT INTO PATIENT_HIST VALUES (?,?,?,?,?,?,?)', record)
        table.commit()
        print('value has been saved')
    
    def general_search_query(self, db_name, record):
        table = sql.connect(db_name)
        curser = table.cursor()
        condition = '''SELECT * 
                        FROM  PATIENT 
                        WHERE ID LIKE '%%s%'
                            OR NAME LIKE '%%s%'
                            OR LASTNAME LIKE '%%s%'
                            OR MINITIAL LIKE '%%s%'
                            OR AGE LIKE '%%s%'
                            OR NEXTOFKIN '%%s%'
                            OR CONTACTINFO '%%s%' ''' %record
                            
            
    def insert_record_patient_data(self, db_name, record):
        #insert items into BLSUGGAR table
        table = sql.connect(db_name)
        try:
            table.execute('INSERT INTO PATIENT_DATA VALUES (?,?,?,?,?,?)', record)
            table.commit()
        except:
            ers.errors().error_messages(5)
        
    def remove_record(self, db_name, tbl, record):
        # Deletes item from Database
        table = sql.connect(db_name)
        query = 'DELETE FROM ' + tbl.upper() + ' WHERE NAME=' + record
        try:
            table.execute(query)
            #table.execute('DELETE FROM PATIENT WHERE NAME=?', (record,))
            table.commit()
        
        except:
            ers.errors().error_messages(5)
            
        table.close()
        
    def remove_record_item(self, db_name, item):
        # Deletes item from Database
        table = sql.connect(db_name)
        table.execute('DELETE FROM PATIENT WHERE VALUES (?,?,?,?)', (item,))
        table.commit()
        
    def db_print(self, db_name):
        # prints information stored in the database
        table = sql.connect(db_name)
        # prepare a cursor object using cursor() method
        cursor = table.cursor()
        # Prepare SQL query to INSERT a record into the database.
        condition = "SELECT * FROM PATIENT" # Displays all items stored in database

        # Creates a list to store output values
        data = [] 
        
        try:
            # Execute the SQL command
            cursor.execute(condition)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            for row in results:
                id_ = row[0]
                lastName = row[2]
                name = row[1]
                mi = row[3]
                age = row[4]
                NofKin = row[5]
                contactInf = row[6]
                # Collects information an stores it into array
                #value = "%d,    %s,    %s,    %s" %d, %s, %s (id_, lastName, name, mi, age, NofKin, contactInf)
                value = ( id_, lastName, name, mi, age, NofKin, contactInf)
                data.append(value)

        except:
            ers.errors().error_messages(5)
        
        # disconnect from server
        table.close()
        return data
    
    def db_patient_history_print(self, db_name):
        # prints information stored in the database
        table = sql.connect(db_name)
        # prepare a cursor object using cursor() method
        cursor = table.cursor()
        # Prepare SQL query to INSERT a record into the database.
        condition = "SELECT * FROM PATIENT_HIST"

        # Creates a list to store output values
        data = [] 
        print('I am inside db_patient_history_print()')
        try:
            # Execute the SQL command
            cursor.execute(condition)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            for row in results:
                id_ = row[0]
                gender_ = row[1]
                weight_= row[2]
                diagnosis_ = row[3]
                date_ = row[4]
                ethnicity_ = row[5]
                alergies_ = row[6]
                # Collects information an stores it into array
                #value = "%d,    %s,    %d,    %s" % (id_, name, age, birthday)
                value = ( id_, gender_, weight_, diagnosis_, date_, ethnicity_, alergies_)
                data.append(value)
        except:
            ers.errors().error_messages(5)
        
        # disconnect from server
        table.close()
        return data
    
    def db_patient_data_print(self, db_name):
        # prints information stored in the database
        table = sql.connect(db_name)
        # prepare a cursor object using cursor() method
        cursor = table.cursor()
        # Prepare SQL query to INSERT a record into the database.
        condition = "SELECT * FROM PATIENT_HISTORY"

        # Creates a list to store output values
        data = [] 
    
        try:
            # Execute the SQL command
            cursor.execute(condition)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            for row in results:
                id_ = row[0]
                bsugar_ = row[1]
                bpressure_= row[2]
                exercise_ = row[3]
                frequency_ = row[4]
                hours_ = row[5]
                
                # Collects information an stores it into array
                #value = ( "%d,    %d,    %s,         %s,        %s,         %s"   )
                value = ( id_, bsugar_, bpressure_, exercise_, frequency_, hours_)
                data.append(value)
        except:
            ers.errors().error_messages(5)
        
        # disconnect from server
        table.close()
        return data
    

    
    # Navigation to the database possible   
    # Implementation needed
    def db_navagation(self):
        
        print('Implementation needed')
        
    # Deletes item from Database
    def remove_item_bsugar(self,db_name, record,):
        # Deletes item from Database
        table = sql.connect(db_name)
        #table.execute('DELETE FROM PATIENT VALUES (?,?,?,?)', record)
        table.execute('DELETE FROM PATIENT WHERE KEY=?', (record,))
        table.commit()
        
    # Retrieves the patient name
    def get_record(self, db_name, key):
        
        table = sql.connect(db_name)
        cursor = table.cursor()
        
        condition = "SELECT * FROM PATIENT \
               WHERE ID == '%d'" % (key)
        
        cursor.execute(condition)
        name_ = cursor.fetchone()
        # returns the patient name
        return name_[1]
    
    def get_record_bool(self, db_name, key):
        
        table = sql.connect(db_name)
        cursor = table.cursor()
        
        condition = "IF EXIST (SELECT * FROM PATIENT WHERE ID == '%d' \
                    THEN RETURN TRUE \
                    ELSE RETURN FALSE END " %(key)
        
        #cursor.execute(condition)
        #name_ = cursor.fetchone()
        # returns the patient name
        #print(key)
        #print(name_[0])
        if cursor.execute(condition) == 1:
            name_ = cursor.fetchone()
            if name_[0] == key:
                return True
        if cursor.execute(condition) == 0:
            return False
    
    # Retrieves the patient record according matching a ID
    def get_patient(self, db_name, ID):
        
        table = sql.connect(db_name)
        cursor = table.cursor()
        
        condition = "SELECT * FROM PATIENT \
               WHERE ID == '%d'" % (ID)
        
        cursor.execute(condition)
        record_ = cursor.fetchone()
        
        return record_
    
    def print_results(self, db_name, column, key):
        # prints information stored in the database
        table = sql.connect(db_name)
        # prepare a cursor object using cursor() method
        cursor = table.cursor()
        # Prepare SQL query to INSERT a record into the database.
        condition = "SELECT * FROM PATIENT \
               WHERE " + column + "='%s'" %(key)

        # Creates a list to store output values
        data = [] 
        
        try:
            # Execute the SQL command
            cursor.execute(condition)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            for row in results:
                id_ = row[0]
                name = row[1]
                lname = row[2]
                mi = row[3]
                age = row[4]
                nok = row[5]
                cinfo = row[6]
                
                # Collects information an stores it into array
                #value = "%d,    %s,    %d,    %s" % (id_, name, age, birthday)
                value = ( id_, lname, name, mi, age, nok, cinfo)
                data.append(value)
                
        except:
            ers.errors().error_messages(5)
        
        # disconnect from server
        table.close()
        return data
    
    def db_general_print(self, db_name, condition):
        # prints information stored in the database
        table = sql.connect(db_name)
        # prepare a cursor object using cursor() method
        cursor = table.cursor()

        # Creates a list to store output values
        data = []
        list_ = []
            # Execute the SQL command
        cursor.execute(condition)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            if len(row) == 7:
                id_ = row[0]
                gender_ = row[1]
                weight_= row[2]
                diagnosis_ = row[3]
                date_ = row[4]
                ethnicity_ = row[5]
                alergies_ = row[6]
                value = ( id_, gender_, weight_, diagnosis_, date_, ethnicity_, alergies_)
                data.append(value)
            else:
                for n in range (0,len(row)):
                    list_.insert(n,row[n])
            # tuple(list_) turns list_ into a touple
            
            data.append(tuple(list_))
            #clears the list_
            for n in range (0, len(list_)):
                list_.pop()
                
        # disconnect from server
        table.close()
        return data
        
        

    

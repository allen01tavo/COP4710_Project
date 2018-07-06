'''
Created on Jul 23, 2017

@author: gmaturan
'''



import tkinter as tr
import errors as ers
import tkinter.ttk as ttk
import csv


import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import database as db
import datetime as dt



class graph:

    DB_NAME = ''
    
    #This class can be used by itself.
    def __init__(self):
        '''
            implementation
            '''
        #self.graph(defaul, db_name)
        
    def graph(self, defaul, db_name):
        # Graph sugar level vs time
        # This section has not been implemented
        title = defaul
        self.DB_NAME = db_name
        
        self.graph_window = tr.Tk()                     # creates a new window
        self.graph_window.minsize(500, 400)
        self.graph_window.title(title)
        self.frame_1 = tr.Frame(self.graph_window) # frame to enclose the button
        self.frame_2 = tr.Frame(self.graph_window)
        self.frame_3 = tr.Frame(self.graph_window)
        self.frame_4 = tr.LabelFrame(self.frame_1, text = 'GRAPH RESULTS')
        
        months1_ = ('Month1','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        days1_ = ('Day1','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',\
                        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',\
                        '25', '26', '27', '28', '29', '30', '31')
        months2_ = ('Month2','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        days2_ = ('Day2','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',\
                        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',\
                        '25', '26', '27', '28', '29', '30', '31')

        self.sel_month_from = ttk.Combobox(self.frame_4, values = months1_, state = 'readonly', width = 5)
        self.sel_month_from.current(0)
        self.sel_day_from =   ttk.Combobox(self.frame_4, values = days1_, state = 'readonly', width = 5)
        self.sel_day_from.current(0)
        self.sel_month_to =   ttk.Combobox(self.frame_4, values = months2_, state = 'readonly', width = 5)
        self.sel_month_to.current(0)
        self.sel_day_to =     ttk.Combobox(self.frame_4, values = days2_, state = 'readonly', width = 5)
        self.sel_day_to.current(0)
        
        self.grap_btn = tr.Button(self.frame_4, \
                                  text = 'Graph', command = self.save_values )
        
        # Creates a close button
        self.close_btn = tr.Button(self.frame_1, \
                                    text = 'Close', command = self.close_window)
        self.print_btn = tr.Button(self.frame_1, \
                                    text = 'Print', command = self.close_window)
        self.export_btn = tr.Button(self.frame_1, \
                                    text = 'Export', command = self.export_)
        
        # TREEVIEW OF RECORDS
        self.dataCols = ('ID_KEY_PRIMARY', 'BLOOD SUGAR LEVEL', 'BLOOD PRESURE', 'TIME', 'DATE')
        self.bsugarLbl = tr.LabelFrame(self.frame_2, text = 'PATIENT TEST RESULTS')
        self.recordListColumn = ttk.Treeview(self.bsugarLbl,columns = self.dataCols, show = 'headings')
        
        for col in self.dataCols:
            self.recordListColumn.heading(col, text = col.title())
        
        #db.database_().databse_patient(self.DB_NAME)
        #inserting values into the record list
        
        cnt = 0
        for item in db.database().db_bloodsugar_print(self.DB_NAME):
            self.recordListColumn.insert('', 'end', values=item)
            cnt = cnt + 1
        t_cnt = cnt + 1   
        
        # ENTRIES FOR RECORDS
        self.mainLbl = tr.LabelFrame(self.frame_1, text = 'BLOODS SUGAR RESULTS')
        self.keyLbl = tr.LabelFrame(self.mainLbl, text = '#')
        self.keyEntry = tr.Entry(self.keyLbl, width = 4)
        self.keyEntry.insert('end', t_cnt)
        
        self.bLevelLbl = tr.LabelFrame(self.mainLbl, text = 'BLOOD SUGAR LEVEL')
        self.bSugarEntry = tr.Entry(self.bLevelLbl, width = 10)
        
        self.bpLbl = tr.LabelFrame(self.mainLbl, text = 'BLOOD PRESSURE')
        self.sbpEntry = tr.Entry(self.bpLbl, width = 4)
        self.label_ = tr.Label(self.bpLbl,text = '/')
        self.dbpEntry = tr.Entry(self.bpLbl,width = 4)
        
        
        self.timeLbl = tr.LabelFrame(self.mainLbl, text = 'TIME')
        self.timeEntry = tr.Entry(self.timeLbl, width = 8)
        
        self.dateLbl = tr.LabelFrame(self.mainLbl, text = 'DATE')
        self.dateEntry = tr.Entry(self.dateLbl, width = 12)
        
        #updates the date and time
        self.update_date_time(self.timeEntry, self.dateEntry)
        
        self.saveBtn = tr.Button(self.mainLbl, text = 'Save', \
                                 command_ = self.save_values)
        
        # Creates a menu
        self.menu_ = tr.Menu(self.graph_window, tearoff = 0)
        self.menu_.add_command(label = 'Delete', command = self.delete_record)
        self.recordListColumn.bind("<Double-Button-1>", self.popup_event)
        self.bSugarEntry.bind("<Return>", self.save_values_event)
        
        self.mainLbl.pack(side = 'top')
        self.keyLbl.pack(side = 'left')
        self.keyEntry.pack(side = 'left')
        self.bLevelLbl.pack(side = 'left')
        self.bSugarEntry.pack(side = 'left')
        self.bpLbl.pack(side = 'left')
        self.sbpEntry.pack(side = 'left')
        self.label_.pack(side = 'left')
        self.dbpEntry.pack(side = 'left')
        self.timeLbl.pack(side = 'left')
        self.timeEntry.pack(side = 'left')
        self.dateLbl.pack(side = 'left')
        self.dateEntry.pack(side = 'left')
        self.saveBtn.pack(side = 'left')
        
        self.frame_4.pack(side = 'bottom')
        self.sel_month_from.pack(side = 'left')
        self.sel_day_from.pack(side = 'left')
        self.sel_month_to.pack(side = 'left')
        self.sel_day_to.pack(side = 'left')
        self.grap_btn.pack(side = 'right')
        
        self.close_btn.pack(side = 'left')
        self.print_btn.pack(side = 'left')
        self.export_btn.pack(side = 'left')
        self.bsugarLbl.pack(side = 'bottom')

        self.recordListColumn.pack(side = 'left')
        
        self.frame_1.pack(side = 'top')
        self.frame_2.pack(side = 'bottom')
    
    def record_comments(self):
        
        title = 'Comments'
        
        self.comment_window = tr.Tk()                     # creates a new window
        self.comment_window.minsize(500, 400)
        self.comment_window.title(title)
        self.enclosure = tr.Frame(self.comment_window)
        self.lwrFrame = tr.Frame(self.comment_window)
        self.lbl_ = tr.LabelFrame(self.enclosure, text = 'COMMENTS')
        
        self.saveBtn = tr.Button(self.lwrFrame, \
                                 text = 'SAVE', command = self.close_window)
        
        self.comm_input = tr.Entry(self.lbl_, width = 50)
        self.comm_input.pack(side = 'left', expand = 'yes', fill = 'both')
        self.enclosure.pack(side = 'left', expand = 'yes', fill = 'both')
        self.lbl_.pack(side = 'left', expand = 'yes', fill = 'both')
        self.lwrFrame.pack(side = 'bottom', expand = 'yes')
        self.saveBtn.pack(side = 'left')
        self.comm_input.focus()
    # Graph
    # further implementation is needed
    def daily_graph(self, db_name):
        # Implementation needed
        x = []
        y = []
   
        for item in db.database().db_bloodsugar_print(db_name):
            y.append(item[1])
            word = self.sentence_split(item[4], '/')
            x.append(word[1])

        #plt.scatter(x,y, s = 30, c ='red', alpha = 1.0)
        plt.plot(x, y, 'go')
        plt.plot(x,y, ':k')
        plt.xlim(1,31)
        plt.title('Blood Sugar Level')
        plt.xlabel('Day')
        plt.ylabel('Sugar Level')
        plt.show()
        
    def weekly_graph(self):
        # Implementation needed
        print('Implementation needed')
        
    def montly_graph(self):
        # Implementation needed
        print('Implementation nneded')
    
    def display_resulst(self):
        print('Implementation needed')
    
    def close_window(self):
        self.graph_window.destroy()
    
    # The following function saves the values into the database
    def save_values(self):
        
        if self.bSugarEntry.get() == '':
            ers.errors().general_error_messages('Blood Sugar Level')
        else:
            key_ = int(self.keyEntry.get())
            bsl_ = int(self.bSugarEntry.get())
            bp_ = self.sbpEntry.get() + '/' + self.dbpEntry.get()
            time_ = self.timeEntry.get()
            date_ = self.dateEntry.get()
        
            record_ = (key_, bsl_, bp_, time_, date_)
            db.database().insert_record_blsuggar(self.DB_NAME, record_)
            self.update_records()
            self.daily_graph(self.DB_NAME) # DELETE
    
    # the following function is even driven helper function.
    # this function is binded to the bSugarEngtry
    def save_values_event(self, event):
        
        self.save_values()
    
    def clear_list(self):
    #this process can be done two ways
        # way # 1
        for item in self.recordListColumn.get_children():
            self.recordListColumn.delete(item) 
            
    def update_records(self):
    # refresh records after the save button is hit
    
        self.clear_list()
        cnt = 0
        for item in db.database().db_bloodsugar_print(self.DB_NAME):
            self.recordListColumn.insert('', 'end', values=item)
            cnt = cnt + 1
        print(cnt)
        t_cnt = cnt + 1
        
        self.keyEntry.delete(0,tr.END)
        self.keyEntry.insert('end', t_cnt)      # Update entry#
        self.bSugarEntry.delete(0, tr.END)
        self.sbpEntry.delete(0, tr.END)
        self.dbpEntry.delete(0,tr.END)
        self.timeEntry.delete(0,tr.END)
        self.dateEntry.delete(0,tr.END)
        self.update_date_time(self.timeEntry, self.dateEntry)
        self.bSugarEntry.focus()
          
    def delete_record(self, *key):
    #deletes the record
        self.clear_list()
        #implementation is needed
        
    def popup_event(self, event):
    # display the popup menu 
        #self.menu_.post(event.x_root, event.y_root)
        self.record_comments()
    
    # splits a sentence into words and returns an array
    def sentence_split(self, phrase, where):
        
        wds = phrase.split(where)
        return wds
    
    # updates the date and time  
    def update_date_time(self, t_object, d_object):
        
        dtime_ = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        split = dtime_.split(' ')
        date_ = split[0]
        time_ = split[1]
        t_object.insert('end',time_)
        d_object.insert('end',date_)   
    
    def export_to_excel(self, db_name):
        phrase = "DATE        TIME        BLOOD SUGAR LEVEL"
        with open('outfile','w') as f:
            try:
                self.writer = csv.writer(f)
                self.writer.writerow(phrase)
                for row in db.database().db_bloodsugar_print(db_name):
                    print(row[1])
                    print(row[2])
                    print(row[3])
                    txt = "%s            %s            %d" %(row[3], row[2], row[1])
                    self.writer.writerow(txt)
            except:
                ers.errors().general_error_messages('Error 1')
                                    
    def export_(self):
        
        self.export_to_excel(self.DB_NAME)
        
        #the following fucntion is just for test
        self.daily_graph(self.DB_NAME) # DELETE
        
        
        

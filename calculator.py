''' written by: Gustavo A. Maturana
    written on: May 14, 2017
    filename: calculator1.py
'''

import tkinter as Tr
import tkinter.ttk as ttk #from Tkinter import Tk as ttk
import database as db
import errors as ers
import graph as graph
from tkinter.constants import VERTICAL


class calculator:
    
    DB_NAME = 'patient1'

    def __init__(self, title):
    
        # Create the main window Widget
        # Main application page
        self.dataCols = ('PATIENT ID', 'LAST NAME', 'NAME', 'MI','AGE', 'NEXT OF KIN', 'CONTACT INFO')
        
        self.root = Tr.Tk()                         # creates a main application window
        self.root.title(title)                      # application window title
        self.root.minsize(width=450, height=500)    # application window size
        self.frame_1 = Tr.Frame(self.root)
        self.frame_2 = Tr.Frame(self.root)
        self.frame_5 = Tr.Frame(self.root)
        self.frame_3 = Tr.Frame(self.root)
        self.frame_4 = Tr.Frame(self.root)
        self.topFrame = Tr.LabelFrame(self.frame_1, text = 'OPTIONS:')
        self.internal_frame = Tr.Frame(self.frame_1)    # to include the search feature
        self.search_frame = Tr.Frame(self.internal_frame)      # to include the search feature
        
        self.records_lable = Tr.Label(self.frame_5, fg = 'blue', text = 'RECORDS')
        
        self.btn_new_patient = Tr.Button(self.topFrame, \
                                       text  = 'NEW PATIENT', command = self.new_patient_win)
        self.btn_patient_history = Tr.Button(self.topFrame,\
                                        text = 'PATIENT HISTORY', command = self.patien_history)
        self.btn_patient_data = Tr.Button(self.topFrame,\
                                        text = 'PATIENT DATA', command = self.patien_history)
        self.btn_close = Tr.Button(self.frame_2,\
                                        text = 'CLOSE', command = self.root.quit)
        self.btn_queries = Tr.Button(self.topFrame,\
                                        text = 'QUERIES', command = self.patien_history)
        
        self.search_entry_lbl = Tr.LabelFrame(self.search_frame, text = 'Criteria: ')

        self.btn_search = Tr.Button(self.search_entry_lbl, bg = "blue",\
                                        text = 'SEARCH', command = self.search_)
        
        self.clear_search_btn = Tr.Button(self.search_entry_lbl, \
                                        text = 'CLEAR', command = self.clear_search)
        

        self.patientLbl = Tr.LabelFrame(self.frame_4, text = 'PATIENT TABLE')
        self.recordListColumn = ttk.Treeview(self.patientLbl,height = 50,columns = self.dataCols, show = 'headings')
        
        # The following lines of codes format the width of the columns inside the treeview (self.recordLIstColumn)
        self.recordListColumn.column(self.dataCols[0], width = 80)
        self.recordListColumn.column(self.dataCols[1], width = 130)
        self.recordListColumn.column(self.dataCols[2], width = 130)
        self.recordListColumn.column(self.dataCols[3], width = 30)
        self.recordListColumn.column(self.dataCols[4], width = 30)
        self.recordListColumn.column(self.dataCols[5], width = 180)
        self.recordListColumn.column(self.dataCols[6], width = 140)
                
        self.search_lbl = Tr.LabelFrame(self.search_frame, text = 'Search By: ')
        choices = ('Select','Patient Number', 'Patient Name','Patient Last Name','Middle Initial','Age', 'Next of Kin', 'Contact Info',\
                   'Diagnosis','Allergies','Treatment','General Search', 'Advance Search')
        self.selection_box = ttk.Combobox(self.search_lbl, values = choices, state = 'readonly')
        self.selection_box.current(0)
        self.selection_box.grid(column = 0, row = 0)
        
        
        self.search_entry = Tr.Entry(self.search_entry_lbl, width = 40)
        
        self.recordListColumn.bind("<Double-Button-1>", self.OnClick)
        self.search_entry.bind("<Return>",self.Event_Driven_Search)
        
        self.patientLbl.pack(side = 'top')
        self.recordListColumn.pack(side = 'top')
        
        self.records_lable.pack(side = 'right')
        
        self.btn_new_patient.pack(side = 'right')
        self.btn_patient_data.pack(side = 'left')
        self.btn_patient_history.pack(side = 'left')
        self.btn_queries.pack(side = 'left')
        self.btn_close.pack(side = 'right')
        
        self.selection_box.pack(side = 'right')
        self.search_lbl.pack(side = 'left')
        self.search_entry_lbl.pack(side = 'right')
        self.clear_search_btn.pack(side = 'right')
        self.btn_search.pack(side = 'right')
        self.search_entry.pack(side = 'left')
        
        # Creates database if it does not exist or open database to connect to it
        db.database().databse()
        #inserting values into the record list
        count = 0
        for item in db.database().db_print('patient1.db'):
            count = count + 1
            if count % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))
        
        #colors the row
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey')
        self.yscroll_ = Tr.Scrollbar(orient = VERTICAL, command = self.recordListColumn.yview()) 
        self.yscroll_.grid(row = 0, column = 1, sticky = 'nse')
        self.yscroll_.pack(side = 'right', fill = 'y')
        #self.recordListColumn.configure(command= self.yscroll_.set())
        # the following lines add the name to the title to the columns
        for col in self.dataCols:
            self.recordListColumn.heading(col, text = col.title())

            
        self.frame_1.pack(side = 'top')
        self.frame_2.pack(side = 'bottom')
        self.frame_3.pack(side = 'bottom')
        self.frame_5.pack(side = 'top')
        self.frame_4.pack(side = 'bottom')
        self.topFrame.pack(side = 'top')
        self.internal_frame.pack(side = 'right')
        self.search_frame.pack(side = 'left')
        
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
        
        Tr.mainloop()
    
    # destroys main window
    def destroy_root(self):
        
        self.root.destroy()
    
    # This module creates a new patient
    def new_patient_win(self):
        
        title = 'NEW PATIENT'
        
        self.new_patient_window = Tr.Tk()                     # creates a new window
        self.new_patient_window.minsize(400, 280)
        self.new_patient_window.title(title)
        self.frame1 = Tr.Frame(self.new_patient_window, height = 100)
        self.frame2 = Tr.Frame(self.new_patient_window, width = 100)
        self.frame3 = Tr.Frame(self.new_patient_window, width = 100)
        self.frame4 = Tr.Frame(self.new_patient_window, width = 100)
        self.frame5 = Tr.Frame(self.new_patient_window)
        self.frame6 = Tr.Frame(self.new_patient_window)
        
        self.keyLbl = Tr.LabelFrame(self.frame3, \
                                        text = 'PATIENT #:')
        self.nameLbl = Tr.LabelFrame(self.frame4, \
                                        text = 'NAME:')
        self.ageLbl = Tr.LabelFrame(self.frame5, \
                                        text = 'AGE:')
        self.bdayLbl = Tr.LabelFrame(self.frame6, \
                                        text = 'Other Patient Information:')
        # Creates a save and close button
        self.save_btn = Tr.Button(self.frame1, \
                                        text = 'SAVE', command = self.save_record)
        self.cancel_btn = Tr.Button(self.frame1, \
                                        text = 'CANCEL', command = self.cancel_)
        
        self.keyLbl.pack(side = 'left')
        self.keyEntry = Tr.Entry(self.keyLbl, \
                                        width = 4)
        self.nameLbl.pack(side = 'left')
        self.lnameEntry = Tr.Entry(self.nameLbl,\
                                        width = 15)
        self.mInitialEntry = Tr.Entry(self.nameLbl,
                                        width = 2)
        self.nameEntry = Tr.Entry(self.nameLbl, \
                                        width = 15)
        
        self.lnameLbl = Tr.Label(self.nameLbl, \
                                        text = 'Last Name   M.I          Name')
        self.lnameLbl.pack(side = 'bottom')
        
        
        self.ageLbl.pack(side = 'left')
        self.ageEntry = Tr.Entry(self.ageLbl, \
                                        width = 4)
        
        self.bdayLbl.pack(side = 'left')
        self.nextOfKin = Tr.Entry(self.bdayLbl, \
                                        width = 30)
        self.contactInfo = Tr.Entry(self.bdayLbl, \
                                        width = 12)
        self.label1 = Tr.Label(self.bdayLbl, text = '/')
        
        self.label2 = Tr.Label(self.bdayLbl, text = '/')

        self.dateFormatLbl = Tr.Label(self.bdayLbl, \
                                        text = ' Next of Kin                    Contact Information')
        
        self.dateFormatLbl.pack(side = 'bottom')
        
        self.keyEntry.pack(side = 'left')
        self.nameEntry.pack(side = 'right')
        self.mInitialEntry.pack(side = 'right')
        self.lnameEntry.pack(side = 'right')
        self.ageEntry.pack(side = 'right')
        self.nextOfKin.pack(side = 'left')
        self.label2.pack(side = 'left')
        self.contactInfo.pack(side = 'left')
        self.label1.pack(side = 'left')
        
        
        # setting up frames and buttons
        self.save_btn.pack(side = 'right')
        self.cancel_btn.pack(side = 'left')
        self.frame1.pack(side = 'bottom')
        self.frame2.pack(side = 'top')
        self.frame3.pack(side = 'top')
        self.frame4.pack(side = 'top')
        self.frame5.pack(side = 'top')
        self.frame6.pack(side = 'top')
        
        #focus the curser to the Patient ID entry
        self.keyEntry.focus()
        
    # This is section creates the edit window for the patient record
    def editPatient(self, key):
        # the patient name will be displayed on window title
        title = db.database().get_record('patient1.db', key)
        
        self.edit_patient_window = Tr.Tk()                     # creates a new window
        self.edit_patient_window.minsize(500, 400)
        self.edit_patient_window.title(title)
        self.frame1 = Tr.Frame(self.edit_patient_window, height = 100)
        self.frame2 = Tr.Frame(self.edit_patient_window, width = 100)
        self.frame3 = Tr.Frame(self.edit_patient_window, width = 100)
        self.frame4 = Tr.Frame(self.edit_patient_window, width = 100)
        self.frame5 = Tr.Frame(self.edit_patient_window)
        self.frame6 = Tr.Frame(self.edit_patient_window)
        self.frame7 = Tr.Frame(self.edit_patient_window)
        
        #store the value for the specific record that has been clicked
        record_ = db.database().get_patient('patient1.db', key)
        
        # Creates save, cancel and delete buttons
        self.edit_save_btn = Tr.Button(self.frame1, \
                                        text = 'SAVE EDIT', command = self.save_edit)
        self.edit_cancel_btn = Tr.Button(self.frame1, \
                                        text = 'CANCEL EDIT', command = self.cancel_edit)
        self.edit_delete_btn = Tr.Button(self.frame1, \
                                        text = 'DELETE', command = self.delete_patient)
        self.pHistory_btn = Tr.Button(self.frame7, \
                                         text = 'Patient History', command = self.blood_sugar_level)
        self.view_data_btn = Tr.Button(self.frame7, \
                                         text = 'View Data', command = self.cancel_edit)

        self.edit_keyLbl = Tr.LabelFrame(self.frame3, \
                                        text = 'PATIENT #:')
        self.edit_nameLbl = Tr.LabelFrame(self.frame4, \
                                        text = 'NAME:')
        self.edit_ageLbl = Tr.LabelFrame(self.frame5, \
                                        text = 'AGE:')
        self.edit_bdayLbl = Tr.LabelFrame(self.frame6, \
                                        text = 'Other Patient Information:')
        
        #PATIENT ID
        self.edit_keyLbl.pack(side = 'left')
        self.edit_keyEntry = Tr.Entry(self.edit_keyLbl, \
                                        width = 4)
        self.edit_keyEntry.insert('end', record_[0])
        
        # NAME
        self.edit_nameLbl.pack(side = 'left')
        self.edit_lnameEntry = Tr.Entry(self.edit_nameLbl,\
                                        width = 15)
        self.edit_nameEntry = Tr.Entry(self.edit_nameLbl, \
                                        width = 15)
        self.edit_mInitialEntry = Tr.Entry(self.edit_nameLbl,
                                        width = 2)
        
      
        self.edit_lnameEntry.insert('end', record_[2])
        self.edit_mInitialEntry.insert('end', record_[3])
        self.edit_nameEntry.insert('end', record_[1])
        
        self.edit_lnameLbl = Tr.Label(self.edit_nameLbl, \
                                        text = 'Last Name                         Name                 M.I.')
        self.edit_lnameLbl.pack(side = 'bottom')
        
        #AGE
        self.edit_ageLbl.pack(side = 'left')
        self.edit_ageEntry = Tr.Entry(self.edit_ageLbl, \
                                        width = 4)
        self.edit_ageEntry.insert('end', record_[4])
        
        #BIRTHDATE
        self.edit_bdayLbl.pack(side = 'left')
        self.edit_nextOfKinEntry = Tr.Entry(self.edit_bdayLbl, \
                                        width = 25)
        self.edit_contacInfoEntry = Tr.Entry(self.edit_bdayLbl, \
                                        width = 12)
        #self.edit_label1 = Tr.Label(self.edit_bdayLbl, text = '/')
        
        
        self.edit_OtherInfoFormatLbl = Tr.Label(self.edit_bdayLbl, \
                                        text = ' Next of Kin                   Contact Info ')
        
        self.edit_nextOfKinEntry.insert('end', record_[5])
        self.edit_contacInfoEntry.insert('end', record_[6])
        
        # self.edit_dateFormatLbl.pack(side = 'bottom')
        
        self.edit_keyEntry.pack(side = 'left')
        self.edit_mInitialEntry.pack(side = 'right')
        self.edit_nameEntry.pack(side = 'right')
        self.edit_lnameEntry.pack(side = 'right')
        self.edit_ageEntry.pack(side = 'right')
        self.edit_nextOfKinEntry.pack(side = 'left')
        #self.edit_label2.pack(side = 'left')
        self.edit_contacInfoEntry.pack(side = 'left')
        #self.edit_label1.pack(side = 'left')

        
        # Setup the buttons and frames
        self.edit_save_btn.pack(side = 'right')
        self.edit_cancel_btn.pack(side = 'left')
        self.edit_delete_btn.pack(side = 'left')
        self.pHistory_btn.pack(side = 'top')
        
        # previous
        self.frame1.pack(side = 'bottom')
        self.frame2.pack(side = 'top')
        self.frame3.pack(side = 'top')
        self.frame4.pack(side = 'top')
        self.frame5.pack(side = 'top')
        self.frame6.pack(side = 'top')
        self.frame7.pack(side = 'bottom')
        
        

    # The following function saves the records to the database
    # The function also checks that none of the Entries are empty or null   
    def save_record(self):
                
        if  self.keyEntry.get() == '' or  self.nameEntry.get() == '' or \
            self.ageEntry.get() == '' or self.nextOfKin.get() == '' or \
            self.lnameEntry.get() == '' or self.contactInfo.get() == '':
            if self.nameEntry.get() == '' or self.lnameEntry.get() == '':
                ers.errors().general_error_messages('NAME')
                self.nameLbl.set('NAME:', fg = 'red')
            if self.ageEntry.get() == '':
                ers.errors().general_error_messages('AGE')
            if self.dayEntry.get() == '' or self.monthEntry.get() == '' or\
                self.yearEntry.get() == '':
                ers.errors().general_error_messages('BIRTHDAY')
        else:
 
            if self.mInitialEntry.get() == '':
                name_ = self.nameEntry.get() + ' ' + self.lnameEntry.get() 
            else:
                id_ = int(self.keyEntry.get())
                name_ = self.nameEntry.get()
                mi_ = self.mInitialEntry.get()
                lname_ = self.lnameEntry.get()

                age_ = int(self.ageEntry.get())
                nextOfkin_ = self.nextOfKin.get()
                cinfo_ = int(self.contactInfo.get())
                db.database().insert_record_patient('patient1.db', (id_, lname_, name_, mi_, age_, nextOfkin_, cinfo_))
                self.clear_()
                self.clear_search() # refreshes the treeview to include the new record
        
    # Clear all Entries and focus on nameEntry
    def clear_(self):
        
        self.keyEntry.delete(0, Tr.END)
        self.nameEntry.delete(0, Tr.END)
        self.lnameEntry.delete(0,Tr.END)
        self.mInitialEntry.delete(0, Tr.END)
        self.nextOfKin.delete(0, Tr.END)
        self.contactInfo.delete(0, Tr.END)
        self.nameEntry.focus()
        self.column_headings()
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
    
    # Cancels the new new_patient_win
    # This function can only be used with new patient
    def cancel_(self):
        # Destroys the new_patient_window
        self.new_patient_window.destroy()
    
    # Deletes patient record    
    def delete_patient(self):
        #this function also deletes the patient personal database

        name_ = self.edit_nameEntry.get()
        print(name_)
        st = name_
        
        result = ers.errors().delete_confirmation(st)
        
        if result == True:
            db.database().remove_record('patient1.db', 'PATIENT', name_)
            
            ers.errors().delete_message(st)
            self.edit_patient_window.destroy()      # Destroys the window
            self.clear_search()                     # Refresh patien list 
        else:
            self.edit_nameEntry.focus()             # Set focus on edit_nameEntery
        
    # Cancel the edit
    def cancel_edit(self):
        # Destroys the edit_patient_window
        self.edit_patient_window.destroy()
    
    # Function saves changes made to the patient
    def save_edit(self):
        # Saves the edit record
        key_ = int(self.edit_keyEntry.get())

        name_ = self.edit_nameEntry.get() 
        lname_ = self.edit_lnameEntry.get() 
        mi_ = self.edit_mInitialEntry.get()

        age_ = int(self.edit_ageEntry.get())
        nOfKin_ = self.edit_nextOfKinEntry.get()
        cinfo_ = int(self.edit_contacInfoEntry.get())
        
        red_ = (name_, lname_, mi_, age_, nOfKin_,cinfo_, key_)
        db.database().update_patient_record('patient1.db',red_)  
        
        #self.clear_()
        self.clear_search() # refreshes the treeview to include the new record
        self.cancel_edit()
        
    # OnClick opens a new window when a record in the patient list is clicked 
    def OnClick(self, event):
        
        selection = self.recordListColumn.focus()
        value = self.recordListColumn.item(selection).get('values')
        # Opens the edit patient window
        # and passes the patient id#
        self.editPatient(value[0])
        
    # Creates a separate table with the patient ID
    def blood_sugar_level(self):
        
        selection = self.recordListColumn.focus()
        value = self.recordListColumn.item(selection).get('values')
        # value[0] is the Patient ID. value[0] must be a string
        # Creates a new table for the specific patient
        db_name = 'patient1.db'
        db.database().patient_tables(db_name)
        title = self.edit_nameEntry.get() + "'s Medical History"
        id_ = self.edit_keyEntry.get()
        self.edit_patient_window.destroy()
        graph.graph().graph(title, db_name, id_)
        
    # Clears the recordListColum
    def clear_list(self):
    #this process can be done two ways
        # way # 1
        for item in self.recordListColumn.get_children():
            self.recordListColumn.delete(item)
        # way #2
        ''' self.reordListColumn.delete(*self.recordListColumn.get_children())
        '''
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))   
    # Opens the search window    
    def search_(self):
        
        if  self.search_entry.get() == '' or  self.selection_box.get() == 'Select': 
            if self.search_entry.get() == '':
                ers.errors().general_error_messages('NAME')
            if self.selection_box.get() == 'Select':
                ers.errors().general_error_messages('Please select a search criteria')
        else:
            if self.selection_box.get() == 'Patient Number':
                #To check that patient number is integer
                if self.IsAnInt(self.search_entry.get()) == True:
                    id_ = 'ID'
                    self.search_items(id_, self.search_entry.get())
                else:
                    ers.errors().integer_error(self.search_entry.get())
            if self.selection_box.get() == 'Patient Name':
                id_ = 'NAME'
                self.search_items(id_, self.search_entry.get())
            if self.selection_box.get() == 'Patient Last Name':
                id_ = 'LASTNAME'
                self.search_items(id_, self.search_entry.get())
            if self.selection_box.get() == 'Middle Initial':
                id_ = 'MINITIAL'
                self.search_items(id_, self.search_entry.get())
            if self.selection_box.get() == 'Age':
                id_ = 'AGE'
                self.search_items(id_, self.search_entry.get())
            if self.selection_box.get() == 'Next of Kin':
                id_= 'NEXTOFKIN'
                self.search_items(id_, self.search_entry.get())
            if self.selection_box.get() == 'Contact info':
                id_ = 'CONTACTINFO'
                self.search_items(id_, int(self.search_entry.get()))
            if self.selection_box.get() == 'Diagnosis':
                self.specific_search(self.general_query_diagnosys(self.search_entry.get()))
            if self.selection_box.get() == 'Allergies':
                self.specific_search(self.general_query_allergies(self.search_entry.get()))
            if self.selection_box.get() == 'General Search':
                self.specific_search(self.general_query_statement_a())
            if self.selection_box.get() == 'Advance Search':
                self.specific_search(self.general_query_patient(self.search_entry.get()))
    
    #search_items function looks for specific items        
    def search_items(self, name, key):
        self.clear_list() # clear the list
        count = 0
        for item in db.database().print_results('patient1.db', name, key):
            count = count + 1
            if count % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))
                        
        #colors the row
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey') 
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
        count = 0  
        
    def general_search_items(self, key):
        self.clear_list() # clear the list
        count = 0
        # This is just a test for my new function
        self.col_headers(self.general_query_statement_a())
        for item in db.database().db_general_print('patient1.db', self.general_query_statement_a()):
            count = count + 1
            if count % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))
                        
        #colors the row
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey') 
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
        count = 0   
        
    def specific_search(self, key):
        self.clear_list() # clear the list
        count = 0
        # Names column headers to display results
        self.col_headers(key)
        
        # displays results
        for item in db.database().db_general_print('patient1.db', key):
            count = count + 1
            if count % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))
                        
        #colors the row
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey') 
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
        count = 0    
    
    # Clears the search criteria 
    # this helper function can also be used to refresh the patient list after a patient
    # has been added or updated        
    def clear_search(self):
        
        self.selection_box.current(0)       #selection_box goes back to its default value
        self.search_entry.delete(0, Tr.END)
        self.clear_list()
        count = 0
        for item in db.database().db_print('patient1.db'):
            count = count + 1
            if count % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))
                        
        #colors the row
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey') 
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
        count = 0
        self.column_headings()
    
    # The following helper function helps to check for integer
    def IsAnInt(self, key):
             
        try:
            int(key)
            return True
        except ValueError:
            return False
    
    # this functions splits any sentence and returns and array
    def sentence_split(self, phrase, where):
        
        wds = phrase.split(where)
        return wds
    
    # this is an even driven search, when the user presses enter        
    def Event_Driven_Search(self, event):
        
        self.search_()
        
    # the following functions displays the patient history database
    def patien_history(self):
        
        self.show_patient_history('patient1.db')

    # show_patient_history will display the PATIENT_HIS table when the PATIENT HISTORY button is pressed
    def show_patient_history(self, db_):
        
        #self.dataCols = ('PATIENT ID', 'LAST NAME', 'NAME', 'MI','AGE', 'NEXT OF KIN', 'CONTACT INFO')
        self.recordListColumn.heading('PATIENT ID', text = 'PATIENT ID')
        self.recordListColumn.heading('LAST NAME', text = 'GENDER')
        self.recordListColumn.heading('NAME', text = 'WEIGHT (lbs)')
        self.recordListColumn.heading('MI', text = 'DIAGNOSIS') 
        self.recordListColumn.heading('AGE', text = 'DATE')
        self.recordListColumn.heading('NEXT OF KIN', text = 'ENTHNICITY')
        self.recordListColumn.heading('CONTACT INFO', text = 'ALLERGIES')
            
        self.clear_list()
        self.recordListColumn.column(self.dataCols[0], width = 80)
        self.recordListColumn.column(self.dataCols[1], width = 100)
        self.recordListColumn.column(self.dataCols[2], width = 100)
        self.recordListColumn.column(self.dataCols[3], width = 100)
        self.recordListColumn.column(self.dataCols[4], width = 100)
        self.recordListColumn.column(self.dataCols[5], width = 100)
        self.recordListColumn.column(self.dataCols[6], width = 100)
        
        cnt = 0
        for item in db.database().db_patient_history_print(db_):
            cnt = cnt + 1
            if cnt % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))            
        cnt = 0
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey') 
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
    
    # column_headings will display the database default table: PATIENT   
    def column_headings(self):

        self.recordListColumn.heading('PATIENT ID', text = 'PATIENT ID')
        self.recordListColumn.heading('LAST NAME', text = 'LAST NAME')
        self.recordListColumn.heading('NAME', text = 'NAME')
        self.recordListColumn.heading('MI', text = 'MI') 
        self.recordListColumn.heading('AGE', text = 'AGE')
        self.recordListColumn.heading('NEXT OF KIN', text = 'NEXT OF KIN')
        self.recordListColumn.heading('CONTACT INFO', text = 'CONTACT INFO')
        
        self.clear_list()
        self.recordListColumn.column(self.dataCols[0], width = 80)
        self.recordListColumn.column(self.dataCols[1], width = 130)
        self.recordListColumn.column(self.dataCols[2], width = 130)
        self.recordListColumn.column(self.dataCols[3], width = 30)
        self.recordListColumn.column(self.dataCols[4], width = 30)
        self.recordListColumn.column(self.dataCols[5], width = 180)
        self.recordListColumn.column(self.dataCols[6], width = 140)
       
        count = 0
        for item in db.database().db_print('patient1.db'):
            count = count + 1
            if count % 2 != 0:
                self.recordListColumn.insert('', 'end', values=item, tags = ('oddrow',))
            else:
                self.recordListColumn.insert('', 'end', values=item, tags = ('evenrow',))
        
        #colors the row
        self.recordListColumn.tag_configure('oddrow', background = 'lightgrey')   
        self.records_lable.config(text = "TOTAL RECORDS: " + str(len(self.recordListColumn.get_children())))
        
    def general_query_statement(self):   
        condition =  "SELECT PATIENT.NAME, PATIENT.LASTNAME, PATIENT.AGE, \
                        PATIENT_HIST.GENDER, PATIENT_HIST.WEIGHT, PATIENT_HIST.ALERGIES, PATIENT_HIST.ETHNICITY \
                        FROM  PATIENT, PATIENT_HIST \
                        WHERE PATIENT.ID = PATIENT_HIST.PATIENT_ID \
                        ORDER BY PATIENT.AGE DESC"
        return condition
                           
    def general_query_statement_a(self):   
        condition = "SELECT PATIENT.NAME, PATIENT.LASTNAME, PATIENT.AGE, \
                        PATIENT_HIST.GENDER, PATIENT_HIST.WEIGHT, PATIENT_HIST.ALERGIES, PATIENT_HIST.ETHNICITY \
                        FROM  PATIENT, PATIENT_HIST \
                        WHERE PATIENT.ID = PATIENT_HIST.PATIENT_ID \
                        ORDER BY PATIENT_HIST.ETHNICITY AND PATIENT.AGE "
        return condition
    
    def general_query_diagnosys(self, key_):   
        condition = "SELECT PATIENT.ID, PATIENT.NAME, PATIENT.LASTNAME, PATIENT.AGE, \
                        PATIENT_HIST.DIAGNOSIS, PATIENT_HIST.DATE\
                        FROM  PATIENT JOIN PATIENT_HIST \
                        ON PATIENT.ID = PATIENT_HIST.PATIENT_ID \
                        WHERE UPPER(PATIENT_HIST.DIAGNOSIS) LIKE '%" + ((key_).upper()) + "%'" + \
                        "ORDER BY PATIENT_HIST.GENDER " 
        return condition

    def general_query_allergies(self, key_):   
        condition = "SELECT PATIENT.ID, PATIENT.NAME, PATIENT.LASTNAME, \
                        PATIENT_HIST.ALERGIES\
                        FROM  PATIENT JOIN PATIENT_HIST \
                        ON PATIENT.ID = PATIENT_HIST.PATIENT_ID \
                        WHERE UPPER(PATIENT_HIST.ALERGIES) LIKE '%" + (key_).upper() + "%'"
                        
        return condition
    
    def general_query_treatment(self, key_):
        condition = "SELECT PATIENT.LASTNAME, TREATMENT.DOCTOR, PATIENT_HIST.DIAGNOSIS, TREATMENT.TREATMENT_ID,\
                            TREATMENT.DESCRIPTION, TREATMENT.START_DATE, TREATMENT.FREQUENCY \
                            FROM PATIENT \
                            JOIN PATIENT_HIST ON PATIENT_HIST.PATIENT_ID = TREATMENT.PATIENT_ID \
                            JOIN TREATMENT ON TREATMENT.PATIENT_ID = PATIENT.ID \
                            WHERE UPPER(PATIENT.LASTNAME) LIKE '%" + (key_).upper() + "%'" 
        
        return condition
        
    def general_query_patient(self, key_):
        condition = "SELECT ID, NAME, LASTNAME, MINITIAL, AGE \
                        NEXTOFKIN, CONTACTINFO \
                        FROM  PATIENT \
                        WHERE UPPER(ID) LIKE '%" + (key_).upper() + "%'" +  \
                           "OR UPPER(NAME) LIKE ''%" + (key_).upper() + "%'" +  \
                           "OR UPPER(LASTNAME) LIKE '%" + (key_).upper() + "%'"  + \
                           "OR UPPER(MINITIAL) LIKE '%" + (key_).upper()  + "%'"  + \
                           "OR UPPER(AGE) LIKE '%" + (key_).upper()  + "%'"  + \
                           "OR UPPER(NEXTOFKIN) LIKE '%" + (key_).upper()  + "%'"  + \
                           "OR UPPER(CONTACTINFO) LIKE '%" + (key_).upper()  + "%'"
                
        return condition
    
    def general_query_phistory(self, key_):
        condition = "SELECT * \
                        FROM PATIENT_HIST \
                        WHERE UPPER(PATIENT_ID) = " + (key_).upper()

        return condition
        
    # col_headers gets the column headers from the statement
    def col_headers(self, statement):
        result = []
        list_ = statement.split(' ')
        
        # the following loop only adds the column names and ignore other characters inside the list
        for c in list_:
            if c == 'FROM':
                break
            if c == "":
                continue
            if c == "\n":
                continue
            else:
                result.append(c)
                 
        cnt = 0       
        # column titles
        for val in result[1:len(result)]:
            l_ = val.split('.')
            
            if cnt < (len(result) -1):
                self.recordListColumn.heading(self.dataCols[cnt], text = l_[1].replace(',', ''))
            else:
                self.recordListColumn.heading(self.dataCols[cnt], text = l_[1])
            cnt = cnt + 1
        
        # column widths
        if len(result) < 7:
            for n in range (0, len(result)):
                self.recordListColumn.column(self.dataCols[n], width = 100)
            for n in range(len(result)-1,len(result)+(7-len(result))):
                self.recordListColumn.heading(self.dataCols[n], text = '')
        else:
            for n in range(0, len(result)-1):
                self.recordListColumn.column(self.dataCols[n], width = 100)
                
     
    

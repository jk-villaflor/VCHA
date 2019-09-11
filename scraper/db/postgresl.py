#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2
import pandas as pd

from psycopg2.pool import SimpleConnectionPool
from model.Property import Property


class PropertyDAO:
    
    def __init__(self):  
        #self.postgreSQL_pool = SimpleConnectionPool(5, 20, user = "adminuser",
        #                                      password = "admin123",
        #                                      host = "gfpostgres.ccqysqxekuuh.us-east-2.rds.amazonaws.com",
        #                                      port = "5432",
        #                                      database = "rentproperty")
        #if(self.postgreSQL_pool):
        #    print("Connection pool created successfully")
        pass

    
    def getConnection(self):
        try:
            #conn  = self.postgreSQL_pool.getconn()
            conn = psycopg2.connect(user = "adminuser",
                                              password = "admin123",
                                              host = "gfpostgres.ccqysqxekuuh.us-east-2.rds.amazonaws.com",
                                              port = "5432",
                                              database = "rentproperty")
        except:
            print ("I am unable to connect to the database")
        
        return conn;
    
    def getRecords(self, limit):
        conn = self.getConnection()           
        cur = conn.cursor()
        
        print("Select from rentproperty database")
        if(limit > 0):
            query = "SELECT id, fulldescription, characteristics, title from rentproperty where finished = false and (fulldescription is not null OR fulldescription <> '') limit " + str(limit)
        else:
            query = "SELECT id, fulldescription, characteristics, title from rentproperty where finished = false and (fulldescription is not null OR fulldescription <> '')"
            
        cur.execute(query)
        
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        return rows;
    
    def getNoSuitLaundryRecords(self, limit):
        conn = self.getConnection()           
        cur = conn.cursor()
        
        print("Select from rentproperty with no suit laundry database")
        if(limit > 0):
            query = "SELECT id, fulldescription, characteristics, title from rentproperty where suit_laundry = false limit " + str(limit)
        else:
            query = "SELECT id, fulldescription, characteristics, title from rentproperty where suit_laundry = false "
            
        cur.execute(query)
        
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        return rows;
    
    def getNoRoomSizeRecords(self, limit):
        conn = self.getConnection()           
        cur = conn.cursor()
        
        print("Select from rentproperty with no bedroom number database")
        if(limit > 0):
            query = "SELECT id, fulldescription, characteristics, title from rentproperty where bedrooms <= 0 limit " + str(limit)
        else:
            query = "SELECT id, fulldescription, characteristics, title from rentproperty where bedrooms <= 0 "
            
        cur.execute(query)
        
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        return rows;

    def getNoSizeRecords(self, limit):
        conn = self.getConnection()           
        cur = conn.cursor()
        
        print("Select from rentproperty with no size records database")
        if(limit > 0):
            query = "SELECT id, fulldescription, title, characteristics from rentproperty where size_sqft <= 0 limit " + str(limit)
        else:
            query = "SELECT id, fulldescription, title, characteristics from rentproperty where size_sqft <= 0 "
            
        cur.execute(query)
        
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        return rows;
    
    def getNoBathRecords(self, limit):
        conn = self.getConnection()           
        cur = conn.cursor()
        
        print("Select from rentproperty with no bathroom database")
        if(limit > 0):
            query = "SELECT id, fulldescription, title, characteristics from rentproperty where bath is null limit " + str(limit)
        else:
            query = "SELECT id, fulldescription, title, characteristics from rentproperty where bath is null "
            
        cur.execute(query)
        
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()        
        
        return rows;


    def getRecordsWithNoLocation(self, limit = 0):
        conn = self.getConnection()           
        cur = conn.cursor()
        
        print("Select from rentproperty with no location database")
        if(limit > 0):
            query = "SELECT id, fulldescription, title, characteristics, link from rentproperty where location is null limit " + str(limit)
        else:
            query = "SELECT id, fulldescription, title, characteristics, link from rentproperty where location is null "
            
        cur.execute(query)
        
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        return rows;
    
    def getRecord(self, rId):
        conn = self.getConnection()     
        cur = conn.cursor()
        query = "SELECT id, fulldescription, title, characteristics from rentproperty where id = " + str(rId)
        cur.execute(query)
        rows = cur.fetchall()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        return rows;
    
    def updateRoomRecord(self, property : Property):
        conn = self.getConnection()
        query = 'UPDATE rentproperty SET bedrooms=%s WHERE id=%s'
        cur = conn.cursor()
        cur.execute(query, (property.rooms, property.id))
        conn.commit()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
    
    def updateSuitLaundryRecord(self, property : Property):
        conn = self.getConnection()
        query = 'UPDATE rentproperty SET suit_laundry=%s WHERE id=%s'
        cur = conn.cursor()
        cur.execute(query, (property.suitLaundry, property.id))
        conn.commit()
       
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        

    def updateSizeRecord(self, property : Property):
        conn = self.getConnection()
        query = 'UPDATE rentproperty SET size_sqft=%s WHERE id=%s'
        cur = conn.cursor()
        cur.execute(query, (property.size, property.id))
        conn.commit()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
    
    def updateBathRecord(self, property : Property):
        conn = self.getConnection()
        query = 'UPDATE rentproperty SET bath=%s WHERE id=%s'
        cur = conn.cursor()
        cur.execute(query, (property.bath, property.id))
        conn.commit()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
    
    def updateLocationRecord(self, location, properties):
        conn = self.getConnection()
        query = 'UPDATE rentproperty SET location=%s WHERE id in %s'
        cur = conn.cursor()
        cur.execute(query, (location, tuple(properties)))
        conn.commit()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        
    def updateRecord(self, property : Property):
        conn = self.getConnection()
        query = 'UPDATE rentproperty SET bedrooms=%s, size_sqft=%s, professionally_managed=%s, no_pet_allowed=%s, suit_laundry=%s, park_stall=%s, available_now=%s, amenities=%s, near_school=%s, brand_new=%s, finished=true WHERE id=%s'
        cur = conn.cursor()
        cur.execute(query, (property.rooms, property.size, property.profMan, property.nopet, property.suitLaundry, property.parkStall, property.availNow, property.amenities, property.nearSchool, property.brandNew, property.id))
        conn.commit()
        
        cur.close()
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        
    def getDataFrameRecords(self, where):
        store = pd.HDFStore('../data/properties.h5')
        print(store.keys())
        if '/df' in store.keys():
            properties = store.get('df')
        else:
            conn = self.getConnection()
            sql = "select * from vw_property_normalized " + where
            properties = pd.read_sql_query(sql, conn)
            store.put('df', properties)
            conn.close()

        store.close()
        
        return properties
    
    def getDataFrameRecord(self, id):
        conn = self.getConnection()
        sql = "select * from vw_property_normalized where id = {}".format(id)
        properties = pd.read_sql_query(sql, conn)
        
        #self.postgreSQL_pool.putconn(conn)
        conn.close()
        
        return properties
    

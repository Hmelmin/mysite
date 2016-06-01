from mysql import connector

class DatabaseManager:
    def __init__(self):
        self.connector = connector.connect(user='root', password='12345678',
                              host='127.0.0.1',
                              database='test')
        self.cursor = self.connector.cursor()
        self.tr = 0
        self.ev = 0

    def close(self):
        self.cursor.close()
        self.connector.close()

    def deletePlanes(self):
        delete = "DELETE FROM planes"
        self.cursor.execute(delete,())
        self.connector.commit()

    def deleteAirlines(self):
        delete = "DELETE FROM airlines"
        self.cursor.execute(delete,())
        self.connector.commit()

    def deleteAirports(self):
        delete = "DELETE FROM airports"
        self.cursor.execute(delete,())
        self.connector.commit()

    def loadPlanes(self):
        load = "LOAD DATA INFILE 'planes.csv'\
                INTO TABLE planes\
                FIELDS TERMINATED BY ';'\
                ENCLOSED BY '\"'\
                LINES TERMINATED BY'\\n' \
                IGNORE 1 ROWS"
        print (load)
        self.cursor.execute(load,())
        self.connector.commit()

    def loadAirlines(self):
        load = "LOAD DATA INFILE 'airlines.csv'\
                INTO TABLE airlines\
                FIELDS TERMINATED BY ';'\
                ENCLOSED BY '\"'\
                LINES TERMINATED BY '\\n' \
                IGNORE 1 ROWS"
        print(load)
        self.cursor.execute(load,())
        self.connector.commit()

    def loadAirports(self):
        load = "LOAD DATA INFILE 'airports.csv'\
                INTO TABLE airports\
                FIELDS TERMINATED BY ';'\
                ENCLOSED BY '\"' \
                LINES TERMINATED BY '\\n' \
                IGNORE 1 ROWS"
        print(load)
        self.cursor.execute(load,())
        self.connector.commit()

    def prepare(self):
        self.deletePlanes()
        self.loadPlanes()
        self.deleteAirlines()
        self.loadAirlines()

        self.deleteAirports()
        self.loadAirports()

    def GetLastIdFromAirports(self):
        get_last_id = "SELECT MAX(id) as x FROM airports"
        self.cursor.execute(get_last_id ,())
        max = self.cursor.fetchone()[0]
        if max is not None:
            return max
        else:
            return 0

    def InsertAirport(self, country, city):
        id = self.GetLastIdFromAirports() + 1
        add_airport = "INSERT INTO airports VALUES(%s,%s, %s)"
        self.cursor.execute(add_airport, (id, country, city))
        self.connector.commit()


    def GetLastIdFromAirlines(self):
        get_last_id = "SELECT MAX(id) as x FROM airlines"
        self.cursor.execute(get_last_id ,())
        max = self.cursor.fetchone()[0]
        if max is not None:
            return max
        else:
            return 0


    def InsertAirline(self, name):
        id = self.GetLastIdFromAirlines() + 1
        add_airport = "INSERT INTO airlines VALUES(%s,%s)"
        self.cursor.execute(add_airport, (id, name))
        self.connector.commit()

    def GetLastIdFromPlanes(self):
        get_last_id = "SELECT MAX(id) as x FROM planes"
        self.cursor.execute(get_last_id ,())
        max = self.cursor.fetchone()[0]
        if max is not None:
            return max
        else:
            return 0


    def InsertPlane(self, model, type):
        id = self.GetLastIdFromPlanes() + 1
        add_airport = "INSERT INTO planes VALUES(%s,%s, %s)"
        self.cursor.execute(add_airport, (id, model, type))
        self.connector.commit()


    def GetLastIdFromFlights(self):
        get_last_id = "SELECT MAX(id) as x FROM flights"
        self.cursor.execute(get_last_id ,())
        max = self.cursor.fetchone()[0]
        if max is not None:
            return max
        else:
            return 0


    def SelectAllFlights(self):
        get_flights = "select f.id, al.name, ap1.city as departure ,  ap2.city as destination, p.model,f.departure_time \
                        from flights f, airlines al, airports ap1,planes p,airports ap2\
                        where p.id = f.plane_id and al.id = f.airlines_id and ap1.id = f.departure_id and ap2.id = f.destination_id \
                        order by f.id"
        self.cursor.execute(get_flights, ())
        return self.cursor.fetchall()

    def SelectAllAirlines(self):
        get_airlines = "select * from airlines"
        self.cursor.execute(get_airlines, ())
        return self.cursor.fetchall()


    def SelectAllAirports(self):
        get_airports = "select * from airports"
        self.cursor.execute(get_airports, ())
        return self.cursor.fetchall()

    def SelectAllPlanes(self):
        get_planes = "select * from planes"
        self.cursor.execute(get_planes, ())
        return self.cursor.fetchall()


    def SelectFlightById(self,id):
        get_flight = "select * from flights where id = "  + str(id)
        self.cursor.execute(get_flight, ())
        return self.cursor.fetchone()

    def GetLastIdFromFlights(self):
        get_last_id = "SELECT MAX(id) as x FROM flights"
        self.cursor.execute(get_last_id ,())
        max = self.cursor.fetchone()[0]
        if max is not None:
            return max
        else:
            return 0


    def InsertFlight(self,id,  airlines, departure, destination, plane, time_out):
        set_flight = " INSERT INTO FLIGHTS VALUES (%s,  %s  ,%s,  %s,  %s,  %s)"
        self.cursor.execute(set_flight, (id , airlines, departure, destination, plane, time_out))
        self.connector.commit()


    def DeleteFlight(self,id):
        delete = " DELETE FROM flights WHERE id =  " + str(id)
        self.cursor.execute(delete , ())
        self.connector.commit()

    def EditFlight(self, id,  airlines, departure, destination, plane, time_out):
        edit_flight = " UPDATE flights SET airlines_id = %s , departure_id = %s , destination_id = %s , plane_id =  %s , departure_time = %s WHERE id = %s;"
        self.cursor.execute(edit_flight , (airlines, departure, destination , plane, time_out , id))
        self.connector.commit()

    def SearchSelect(self, out_list, in_list, date1,date2, plane, airline):
        select_text = "select f.id, al.name, ap1.city as departure ,  ap2.city as destination, p.model,f.departure_time \
                        from flights f, airlines al, airports ap1,planes p,airports ap2 \
                        where p.id = f.plane_id and al.id = f.airlines_id and ap1.id = f.departure_id and ap2.id = f.destination_id "
        if len(out_list) > 0:
            select_text = select_text + "and f.departure_id in (" + ", ".join(out_list) + ") order by f.id"
        elif len(in_list) > 0:
            select_text = select_text + "and f.destination_id in (" + ", ".join(in_list) + ") order by f.id"
        elif len(date1) > 0 and len(date2)>0 :
            select_text = select_text + "and f.departure_time BETWEEN " +"'" + date1 +"'"+ " AND "+"'" + date2 +"'"  + " order by f.id"
        elif len(plane) > 0:
            plane = "+(+" + plane
            plane = plane.replace(" ", " +")
            select_text = select_text +  "and MATCH (p.model) AGAINST ('"+plane+")' IN BOOLEAN MODE)"
            print(select_text)
        elif len(airline) > 0:
            select_text = select_text + "and MATCH (al.name) AGAINST ('+\"" +airline+"\"' IN BOOLEAN MODE)"
        else:
            select_text = select_text + "order by f.id"
        print(select_text)

        self.cursor.execute(select_text, ())
        result = self.cursor.fetchall()
        print result
        return result

    def event(self, long, period):
        if self.ev == 0 :
            self.ev = 1
            schedule = "SET GLOBAL event_scheduler = ON;"
            self.cursor.execute(schedule,())
            event_query = "CREATE EVENT if not exists test_event_n1000 \n\
                            ON SCHEDULE AT CURRENT_TIMESTAMP "
            if len(long)>0 and len(period)>0:
                event_query = event_query + "+ INTERVAL " +long + " " + period + "\n"

            event_query= event_query+"ON COMPLETION PRESERVE \n\
                                      DO \n\
                                      update flights \n\
                                      set departure_time = '2016-04-01' where id <6;"

            print(event_query)

            self.cursor.execute(event_query,())

    def trigger(self):
        if self.tr ==0 :
            self.tr =1
            drop = "drop trigger if exists trigger2"
            self.cursor.execute(drop, ())
            query = "CREATE TRIGGER trigger2 \n\
                     AFTER INSERT on flights \n\
                     FOR EACH ROW \n\
                     BEGIN \n\
 	                 update airports set city = 'Hamburg' where country = 'Germany';\
                     END"
            print(query)
            self.cursor.execute(query,())










dm = DatabaseManager()
#dm.InsertAirport("Ukraine","Lviv")
#print(dm.GetLastIdFromAirports())
dm.close()


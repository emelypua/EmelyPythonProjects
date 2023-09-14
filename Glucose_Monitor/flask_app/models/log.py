from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models import user
from flask import flash

class Log:
    DB = 'project_glucose'
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.date = data['date']
        self.time = data['time']
        self.glucose = data['glucose']
        self.mealtype = data['mealtype']
        self.log_meal = data['log_meal']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.patient = None

    @classmethod
    def get_all_reports(cls):
        query = """
                SELECT * FROM logs
                JOIN users on logs.user_id = users.id;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        glucose_readings = []
        for row in results:
            reading = cls(row)
            data = {
                        "id": row['user_id'],
                        "first_name": row['first_name'],
                        "last_name": row['last_name'],
                        "email": row['email'],
                        "password": row['password'],
                        "created_at": row['users.created_at'],
                        "updated_at": row['users.updated_at']
                }
            reading.patient = user.User(data)
            glucose_readings.append(reading)
            
        return glucose_readings

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM logs
                JOIN users on logs.user_id = users.id
                WHERE logs.id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query,data)
        # if not result:
        #     return False
        result = result
        reading = cls(result[0])
        data = {
                "id": result[0]['users.id'],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": "",
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
        }
        reading.patient = user.User(data)
        print(reading.patient.first_name)
        return reading
    
    @classmethod
    def save_report(cls, data):
        parce_data = cls.parce_form(data)
        print (parce_data)
        query ="""
                    INSERT INTO logs(user_id, date, time, glucose, mealtype, log_meal)
                    VALUES( %(user_id)s, %(date)s,%(time)s,%(glucose)s,%(mealtype)s,%(log_meal)s)
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query, parce_data)
        return result

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM logs WHERE id = %(id)s";
        result = connectToMySQL(cls.DB).query_db( query, data)
        return cls(result[0])

    @classmethod
    def destroy_report(cls, data):
        query = "DELETE FROM logs WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update_report(cls, data):
        query = """UPDATE logs SET date=%(date)s, time=%(time)s, glucose=%(glucose)s, mealtype= %(mealtype)s, log_meal= %(log_meal)s  WHERE id=%(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result


    @staticmethod
    def validate_report(data):
        is_valid = True
        if len(data['date']) < 1:
            flash ('We need to know the date of your reading.', 'create')
            is_valid = False
        if len(data['mealtype']) < 1:
            flash('We need to know if this was breakfast, lunch, dinner or a snack.', "create")
            is_valid = False
        if 'log_meal' not in data:
            flash('We want to know what you ate that gave you this reading. Please fill your meal log.', "create")
            is_valid = False

        return is_valid
    
    @staticmethod
    def parce_form(data):
        parce_data ={} 
        # if creating should print "we are creatin a log" then if editing should parce{cleaning} data
        try:
            if data['id']:
                parce_data['id'] = data['id']
        except:
            print('We are creating a log')
        #if the form has a user_id hidden input then it'll add user_id as needed
        if data['user_id']:
            parce_data['user_id'] =  data['user_id']
        if len(data['time']) == 8:
            parce_data['time'] =  data['time']
        else:
            parce_data['time'] = f"{data['time']}:00"
        parce_data['date'] =  data['date']
        parce_data['glucose'] =  data['glucose']
        parce_data['mealtype'] =  data['mealtype']
        parce_data['log_meal'] =  data['log_meal']
        return parce_data


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import joblib
import pandas as pd
import warnings
#warnings.filterwarnings('ignore')


app = Flask(__name__)

# Secret key for session management. You can generate a random key.
app.secret_key = 'raymond123'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'leenawastepaper'
app.config['MYSQL_DB'] = 'company'

#importing model and scaler
model = joblib.load('model/model.pkl')
scaler = joblib.load('model/scaler.pkl')

BusinessTravel = ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely']
Department = ['Human Resources', 'Research & Development', 'Sales']
Education = ['Bachelor', 'Below College', 'College', 'Doctor', 'Master']
EnvironmentSatisfaction = ['High', 'Low', 'Medium', 'Very High']
JobRole = ['Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager', 'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive', 'Sales Representative']
JobSatisfaction = ['High', 'Low', 'Medium', 'Very High']
MaritalStatus = ['Divorced', 'Married', 'Single']
RelationshipSatisfaction = ['High', 'Low', 'Medium', 'Very High']
WorkLifeBalance = ['Bad', 'Best', 'Better', 'Good']
cat_var = [BusinessTravel, Department, Education, EnvironmentSatisfaction, JobRole, JobSatisfaction, MaritalStatus, RelationshipSatisfaction, WorkLifeBalance]
cat_nam = ['BusinessTravel', 'Department', 'Education', 'EnvironmentSatisfaction', 'JobRole', 'JobSatisfaction', 'MaritalStatus', 'RelationshipSatisfaction', 'WorkLifeBalance']
num_var = ['Age','DistanceFromHome','MonthlyIncome','NumCompaniesWorked','PercentSalaryHike','TotalWorkingYears','YearsAtCompany','YearsInCurrentRole']

def data_preprocessing(df):
  df = df.drop(['id'], axis=1)
  df['Gender'] = df['Gender'].replace({'Male': 1, 'Female': 0, 'female': 0, 'male': 1})
  df['OverTime'] = df['OverTime'].replace({'yes': 1, 'no': 0})
  for col_index in range(len(cat_var)):
    col = cat_var[col_index]
    col_name = cat_nam[col_index]
    for i in range(len(col)):
      df[f'{col_name}_{col[i]}'] = 0
  for col_index in range(len(cat_var)):
    col = cat_var[col_index]
    for j in range(df.shape[0]):
      for i in range(len(col)):
        col_name = cat_nam[col_index]
        if df[col_name][j] == col[i]:
          df[f'{col_name}_{col[i]}'][j] = 1
    df = df.drop([col_name], axis=1)

  df[num_var] = scaler.transform(df[num_var])
  return df

mysql = MySQL(app)
username = ''
modify_id= 0
@app.route('/', methods=['GET', 'POST'])
def login():
    global username
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hr_details WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username/password!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT name FROM hr_details WHERE username = %s", (username,))
    name = cursor.fetchone()
    name = name['name']
    return render_template('dashboard.html', name=name)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        id = request.form['id']
        age = request.form['age']
        distance = request.form['DistanceFromHome']
        gender = request.form['Gender']
        monthly_income = request.form['MonthlyIncome']
        num_companies_worked = request.form['NumCompaniesWorked']
        overtime = request.form['OverTime']
        percent_salary_hike = request.form['PercentSalaryHike']
        total_working_years = request.form['TotalWorkingYears']
        years_at_company = request.form['YearsAtCompany']
        years_in_current_role = request.form['YearsInCurrentRole']
        business_travel = request.form['BusinessTravel']
        department = request.form['Department']
        education = request.form['Education']
        environment_satisfaction = request.form['EnvironmentSatisfaction']
        job_role = request.form['JobRole']
        job_satisfaction = request.form['JobSatisfaction']
        marital_status = request.form['MaritalStatus']
        relationship_satisfaction = request.form['RelationshipSatisfaction']
        work_life_balance = request.form['WorkLifeBalance']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(''' INSERT INTO employee_details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                       (id, age, distance, gender, monthly_income, num_companies_worked, overtime, percent_salary_hike, total_working_years, years_at_company, years_in_current_role, business_travel, department, education, environment_satisfaction, job_role, job_satisfaction, marital_status, relationship_satisfaction, work_life_balance))
        mysql.connection.commit()
        cursor.close()
        flash('Employee details added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html')

@app.route('/modify_employee', methods=['GET', 'POST'])
def modify_employee():
    if request.method == 'POST':
        global modify_id
        id = request.form['id']
        modify_id = id
        return redirect(url_for('modify_id'))
    return render_template('modify_employee.html')

@app.route('/modify_id', methods=['GET', 'POST'])
def modify_id():
    id = modify_id
    if request.method == 'POST':
        age = request.form['age']
        distance = request.form['DistanceFromHome']
        gender = request.form['Gender']
        monthly_income = request.form['MonthlyIncome']
        num_companies_worked = request.form['NumCompaniesWorked']
        overtime = request.form['OverTime']
        percent_salary_hike = request.form['PercentSalaryHike']
        total_working_years = request.form['TotalWorkingYears']
        years_at_company = request.form['YearsAtCompany']
        years_in_current_role = request.form['YearsInCurrentRole']
        business_travel = request.form['BusinessTravel']
        department = request.form['Department']
        education = request.form['Education']
        environment_satisfaction = request.form['EnvironmentSatisfaction']
        job_role = request.form['JobRole']
        job_satisfaction = request.form['JobSatisfaction']
        marital_status = request.form['MaritalStatus']
        relationship_satisfaction = request.form['RelationshipSatisfaction']
        work_life_balance = request.form['WorkLifeBalance']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(''' UPDATE employee_details 
                            SET 
                                Age = %s,
                                DistanceFromHome  = %s,
                                Gender = %s,
                                MonthlyIncome = %s,
                                NumCompaniesWorked = %s,
                                OverTime = %s,
                                PercentSalaryHike = %s,
                                TotalWorkingYears = %s,
                                YearsAtCompany = %s,
                                YearsInCurrentRole = %s,
                                BusinessTravel = %s,
                                Department = %s,
                                Education = %s,
                                EnvironmentSatisfaction = %s,
                                JobRole = %s,
                                JobSatisfaction = %s,
                                MaritalStatus = %s,
                                RelationshipSatisfaction = %s,
                                WorkLifeBalance = %s
                            WHERE
                                id = %s;
                                ''', (age, distance, gender, monthly_income, num_companies_worked, overtime, percent_salary_hike, total_working_years, years_at_company, years_in_current_role, business_travel, department, education, environment_satisfaction, job_role, job_satisfaction, marital_status, relationship_satisfaction, work_life_balance, id))
        mysql.connection.commit()
        cursor.close()
        flash('Employee details modified successfully!')
        return redirect(url_for('dashboard'))
    return render_template('modify_id.html', id=id)


@app.route('/show_employees')
def show_employees():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee_details')
    employees = cursor.fetchall()
    return render_template('show_employees.html', employees=employees)

@app.route('/predict_attrition', methods=['GET', 'POST'])
def predict_attrition():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employee_details")
    employee_data = cursor.fetchall()
    cursor.close()

    if not employee_data:
        flash('Employee not found!')
        return redirect(url_for('dashboard'))
    
    id = [i['id'] for i in employee_data]
    features = {
        'id': [i['id'] for i in employee_data],
        'Age': [i['Age'] for i in employee_data],
        'DistanceFromHome': [i['DistanceFromHome'] for i in employee_data],
        'Gender': [i['Gender'] for i in employee_data],
        'MonthlyIncome': [i['MonthlyIncome'] for i in employee_data],
        'NumCompaniesWorked': [i['NumCompaniesWorked'] for i in employee_data],
        'OverTime': [i['OverTime'] for i in employee_data],
        'PercentSalaryHike': [i['PercentSalaryHike'] for i in employee_data],
        'TotalWorkingYears': [i['TotalWorkingYears'] for i in employee_data],
        'YearsAtCompany': [i['YearsAtCompany'] for i in employee_data],
        'YearsInCurrentRole': [i['YearsInCurrentRole'] for i in employee_data],
        'BusinessTravel': [i['BusinessTravel'] for i in employee_data],
        'Department': [i['Department'] for i in employee_data],
        'Education': [i['Education'] for i in employee_data],
        'EnvironmentSatisfaction': [i['EnvironmentSatisfaction'] for i in employee_data],
        'JobRole': [i['JobRole'] for i in employee_data],
        'JobSatisfaction': [i['JobSatisfaction'] for i in employee_data],
        'MaritalStatus': [i['MaritalStatus'] for i in employee_data],
        'RelationshipSatisfaction': [i['RelationshipSatisfaction'] for i in employee_data],
        'WorkLifeBalance': [i['WorkLifeBalance'] for i in employee_data]
    }

        # Convert features to DataFrame
    df = pd.DataFrame(features)
    df = data_preprocessing(df)
    prediction = model.predict(df)
    
    return render_template('predict_attrition.html',ids = id, n = len(id), predictions = prediction)

if __name__ == '__main__':
    app.run(debug=True)

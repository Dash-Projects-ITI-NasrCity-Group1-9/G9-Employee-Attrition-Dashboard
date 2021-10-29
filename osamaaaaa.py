from flask import Flask, render_template, request
from flask.sessions import NullSession
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

file=pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
no_employees=file.shape[0]
avg_age=round(file["Age"].mean())
avg_salary=round(file["MonthlyIncome"].mean())
avg_hours=round(file["HourlyRate"].mean())
fig1 = px.pie(file, names='Attrition' ,title='Attrition',width=350,height=350,template='plotly_dark')
attritionJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
fig2 = px.pie(file, names='MaritalStatus' ,title='MaritalStatus',width=350,height=350,template='plotly_dark')
maritalJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
fig3 = px.pie(file, names='Gender' ,title='Gender',width=350,height=350,template='plotly_dark')
genderJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
fig4 = px.pie(file, names='OverTime' ,title='OverTime',width=350,height=350,template='plotly_dark')
overJSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

file["salary"]=pd.qcut(file["MonthlyIncome"], 4,labels=[">1000",">3000",">5000",">8000"])
ig = px.area(file,x="EmployeeNumber",y="WorkingYears",width=700,height=500,template='plotly_dark')
ig = json.dumps(ig, cls=plotly.utils.PlotlyJSONEncoder)
ig1= px.bar(file[file['Department']=="Sales"]["salary"],width=500,height=500,template='plotly_dark', x="salary")
ig1= json.dumps(ig1, cls=plotly.utils.PlotlyJSONEncoder)
@app.route("/")
def index():
    return render_template('osamaaaaa.html',no_employees=no_employees,avg_age=avg_age,avg_salary=avg_salary,avg_hours=avg_hours,attritionJSON=attritionJSON
    ,maritalJSON=maritalJSON,genderJSON=genderJSON,overJSON=overJSON,ig=ig,ig1=ig1)

@app.route('/callback/<endpoint>')
def callback(endpoint):
    if endpoint=='sales':
         return gm("Sales")
    elif endpoint=='research':
        return gm("Research & Development")
    elif endpoint=='hr':
        return gm("Human Resources")
    elif endpoint=="All":
        return gm("All")
    else:
        return "Bad endpoint", 400

def gm(department="All"):
    if department=="All":
        ig=px.bar(file["Department"],x="salary",template='plotly_dark')
    else:

        ig = px.bar(file[file['Department']==department]["salary"],width=500,height=500 ,template='plotly_dark')

    # Create a JSON representation of the graph
    graphJSON = json.dumps(ig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/callback1/<endpoint>')   
def callback1(endpoint):
    if endpoint=='sales':
         return gm1("Sales")
    elif endpoint=='research':
        return gm1("Research & Development")
    elif endpoint=='hr':
        return gm1("Human Resources")
    elif endpoint=="All":
        return gm1("All")
    else:
        return "Bad endpoint", 400

def gm1(department="All"):
    if department=="All":
        ig=px.area(file["Department"],x="salary",template='plotly_dark')
    else:

        ig = px.area(file[file['Department']==department]["WorkingYears"],width=700,height=500,template='plotly_dark' )

    # Create a JSON representation of the graph
    graphJSON1 = json.dumps(ig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON1

if __name__ == "__main__":
    app.run(debug=True)
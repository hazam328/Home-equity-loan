# Import essential libraries for web app

from flask import Flask, render_template, session, url_for, redirect, request
import numpy as np
import joblib
import json
import pandas as pd
import plotly
import plotly.express as px


# read csv file for plotting
df = pd.read_csv("hmeq.csv")





# A fucntion that returns predicted class defaulter or not defaulter

def return_prediction(model, feat):

    classes = np.array(["'NOT DEFAULTER'", "'DEFAULTER'"])

    class_ind = model.predict(feat)[0]

    return classes[class_ind]


# Loading a Trained model for webapp
model = joblib.load("home_equity_loan_predictor.joblib")



#assign a variable to flask to initialize routes
app = Flask(__name__)
app.config["SECRET_KEY"] = 'ViewRRs998eerRtky'





# main route where the user will see first page whenever user visits the webapp
@app.route("/", methods=["GET","POST"])
def main():


    return render_template("main.html")




# home route where user can enter credentials in input fields    
@app.route("/home", methods=["GET","POST"])
def index():
    

    return render_template("home.html")


# prediction route where user sees the output of entered inputs
@app.route("/prediction",methods=["POST"])
def predicttion():
    # looping through all the input fields and assigning it to a variable int_features
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]

    # calling a return_prediction fuction on our final inputs 
    results = return_prediction(model, final)
    
    
    return render_template('prediction.html', results=results)



# In this route there is little info about this webapp
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")



# This route is for visual
@app.route('/chart1')
def chart1():
    #plots and graphs
    fig = px.scatter(df, x='LOAN', y='DEBTINC',title="This Plot Shows Loan Against Debt-income-Ratio",color="LOAN"
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("chart1.html",graphJSON=graphJSON)


# This route is for visual
# @app.route('/chart2')
# def chart2():
#     #plots and graphs
#     fig = px.scatter(df, x='DEBTINC', y='YOJ',title=" This Plot Show Debt-income-Ratio Against Years Of Job",color="YOJ",
#     )
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#     return render_template("chart1.html",graphJSON=graphJSON)


# This route is for visual
@app.route('/chart3')
def chart3():
    #plots and graphs
    df1 = pd.crosstab(df.BAD, df.REASON)
    fig = px.bar(df1 ,title="Cross checking the 'Reason' column with 'Bad' target column")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("chart1.html",graphJSON=graphJSON)



# This route is for visual
@app.route('/chart4')
def chart4():
    #plots and graphs
    df_val1 = df.loc[df["BAD"]== 1].groupby('MORTDUE')['BAD'].agg('sum').sort_values(ascending=False)
    df_val1 = pd.DataFrame({'MORTDUE':df_val1.index, 'Number of Cases':df_val1.values})
    fig = px.histogram(df_val1 ,x='MORTDUE',y="Number of Cases",title="This Histogram shows that how many people were defaulted against Amount Due On Mortgage ")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("chart1.html",graphJSON=graphJSON)



# This route is for visual
@app.route('/chart5')
def chart5():
    #plots and graphs
    
    fig = px.scatter(df ,x='DEBTINC',y='MORTDUE',marginal_x="histogram", marginal_y="rug",title="Scatter Plot Marginals",color="DEBTINC")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("chart1.html",graphJSON=graphJSON)


# This route is for visual
@app.route('/chart6')
def chart6():
    #plots and graphs
    df_val1 = df.loc[df["BAD"]== 1].groupby('YOJ')['BAD'].agg('sum').sort_values(ascending=False)
    df_val1 = pd.DataFrame({'YOJ':df_val1.index, 'Number of Cases':df_val1.values})
    fig = px.scatter(df_val1,x='YOJ',y='Number of Cases',marginal_x="histogram",marginal_y="rug",title="This Dist plots shows that how many people were defaulted against Years Of Job",color="YOJ")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("chart1.html",graphJSON=graphJSON)


# This route is for visual
@app.route('/chart7')
def chart7():
    #plots and graphs
    df_val1 = df.loc[df["BAD"]== 1].groupby('DEBTINC')['BAD'].agg('sum').sort_values(ascending=False)
    df_val1 = pd.DataFrame({'DEBTINC':df_val1.index, 'Number of Cases':df_val1.values})
    fig = px.histogram(df_val1,x='DEBTINC',y='Number of Cases',title="This Histogram plot shows that how many people were defaulted against Debt-income-ratio")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("chart1.html",graphJSON=graphJSON)









if __name__ == '__main__':
    app.run()
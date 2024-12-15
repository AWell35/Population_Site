from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
global jsonData 
jsonData = {}
app = Flask(__name__)

def urlReq(keyName, url):
    response = requests.get(url)
    jsonFile = response.json()
    jsonData[keyName] = jsonFile 

@app.route("/")
def index():
    return render_template("homepage.html")



@app.route("/datasearch", methods=['GET', 'POST']) 
def datasearch():
    if not "flagData" in jsonData or not "populationData" in jsonData: #Stops the API data reloading after the first time
        urlReq("populationData", "https://countriesnow.space/api/v0.1/countries/population")
        urlReq("flagData", "https://countriesnow.space/api/v0.1/countries/flag/unicode")
    
    if "POST": #collects form data
        req = request.form
        if "countrySelect" in req:
            postRequest = {"iso3":req["countrySelect"]} 
            postResponse = requests.post("https://countriesnow.space/api/v0.1/countries/population", json = postRequest)
            jsonData["requestedData"] = postResponse.json()


        if "dateSelect" in req:
            searchYear = req["dateSelect"]
            for record in jsonData["requestedData"]["data"]["populationCounts"]:
                if record["year"] == int(searchYear):
                    jsonData["requestedDate"] = [searchYear, record["value"]]

    return render_template("dataSearch.html", data=jsonData).encode( "utf-8" )

@app.route("/dataVisual")
def datamap():
    if not "populationData" in jsonData:
        urlReq("populationData", "https://countriesnow.space/api/v0.1/countries/population")
    if not "pieChart" in jsonData: #Creates the prototype pie chart
        country = [] #pie chart labels
        population = [] #pie chart data
        flag = False
        
        for record in jsonData["populationData"]['data']: #checks for when Countries start in the dataset
            if  record['country'] == "Afghanistan":
                flag = True
            if flag:
                if record['populationCounts'][-1]['value'] > 80000000:
                    country.append(record['country'])
                    population.append(record['populationCounts'][-1]['value'])
        plt.pie(population, labels=country, rotatelabels=90, labeldistance=1.25, textprops= {"fontsize":5}, radius=0.75) #designs the pie chart
        plt.savefig("./.venv/static/pieChartExample.jpg") #saves the pie chart tp static to be called by the website
        jsonData["pieChart"] = True #prevents it from being remade every reload
 
    return render_template("dataVisual.html")

if __name__ == "__main__": 
    app.run() 
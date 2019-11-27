'''
Pre-Requisite : 
Generate  API Key for Zillow account by signing up at 
    https://www.zillow.com/howto/api/APIOverview.htm
Use your own API KEY in line 44 below
For example,
 api_key = 'YOUR API_KEY'
'''

from flask import Flask, request, redirect, render_template, session, url_for
import pandas as pd
import json
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults,GetUpdatedPropertyDetails
from uszipcode import SearchEngine
from joblib import dump, load
import os
import numpy as np
import platform

cwd = os.getcwd()
os.chdir(cwd)

##CA_model = load(cwd + '\\models\\CA.joblib')
##DC_model = load(cwd + '\\models\\DC.joblib')
##GA_model = load(cwd + '\\models\\GA.joblib')
##IL_model = load(cwd + '\\models\\IL.joblib')
##NY_model = load(cwd + '\\models\\NY.joblib')
##TX_model = load(cwd + '\\models\\TX.joblib')
##WA_model = load(cwd + '\\models\\WA.joblib')

if platform.system() in ('Darwin','Linux'):
    model = load(cwd + '/models/model5.joblib')
    
else:
    model = load(cwd + '\\models\\model5.joblib')

#model = load(cwd + '\\models\\model5.joblib')


##models = {'CA':CA_model,'DC':DC_model,'GA':GA_model,'IL':IL_model,'NY':NY_model,'TX':TX_model,'WA':WA_model}
state_mapping = {'CA':0,'DC':1,'GA':2,'IL':3,'NY':4,'TX':5,'WA':6}
hometype_mapping = {'Apartment':0,'Condominium':1,'Cooperative':2,'Duplex':3,'Miscellaneous':4,'Mobile':5,'MultiFamily2To4':6,'MultiFamily5Plus':7,\
                    "Quadruplex":8,"SingleFamily":9,"Townhouse":10,"Triplex":11,"Unknown":12,"VacantResidentialLand":13}
             

api_key = 'X1-ZWz17l7hzioj63_3pg0i'

app= Flask(__name__)


app.secret_key = b'blkjhbckjblkj*$'

state_names = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',\
               'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',\
               'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', \
               'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',\
               'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',\
               'NC': 'North Carolina', 'ND': 'North Dakota', 'MP': 'Northern Mariana Islands', 'OH': 'Ohio', 'OK': 'Oklahoma',\
               'OR': 'Oregon', 'PW': 'Palau', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island',\
               'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', \
               'VT': 'Vermont', 'VI': 'Virgin Islands', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}



@app.route('/', methods=['GET', 'POST'])
def mainpage():
    return render_template('index.html')


@app.route('/cities', methods=['GET', 'POST'])
def cities():
    street_address = request.args.get('street')
    zipcode = request.args.get('zip')
    bedrooms = float(request.args.get('bed'))
    bathrooms = float(request.args.get('bath'))
    home_size = float(request.args.get('size'))
    property_size = float(request.args.get('psize'))
    year_built = int(request.args.get('year'))
    hometype = request.args.get('hometype')
    taxyear = int(request.args.get('taxyear'))
    taxvalue = float(request.args.get('taxvalue'))
    
    citiesvalues = pd.read_csv('cities-lived.csv')   #.to_dict('records')
    citiesvalues['user_city'] = 'N'
    if street_address != '' and zipcode != '':
        search = SearchEngine(simple_zipcode=True)
        city = search.by_zipcode(int(zipcode)).city
        zillow_data = ZillowWrapper(api_key)
        deep_search_response = zillow_data.get_deep_search_results(street_address, zipcode)
        result = GetDeepSearchResults(deep_search_response)
        errors = []
        inputvals = {}
        if result.bathrooms is not None and bathrooms == 0:
            bathrooms = float(result.bathrooms)
        elif result.bathrooms is not None and bathrooms != 0:
            bla=0 #do nothing
        elif result.bathrooms is None and bathrooms == 0:
            errors.append(bathrooms)
        inputvals["bathrooms"] = bathrooms
        #############################################
        if result.bedrooms  is not None and bedrooms == 0:
            bedrooms = float(result.bedrooms)
        elif result.bedrooms  is not None and bedrooms != 0:
            bla=0 #do nothing
        elif result.bedrooms is None and bedrooms == 0:
            errors.append(bedrooms)
        inputvals["bedrooms"] = bedrooms
        #############################################
        if result.home_size is not None and home_size == 0:
            home_size = float(result.home_size)
        elif result.home_size is not None and home_size != 0:
            bla=0 #do nothing
        elif result.home_size is None and home_size == 0:
            errors.append(home_size)
        inputvals["home_size"] = home_size
        #############################################
        if result.property_size is not None and property_size == 0:
            property_size = float(result.property_size)
        elif result.property_size is not None and property_size != 0:
            bla=0 #do nothing
        elif result.property_size is None and property_size == 0:
            errors.append(property_size)
        inputvals["property_size"] = property_size
        #############################################
        if result.year_built is not None and year_built == 0:
            year_built = int(result.year_built)
        elif result.year_built is not None and year_built != 0:
            bla=0 #do nothing
        elif result.year_built is None and year_built == 0:
            errors.append(year_built)
        inputvals["year_built"] = year_built
        #############################################
        if result.tax_year is not None and taxyear == 0:
            taxyear = int(result.tax_year)
        elif result.tax_year is not None and taxyear != 0:
            bla=0 #do nothing
        elif result.tax_year is None and taxyear == 0:
            errors.append(taxyear)
        inputvals["taxyear"] = taxyear
        #############################################
        if result.tax_value is not None and taxvalue == 0:
            taxvalue = float(result.tax_value)
        elif result.tax_value is not None and taxvalue != 0:
            bla=0 #do nothing
        elif result.tax_value is None and taxvalue == 0:
            errors.append(taxvalue)
        inputvals["taxvalue"] = taxvalue
        #############################################
        if result.home_type is not None and hometype == "Unknown":
            hometype = result.home_type
        elif result.home_type is not None and hometype != "Unknown":
            bla=0 #do nothing
        elif result.home_type is None and hometype == "Unknown":
            errors.append(hometype)
        inputvals["hometype"] = hometype
        #############################################
        citiesvalues['bedrooms'] = bedrooms
        citiesvalues['bathrooms'] = bathrooms
        citiesvalues['tax_year'] = taxyear
        citiesvalues['tax_value'] = taxvalue
        citiesvalues['property_size'] = property_size
        citiesvalues['home_size'] = home_size
        citiesvalues['location'] = citiesvalues['state'].apply(lambda x: state_mapping[x])
        citiesvalues['home_type'] = hometype_mapping[hometype]
        citiesvalues['age'] = 2019-year_built
        citiesvalues['price'] = model.predict(citiesvalues[['bedrooms','bathrooms','tax_year','tax_value','property_size','home_size','location','home_type','age']])
        print(citiesvalues['price'])						
        citiesvalues['price'] = citiesvalues['price'].apply(lambda x: round(x,2))
        citiesvalues = citiesvalues.drop(columns = ['bedrooms','bathrooms','tax_year','tax_value','property_size','home_size','location','home_type','age'])
 
##        for i, r in citiesvalues.iterrows():
##            citiesvalues.at[i,'price'] = model.predict(np.array([[bedrooms,bathrooms,taxyear,taxvalue,property_size,home_size,state_mapping[r['state']],hometype_mapping[hometype],2019-year_built]]))[0]
        citiesvalues = citiesvalues.to_dict('records')
        if result.zestimate_amount is None and result.tax_value is None and result.last_sold_price is not None:
            result.zestimate_amount = result.last_sold_price #default for the circle to show
        elif result.zestimate_amount is None and result.tax_value is None and result.last_sold_price is None:
            result.zestimate_amount = 100000

        print({'price':result.zestimate_amount, 'place':city, 'lat':result.latitude, 'lon':result.longitude,'user_city':'Y'})
        citiesvalues.append({'price':result.zestimate_amount, 'place':city, 'lat':result.latitude, 'lon':result.longitude,'user_city':'Y'})
        citiesvalues.append({"errors":errors,"input":inputvals})
    else:
        citiesvalues = citiesvalues.to_dict('records')
    print(citiesvalues)	
        
    return json.dumps(citiesvalues)

@app.route('/states', methods=['GET', 'POST'])
def states():
    zipcode = request.args.get('zip')    
    statesvalues = pd.read_csv('stateslived.csv').to_dict('records')
    if zipcode != '':
        search = SearchEngine(simple_zipcode=True)
        state = state_names[search.by_zipcode(int(zipcode)).state]
        statesvalues.append({'state':state,'visited':1})
    return json.dumps(statesvalues)      

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True)

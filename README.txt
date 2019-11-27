DESCRIPTION
-----------
REMI is Real-Estate Market Insights application to predict home prices of a similar 
home as your's in top big cities in USA.
This application compises of :
1.  Datasets retrieved from Zillow about top citi's real estate pricing and features
2.  Trained models to predict housing price based on above dataset
3.  User-Interface where User can either put his home address OR input features of a home
    in any zip-code of the country 
    This interface will then 
    a.  retrieve the features of realestate using Zillow API
    b.  use trained model to predict the house value in top cities of similar home
    c.  provide house prices through visualization 

INSTALLATION
------------
Few software libraries need to be installed before this app can be used 
Pre-Requisites 
	flask
	pandas
	pyzillow
	uszipcode
	joblib
	numpy
Please run commands below to install all pre-requisites :
	pip install flask
	pip install pandas
	pip install pyzillow
	pip install uszipcode
	pip install joblib
	pip install numpy
	
Application Install	
This application can be installed using attached ZIP file <remi_app.zip>  ## TODO
1.  Download the zipfile to the directory of your choice on your pc ( or mac) 
2.  unzip the contents of the directory
3.  run command below 
    python <install directory location>/app/run_remi.py
4.  Observe the message displayed on console to find out link and port
    example, if you notice below line ,  
           * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 
    The application uses 5000 as default port. Use link below using Chrome or Firefox
    browser to use the application 
    http://127.0.0.1:5000

Video showing installation
https://www.youtube.com/watch?v=OfmrBnAEdnI
   
 

EXECUTION
---------
Once application is launched and accessed through browser,
1.    Red Circles on large metro areas shows average house price in that market

2-A.  Enter any address like your current home address for which you want to compare, using
      Street and Zipcode fields on top left
      OR
2-B.  Enter all the input features using other boxes bedrooms,bathrooms,homesize,
      propertysize,yearbuilt,Taxyear,Taxvalue and HomeType.
       
3.    Click "Compare Price" button at the bottom 
      The visualization renders predicted prices based on above input in all markets



DEMO VIDEO
----------
Link
 
 

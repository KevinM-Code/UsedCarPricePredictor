# Used Car Price Predictor

Application description: 
> This is an application that gives the user options to select the make, model and other options to a car to find the approximate market price of that car based on a large number of different used car price listings from web scraping of Craigslist.

May not be as good as Kelly Blue Book but it was fun to try:blush:

##### Directions to run the web application locally on a Windows 10 machine:

1. `git clone https://github.com/KevinM-Code/UsedCarPricePredictor.git`

2. Install Anaconda from [here](https://www.anaconda.com/products/individual-d) to run the web application locally *and* to view the Jupyter Notebook files in the `JupyterNotebook-DataCleaningandAnalysis` folder.    
   * **When installing _Anaconda_ make sure you check** 
      - [x] `Add Anaconda3 to my PATH environment variable`.
   * To **ONLY** run the application locally install python from [here](https://www.python.org/downloads/) and continue.
      * There are **preview HTML files** of the Jupyter Notebook files in the `JupyterNotebook-DataCleaningandAnalysis` folder.<br/><br/>

      
3. On the command line run `cd UsedCarPricePredictor` into the project root directory.<br/><br/>
4. In the root directory of the project folder, also on the command line run the following:
   1. `python -m venv env`
   2. `.\env\Scripts\activate`
   3. `pip install -r requirements.txt`
   4. `python manage.py runserver`<br/>   
   http://127.0.0.1:8000/   

##### Directions to view Jupyter Notebook files on a Windows 10 machine once _Anaconda_ is installed:

1. On the command line from the project root `cd JupyterNotebook-DataCleaningandAnalysis` inside the folder and run `jupyter notebook` a browser should open with the folder contents.
 

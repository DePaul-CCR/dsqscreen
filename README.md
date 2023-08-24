### Dev Env Setup
->Need Python 3 installed w/ pip and virtualenv for dev env ~~and mysql~~  
[Install Python 3 w/ pip](https://www.python.org/downloads/)  
MacOS:
~~`brew install mysql`~~  
`pip install virtualenv`

->Clone this repo  
`gh repo clone DePaul-CCR/dsqscreen`

->CD into repo

->Create an environment for packages  
`python3 -m venv ./env`

->Activate the environment and install packages
`source ./env/bin/activate`  
`pip install -r requirements.txt`

->Add environment to path if needed  
`export PYTHONPATH=$PYTHONPATH:~/Github/Depaul_CCR/Screener/env/lib/python3.11/site-packages`

~~-> Run database migrations if exist~~

-> To start dev server  
`python3 main.py dev`

### Dev pipeline:  
`featurebranch` -> PR `main` -> PR `production` -> Create release on Github -> autodeploys to render.com 

### Production:
-> To start production server  
`gunicorn main:app prod`

###NB
If you change the routes please update the route-order "page_flow" tuple in 'utils/back_function.py' so the back button works correctly 
+ the dsqitems_to_routes.txt file, which shows the DSQ item var names mapped to routes, should be updated also. 

To make changes to question pages there is one partial for all the F/S questions and then the single-question items are less templated so need to be modified directly (dsq/viral.html and short_form/reduction.html)
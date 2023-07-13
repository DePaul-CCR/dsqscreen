->Need Python3 installed w/ pip and also mysql  
MacOS:  
`> brew install mysql`
`> pip install virtualenv`

->Clone repo

->CD into repo

->Create a python3 environment for packages  
`> python3 -m venv ./env`

->Activate the environment  
`> source ./env/bin/activate`  
`pip install -r requirements.txt`

->Add environment to path if needed  
`> export PYTHONPATH=$PYTHONPATH:~/Github/Depaul_CCR/Screener/env/lib/python3.11/site-packages`

-> Run database migrations if exist

-> To start dev server  
`> python3 main.py dev`

-> To start production server  
`> gunicorn main:app` prod

Dev pipeline: `featurebranch` -> PR `main` -> PR `production` -> autodeploys to render.com
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
`featurebranch` -> PR `main` -> PR `production` -> autodeploys to render.com

### Production:
-> To start production server  
`gunicorn main:app prod`
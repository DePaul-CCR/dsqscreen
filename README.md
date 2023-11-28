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

###N.B.
-If you change the routes please update the route-order "page_flow" tuple in 'utils/back_function.py' so the back button works correctly 
+ the docs/dsqitems_and_routes_map.txt file, which shows the DSQ item var names mapped to routes, should be updated also. 
+ dsq_columns in utils/export_columns_util.py are order-specific so will also be misaligned if the order of questions changes. (TODO: make the data export order-agnostic)

-If you change which items / questions are used, you also need to update the dsq_columns in utils/export_columns_util.py
+Also, you will need to update the columns in the export sheet: depaulccrdev@gmail.com's "DSQScreen Output"
+Manually, you can compare the data frame which holds the responses to the header row in the Google sheet via
```
#Debug breakpoint on ~line 22 in utils/export_columns_util.py
import nump as np
gs_arr = np.array(#paste gsheet column headers in here formatted as a list ['x', 'y', 'z'...]
)
np.array(df.columns.to_list()) == gs_arr
```

-To make changes to question pages there is one partial for all the F/S questions and then the single-question items are less templated so need to be modified directly (dsq/viral.html and short_form/reduction.html)
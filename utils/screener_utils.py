from flask import render_template, session
import plotly.graph_objects as go
import pandas as pd
import json
import plotly.utils

def screener_diagnose():
    # we *25 to scale 4pt scale to 100 pt scale
    fatiguescore = domain_score('fatiguescore')
    pemscore = domain_score('pemscore')
    sleepscore = domain_score('sleepscore')
    cogscore = domain_score('cogscore')

    df = pd.read_csv('MECFS COMPOSITE DATA.csv')
    responses = [fatiguescore, pemscore, sleepscore, cogscore]
    iomfatiguecheck = "No"
    iompemcheck = "No"
    iomsleepcheck = "No"
    iomcogcheck = "No"
    dx_met = False

    if session['fatiguescoref'] >= 2 and session['fatiguescores'] >= 2:
        iomfatiguecheck = "Yes"
    if session['minexf'] >= 2 and session['minexs'] >= 2:
        iompemcheck = "Yes"
    if session['sleepf'] >= 2 and session['sleeps'] >= 2:
        iomsleepcheck = "Yes"
    if session['rememberf'] >= 2 and session['remembers'] >= 2:
        iomcogcheck = "Yes"

    screen_message = 'Your responses to the screener questions are scored below. <br> Scores range from 0 to 100, with higher scores indicate more frequent and severe problems.'
    if iomfatiguecheck == "Yes" or iompemcheck == "Yes" or iomsleepcheck == "Yes" or iomcogcheck == "Yes":
        dx_met = True

    composite_scores = responses
    categories = ['Fatigue', 'Post-exertional malaise', 'Sleep problems',
                  'Cognitive problems']

    select_list = ['fatigue13c', (session['pemname'] + 'c'),
                   (session['cogname'] + 'c'), (session['sleepname'] + 'c'), 'dx']
    df = df[select_list]
    colors = ['#56A8A0' for score in composite_scores]
    
    # composite f/s score graph
    fig = go.Figure(
        data=[
            go.Bar(y=composite_scores, x=categories, name="Your scores", marker=dict(color=colors))],
        layout=go.Layout(
            title=go.layout.Title(text='Your Summary Score', x=0.5),
            showlegend=True, 
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            autosize=True
        )
    )
    fig.update_layout(
        yaxis_title='Combined Frequency and Severity Scores',
        xaxis_title='Symptom Domains'
    )
    fig.update_yaxes(range=[0, 100], dtick=25)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("results/graph.html",
                           graphJSON = graphJSON, 
                           screen_message = screen_message,
                           dx_met = dx_met)

def domain_score(session_var_string):
    return 1 if session[session_var_string] == 0 else session[session_var_string] * 25
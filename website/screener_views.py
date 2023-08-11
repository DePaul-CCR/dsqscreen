from flask import Blueprint, render_template, session, request, redirect, url_for
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.utils
# used for /scores which is currently not in use - PC 7/21/23
# import numpy as np

screener_views = Blueprint('screener_views', __name__)

message = "Please enter a response for both frequency and severity before continuing"


@screener_views.route('/', methods=['post', 'get'])
def home():
    session["pagenum"] = 0
    survey = 'classic'
    if request.method == "POST":
        session["pagenum"] += 1
        return redirect(url_for("screener_views.page1"))
    return render_template("home.html", session=session)


# First symptom question
@screener_views.route('/fatigue', methods=['post', 'get'])
def page1():

    session['pagenum'] = 1
    if request.method == "POST":
        selected_radio = request.form.get('fatigue')
        selected_severity = request.form.get('severity')
        fatiguescoref = request.form.get("fatigue")
        fatiguescores = request.form.get("severity")
        if fatiguescores is not None and fatiguescoref is not None:
            session['fatiguescoref'] = int(fatiguescoref)
            session['fatiguescores'] = int(fatiguescores)
            session['fatiguescore'] = (session['fatiguescoref'] + session['fatiguescores']) / 2
            session['pagenum'] += 1

            return redirect(url_for("screener_views.page2"))
        else:
            return render_template("screener/page1.html", pagenum=session['pagenum'], message=message,
                                   selected_radio=selected_radio, selected_severity=selected_severity)
    return render_template("screener/page1.html", pagenum=session['pagenum'], message='')


@screener_views.route('/minimum', methods=["post", "get"])
def page2():
    global pemname
    selected_f = request.form.get('minex')
    selected_s = request.form.get('minex_s')
    if request.method == "POST":
        minexf = request.form.get("minex")
        minexs = request.form.get("minex_s")
        if minexs is not None and minexf is not None:
            session["minexf"] = int(minexf)
            session["minexs"] = int(minexs)
            session["pemscore"] = (int(minexf) + int(minexs)) / 2
            session["pemname"] = "minimum17"
            session['pagenum'] += 1

            return redirect(url_for("screener_views.page3"))

        else:
            return render_template("screener/page2.html", pagenum=session['pagenum'], message=message,
                                   selected_s=selected_s, selected_f=selected_f)
    return render_template("screener/page2.html", pagenum=session['pagenum'], message='')


@screener_views.route('/unrefreshed', methods=['post', 'get'])
def page3():
    global sleepname

    if request.method == "POST":
        sleepf = request.form.get("sleepf")
        sleeps = request.form.get("sleeps")
        if sleeps is not None and sleepf is not None:
            session["sleepf"] = int(sleepf)
            session["sleeps"] = int(sleeps)
            session['pagenum'] += 1

            if int(session["sleepf"]) >= 0 and int(session["sleeps"]) >= 0:
                session['sleepscoref'] = int(sleepf)
                session['sleepscores'] = int(sleeps)
                session['sleepscore'] = (int(session['sleepf']) + int(session['sleeps'])) / 2
                session["sleepname"] = 'unrefreshed19'

                return redirect(url_for("screener_views.page4"))

        else:
            return render_template("screener/page3.html", pagenum=session['pagenum'], message=message,
                                   sleepf=sleepf, sleeps=sleeps)
    return render_template("screener/page3.html", pagenum=session['pagenum'], message='')


@screener_views.route('/remember', methods=['post', 'get'])
def page4():
    global cogname

    if request.method == "POST":
        rememberf = request.form.get("rememberf")
        remembers = request.form.get("remembers")
        if remembers is not None and rememberf is not None:
            session["rememberf"] = int(rememberf)
            session["remembers"] = int(remembers)
            session['pagenum'] += 1

            session['cogscoref'] = int(rememberf)
            session['cogscores'] = int(remembers)
            session["cogname"] = 'remember36'
            session['cogscore'] = (int(session['rememberf']) + int(session['remembers'])) / 2

            return redirect(url_for('screener_views.graph'))

        else:
            return render_template("screener/page4.html", pagenum=session['pagenum'], message=message,
                                   rememberf=rememberf, remembers=remembers)
    return render_template("screener/page4.html", pagenum=session['pagenum'], message='')


@screener_views.route('/screener_dx')
def graph():
    # we *25 to scale 4pt scale to 100 pt scale
    fatiguescore = session['fatiguescore'] * 25
    pemscore = session['pemscore'] * 25
    sleepscore = session['sleepscore'] * 25
    cogscore = session['cogscore'] * 25

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

    if iomfatiguecheck == "Yes" or iompemcheck == "Yes" or iomsleepcheck == "Yes" or iomcogcheck == "Yes":
        screen_message = 'Based on your responses there is a chance you might have MECFS. <br> Please continue to the next section for a more accurate assessment.'
        dx_met = True
    else:
        screen_message = "Based on your responses it does not appear you have MECFS."

    composite_scores = responses
    categories = ['Fatigue', 'Post-exertional malaise', 'Sleep problems',
                  'Cognitive problems']

    select_list = ['fatigue13c', (session['pemname'] + 'c'),
                   (session['cogname'] + 'c'), (session['sleepname'] + 'c'), 'dx']
    df = df[select_list]
    colors = ['#89889E' if score < 50 else '#56A8A0' for score in composite_scores]
    
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

# not currently in use since we disabled users - PC 7/21/23
# @screener_views.route('/scores')
# def scores():
#     name = session['user']
#     user_id = session['user_id']
#     graphJSON = None
#     print(['user id', user_id])
#     if session['checkbox'] == 'data':
#         cursor = mysql.connection.cursor()
#         cursor.execute("""
#             SELECT fatigue13f, fatigue13s, minimum17f, minimum17s, unrefreshed19f, 
#             unrefreshed19s, remember36f, remember36s
#             FROM screen
#             JOIN login ON screen.login_id = login.id
#             WHERE login.id = %s
#         """, (user_id,))
#         results = cursor.fetchall()
#         print('results', results, type(results))
#         array = np.array(results)
#         print(array)
#         if len(array) > 0:

#             fatigue = np.mean([array[:, 0], array[:, 1]], axis=0)
#             pem = np.mean([array[:, 2], array[:, 3]], axis=0)
#             sleep = np.mean([array[:, 4], array[:, 5]], axis=0)
#             cog = np.mean([array[:, 6], array[:, 7]], axis=0)
#             plot_lines = [fatigue, pem, sleep, cog]
#             line_names = ["Fatigue", "PEM", "Sleep", "Cognitive Problems"]
#             print('array', fatigue)
#             timestamps = np.arange(len(array[:, 0]))

#             length = len(array)
#             max_width = 16
#             fig = go.Figure()

#             for i in range(len(plot_lines)):
#                 fig.add_trace(go.Scatter(x=timestamps, y=plot_lines[i], name=line_names[i],
#                                          line=dict(width=max_width - (i * 4))))
#                 fig.update_traces(mode='lines')

#             fig.update_layout(title='Your domain scores over time', xaxis_title='Times you took the screener',
#                               yaxis_title='Domain scores')
#             fig.update_layout(xaxis=dict(
#                 tickmode='array',
#                 tickvals=timestamps,
#                 ticktext=[(int(val) + 1) for val in timestamps]
#             ))
#             fig.update_layout(yaxis_range=[0, 4.5])

#             graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#             user_message = f"You have data available from {length} sessions. A graph of your responses is shown below."

#         else:
#             user_message = "You do not have any scores yet. Your saved responses will be available here once you take " \
#                            "the screener."
#         if name == "guest":
#             user_message = "You are using the screener as a guest, and do not have data stored. " \
#                            " To track your data over time, please login."
#     else:
#         if session['checkbox'] != "data":
#             user_message = "You logged in, but chose not to have your data stored, " \
#                            " so no information is available to report."
#         else:
#             user_message = "Test"

#     return render_template('scores.html', name=name, user_message=user_message, graphJSON=graphJSON)

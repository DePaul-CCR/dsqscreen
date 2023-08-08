import numpy as np
from flask import render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
import utils.dsq_utils as dsq_utils
# commented out unused imports, can probably delete soon -- PC 7/31/23
# import plotly.utils
# import plotly.graph_objects as go
# import json
# from flask_session import Session
# from wtforms import RadioField, SubmitField
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.offline as pyo
# import base64
# from io import BytesIO
# from wtforms.validators import InputRequired
# import re
# from os import path

# imports the flask app we configured in the websites folder:
from website import create_app

app = create_app()

symptom = ["Fatigue", "Minimum exercise", "Sleep", "Remember"]
pagenum = 0
end = False
pemdomain = 0
sleepdomain = 0
cogdomain = 0
survey = 'classic'
message = "Please enter a response for both frequency and severity before continuing"
composite = 0
pemname = str
sleepname = str
cogname = str

@app.route('/viral', methods=['post', 'get'])
def viral():
    form = FlaskForm()
    msg_viral = "Please select one of the options before continuing"
    if request.method == 'POST':
        viral = request.form.get('viral')
        if viral is not None:
            session['viral'] = viral
            session['pagenum'] += 1
            return redirect(url_for('expem3'))
        else:
            return render_template("dsq/viral.html", message=msg_viral, pagenum=session['pagenum'])
    return render_template('dsq/viral.html', message='', pagenum=session['pagenum'])

@app.route('/heavy', methods=['post', 'get'])
def expem3():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        heavyf = request.form.get("heavyf")
        heavys = request.form.get("heavys")

        if heavyf is not None and heavys is not None:
            session["heavyf"] = heavyf
            session["heavys"] = heavys
            session['pagenum'] += 1
            if int(session["heavyf"]) >= 0 and int(session["heavys"]) >= 0:
                session['pemscoref'] = session['heavyf']
                session['pemscores'] = session['heavys']
                session['pemscore'] = (int(session['heavyf']) + int(session['heavys'])) / 2
                pemname = 'heavy14'
                return redirect(url_for("expem4"))
        else:
            return render_template("dsq/expem3.html", pagenum=session['pagenum'], message=message)
    return render_template("dsq/expem3.html", pagenum=session['pagenum'], message='')

@app.route('/mentally', methods=['post', 'get'])
def expem4():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        mentalf = request.form.get("mentalf")
        mentals = request.form.get("mentals")
        if mentalf is not None and mentals is not None:
            session["mentalf"] = mentalf
            session["mentals"] = mentals
            session['pagenum'] += 1
            if int(session["mentalf"]) >= 0 and int(session["mentals"]) >= 0:
                session['pemscoref'] = int(mentalf)
                session['pemscores'] = int(mentals)
                session['pemscore'] = (int(session['mentalf']) + int(session['mentals'])) / 2
                pemname = 'mental16'
                return redirect(url_for("expem2"))
        else:
            return render_template("dsq/expem4.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/expem4.html", message='', pagenum=session['pagenum'])

@app.route('/drained', methods=['post', 'get'])
def expem2():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        drainedf = request.form.get("drainedf")
        draineds = request.form.get("draineds")
        if drainedf is not None and draineds is not None:
            session["drainedf"] = drainedf
            session["draineds"] = draineds
            session['pagenum'] += 1
            if int(session["drainedf"]) >= 0 and int(session["draineds"]) >= 0:
                session['pemscoref'] = session['drainedf']
                session['pemscores'] = session['draineds']
                session['pemscore'] = (int(session['drainedf']) + int(session['draineds'])) / 2
                pemname = 'drained18'
                return redirect(url_for("weakness"))
        else:
            return render_template("dsq/expem2.html", pagenum=session['pagenum'], message=message)
    return render_template("dsq/expem2.html", pagenum=session['pagenum'], message='')

@app.route('/weakness', methods=['post', 'get'])
def weakness():
    form = FlaskForm()
    global pemname
    if request.method == "POST":
        weakf = request.form.get("weakf")
        weaks = request.form.get("weaks")
        if weakf is not None and weaks is not None:
            session["weakf"] = weakf
            session["weaks"] = weaks
            session['pagenum'] += 1
            session['pemscoref'] = int(weakf)
            session['pemscores'] = int(weaks)
            pemname = 'weakness33'
            session['pemscore'] = (int(session['weakf']) + int(session['weaks'])) / 2
            return redirect(url_for("exsleep2"))
        else:
            return render_template("dsq/weakness33.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/weakness33.html", message='', pagenum=session['pagenum'])

@app.route('/nap', methods=['post', 'get'])
def exsleep2():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        napf = request.form.get("napf")
        naps = request.form.get("naps")
        if napf is not None and naps is not None:
            session["napf"] = napf
            session["naps"] = naps
            session['pagenum'] += 1

            session['sleepscoref'] = int(napf)
            session['sleepscores'] = int(naps)
            session['sleepscore'] = (int(session['napf']) + int(session['naps'])) / 2
            sleepname = 'nap20'
            return redirect(url_for("exsleep3"))
        else:
            return render_template("dsq/exsleep2.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/exsleep2.html", message='', pagenum=session['pagenum'])

@app.route('/falling', methods=['post', 'get'])
def exsleep3():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        fallf = request.form.get("fallf")
        falls = request.form.get("falls")
        if fallf is not None and falls is not None:
            session["fallf"] = fallf
            session["falls"] = falls
            session['pagenum'] += 1
            if int(session["fallf"]) >= 0 and int(session["falls"]) >= 0:
                session['sleepscoref'] = int(fallf)
                session['sleepscores'] = int(falls)
                session['sleepscore'] = (int(session['fallf']) + int(session['falls'])) / 2
                sleepname = 'falling21'
                return redirect(url_for("exsleep1"))
        else:
            return render_template("dsq/exsleep3.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/exsleep3.html", message='', pagenum=session['pagenum'])

@app.route('/staying', methods=['post', 'get'])
def exsleep1():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        stayf = request.form.get("stayf")
        stays = request.form.get("stays")
        if stayf is not None and stays is not None:
            session["stayf"] = stayf
            session["stays"] = stays
            session['pagenum'] += 1
            if int(session["stayf"]) >= 0 and int(session["stays"]) >= 0:
                session['sleepscoref'] = int(stayf)
                session['sleepscores'] = int(stays)
                session['sleepscore'] = (int(session['stayf']) + int(session['stays'])) / 2
                sleepname = 'staying22'
                return redirect(url_for("early"))
        else:
            return render_template("dsq/exsleep1.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/exsleep1.html", message='', pagenum=session['pagenum'])

@app.route('/early', methods=['post', 'get'])
def early():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        earlyf = request.form.get("earlyf")
        earlys = request.form.get("earlys")
        if earlyf is not None and earlys is not None:
            session["earlyf"] = earlyf
            session["earlys"] = earlys
            session['pagenum'] += 1
            if int(session["earlyf"]) >= 0 and int(session["earlys"]) >= 0:
                session['sleepscoref'] = int(earlyf)
                session['sleepscores'] = int(earlys)
                session['sleepscore'] = (int(session['earlyf']) + int(session['earlys'])) / 2
                sleepname = 'falling21'
                return redirect(url_for("exsleep4"))
        else:
            return render_template("dsq/early23.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/early23.html", message='', pagenum=session['pagenum'])

@app.route('/allday', methods=['post', 'get'])
def exsleep4():
    form = FlaskForm()
    global sleepname
    if request.method == "POST":
        alldayf = request.form.get("alldayf")
        alldays = request.form.get("alldays")
        if alldayf is not None and alldays is not None:
            session["alldayf"] = alldayf
            session["alldays"] = alldays
            session['pagenum'] += 1
            if int(session["alldayf"]) >= 0 and int(session["alldays"]) >= 0:
                session['sleepscoref'] = int(alldayf)
                session['sleepscores'] = int(alldays)
                session['sleepscore'] = (int(session['alldayf']) + int(session['alldays'])) / 2
                sleepname = 'allday24'
                return redirect(url_for("jointpain"))
            else:
                sleepname = 'allday24'
                session['sleepscoref'] = int(alldayf)
                session['sleepscores'] = int(alldays)
                session['sleepscore'] = (int(session['jointpain']) + int(session['alldays'])) / 2
                return redirect(url_for("jointpain"))
        else:
            return render_template("dsq/exsleep4.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/exsleep4.html", message='', pagenum=session['pagenum'])

@app.route('/jointpain', methods=['post', 'get'])
def jointpain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        jointpainf = request.form.get("jointpainf")
        jointpains = request.form.get("jointpains")
        if jointpainf is not None and jointpains is not None:
            session["jointpainf"] = jointpainf
            session["jointpains"] = jointpains
            session['pagenum'] += 1
            return redirect(url_for("eyepain"))
        else:
            return render_template("dsq/jointpain26.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/jointpain26.html", message='', pagenum=session['pagenum'])

@app.route('/eyepain', methods=['post', 'get'])
def eyepain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        eyepainf = request.form.get("eyepainf")
        eyepains = request.form.get("eyepains")
        if eyepainf is not None and eyepains is not None:
            session["eyepainf"] = eyepainf
            session["eyepains"] = eyepains
            session['pagenum'] += 1
            return redirect(url_for("chestpain"))
        else:
            return render_template("dsq/eyepain27.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/eyepain27.html", message='', pagenum=session['pagenum'])

@app.route('/chestpain', methods=['post', 'get'])
def chestpain():
    global end
    form = FlaskForm()
    if request.method == "POST":
        chestpainf = request.form.get("chestpainf")
        chestpains = request.form.get("chestpains")
        if chestpainf is not None and chestpains is not None:
            session["chestpainf"] = chestpainf
            session["chestpains"] = chestpains
            session['pagenum'] += 1
            return redirect(url_for("stomach"))
        else:
            return render_template("dsq/chestpain28.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/chestpain28.html", message='', pagenum=session['pagenum'])

@app.route('/stomach', methods=['post', 'get'])
def stomach():
    global end
    form = FlaskForm()
    if request.method == "POST":
        stomachf = request.form.get("stomachf")
        stomachs = request.form.get("stomachs")
        if stomachf is not None and stomachs is not None:
            session["stomachf"] = stomachf
            session["stomachs"] = stomachs
            session['pagenum'] += 1
            return redirect(url_for("headaches"))
        else:
            return render_template("dsq/stomach30.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/stomach30.html", message='', pagenum=session['pagenum'])

@app.route('/headaches', methods=['post', 'get'])
def headaches():
    global end
    form = FlaskForm()
    if request.method == "POST":
        headachesf = request.form.get("headachesf")
        headachess = request.form.get("headachess")
        if headachesf is not None and headachess is not None:
            session["headachesf"] = headachesf
            session["headachess"] = headachess
            session['pagenum'] += 1
            return redirect(url_for("twitches"))
        else:
            return render_template("dsq/headaches31.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/headaches31.html", message='', pagenum=session['pagenum'])

@app.route('/twitches', methods=['post', 'get'])
def twitches():
    global end
    form = FlaskForm()
    if request.method == "POST":
        twitchesf = request.form.get("twitchesf")
        twitchess = request.form.get("twitchess")
        if twitchesf is not None and twitchess is not None:
            session["twitchesf"] = twitchesf
            session["twitchess"] = twitchess
            session['pagenum'] += 1
            return redirect(url_for("noise"))
        else:
            return render_template("dsq/twitches32.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/twitches32.html", message='', pagenum=session['pagenum'])

@app.route('/noise', methods=['post', 'get'])
def noise():
    global end
    form = FlaskForm()
    if request.method == "POST":
        noisef = request.form.get("noisef")
        noises = request.form.get("noises")
        if noisef is not None and noises is not None:
            session["noisef"] = noisef
            session["noises"] = noises
            session['pagenum'] += 1
            return redirect(url_for("lights"))
        else:
            return render_template("dsq/noise34.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/noise34.html", message='', pagenum=session['pagenum'])


@app.route('/lights', methods=['post', 'get'])
def lights():
    global end
    form = FlaskForm()
    if request.method == "POST":
        lightsf = request.form.get("lightsf")
        lightss = request.form.get("lightss")
        if lightsf is not None and lightss is not None:
            session["lightsf"] = lightsf
            session["lightss"] = lightss
            session['pagenum'] += 1
            return redirect(url_for("excog2"))
        else:
            return render_template("dsq/lights35.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/lights35.html", message='', pagenum=session['pagenum'])

@app.route('/word', methods=['post', 'get'])
def excog2():
    form = FlaskForm()
    global cogname
    global end
    if request.method == "POST":
        wordf = request.form.get("wordf")
        words = request.form.get("words")
        if words is not None and wordf is not None:
            session["wordf"] = wordf
            session["words"] = words
            session['pagenum'] += 1
            if int(session["wordf"]) >= 0 and int(session["words"]) >= 0:
                session['cogscoref'] = int(wordf)
                session['cogscores'] = int(words)
                session['cogscore'] = (int(session['wordf']) + int(session['words'])) / 2
                return redirect(url_for("understand"))
        else:
            return render_template("dsq/excog2.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/excog2.html", message='', pagenum=session['pagenum'])

@app.route('/understand', methods=['post', 'get'])
def understand():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        understandf = request.form.get("understandf")
        understands = request.form.get("understands")
        if understandf is not None and understands is not None:
            session["understandf"] = understandf
            session["understands"] = understands
            session['pagenum'] += 1
            if int(session["understandf"]) >= 0 and int(session["understands"]) >= 0:
                session['cogscoref'] = int(understandf)
                session['cogscores'] = int(understands)
                session['cogscore'] = (int(session['understandf']) + int(session['understands'])) / 2
                # end = True
                cogname = 'understand39'
                return redirect(url_for("excog3"))
        else:
            return render_template("dsq/understand39.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/understand39.html", message='', pagenum=session['pagenum'])

@app.route('/focus', methods=['post', 'get'])
def excog3():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        focusf = request.form.get("focusf")
        focuss = request.form.get("focuss")
        if focuss is not None and focusf is not None:
            session["focusf"] = focusf
            session["focuss"] = focuss
            session['pagenum'] += 1
            if int(session["focusf"]) >= 0 and int(session["focuss"]) >= 0:
                session['cogscoref'] = int(focusf)
                session['cogscores'] = int(focuss)
                session['cogscore'] = (int(session['focusf']) + int(session['focuss'])) / 2
                # end = True
                cogname = 'focus40'
                return redirect(url_for('vision'))
        else:
            return render_template("dsq/excog3.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/excog3.html", message='', pagenum=session['pagenum'])

@app.route('/vision', methods=['post', 'get'])
def vision():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        visionf = request.form.get("visionf")
        visions = request.form.get("visions")
        if visionf is not None and visions is not None:
            session["visionf"] = visionf
            session["visions"] = visions
            session['pagenum'] += 1
            if int(session["visionf"]) >= 0 and int(session["visions"]) >= 0:
                session['cogscoref'] = int(visionf)
                session['cogscores'] = int(visions)
                session['cogscore'] = (int(session['visionf']) + int(session['visions'])) / 2
                # end = True
                cogname = 'unable41'
                return redirect(url_for('depth'))

        else:
            return render_template("dsq/vision41.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/vision41.html", message='', pagenum=session['pagenum'])

@app.route('/depth', methods=['post', 'get'])
def depth():
    global end
    form = FlaskForm()
    if request.method == "POST":
        depthf = request.form.get("depthf")
        depths = request.form.get("depths")
        if depthf is not None and depths is not None:
            session["depthf"] = depthf
            session["depths"] = depths
            session['pagenum'] += 1
            return redirect(url_for("slowness"))
        else:
            return render_template("dsq/depth42.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/depth42.html", message='', pagenum=session['pagenum'])

@app.route('/slowness', methods=['post', 'get'])
def slowness():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        slowf = request.form.get("slowf")
        slows = request.form.get("slows")
        if slowf is not None and slows is not None:
            session["slowf"] = slowf
            session["slows"] = slows
            session['pagenum'] += 1
            if int(session["slowf"]) >= 0 and int(session["slows"]) >= 0:
                session['cogscoref'] = int(slowf)
                session['cogscores'] = int(slows)
                session['cogscore'] = (int(session['slowf']) + int(session['slowf'])) / 2
                # end = True
                cogname = 'slowness43'
                return redirect(url_for("absent"))
            else:
                return redirect(url_for("absent"))
        else:
            return render_template("dsq/slowness43.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/slowness43.html", message='', pagenum=session['pagenum'])

@app.route('/absent', methods=['post', 'get'])
def absent():
    form = FlaskForm()
    global end
    global cogname
    if request.method == "POST":
        absentf = request.form.get("absentf")
        absents = request.form.get("absents")
        if absentf is not None and absents is not None:
            session["absentf"] = absentf
            session["absents"] = absents
            session['pagenum'] += 1
            if int(session["absentf"]) >= 0 and int(session["absents"]) >= 0:
                session['cogscoref'] = int(absentf)
                session['cogscores'] = int(absents)
                session['cogscore'] = (int(session['absentf']) + int(session['absents'])) / 2
                # end = True
                cogname = 'absent44'
                return redirect(url_for("bladder"))
        else:
            return render_template("dsq/absent44.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/absent44.html", message='', pagenum=session['pagenum'])


@app.route('/bladder', methods=['post', 'get'])
def bladder():
    global end
    form = FlaskForm()
    if request.method == "POST":
        bladderf = request.form.get("bladderf")
        bladders = request.form.get("bladders")
        if bladderf is not None and bladders is not None:
            session["bladderf"] = bladderf
            session["bladders"] = bladders
            session['pagenum'] += 1
            return redirect(url_for("nausea"))
        else:
            return render_template("dsq/bladder45.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/bladder45.html", message='', pagenum=session['pagenum'])


@app.route('/nausea', methods=['post', 'get'])
def nausea():
    global end
    form = FlaskForm()
    if request.method == "POST":
        nauseaf = request.form.get("nauseaf")
        nauseas = request.form.get("nauseas")
        if nauseaf is not None and nauseas is not None:
            session["nauseaf"] = nauseaf
            session["nauseas"] = nauseas
            session['pagenum'] += 1
            return redirect(url_for("shortness"))
        else:
            return render_template("dsq/nausea47.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/nausea47.html", message='', pagenum=session['pagenum'])


@app.route('/shortness', methods=['post', 'get'])
def shortness():
    global end
    form = FlaskForm()
    if request.method == "POST":
        shortf = request.form.get("shortf")
        shorts = request.form.get("shorts")
        if shortf is not None and shorts is not None:
            session["shortf"] = shortf
            session["shorts"] = shorts
            session['pagenum'] += 1
            return redirect(url_for("dizzy"))
        else:
            return render_template("dsq/shortness49.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/shortness49.html", message='', pagenum=session['pagenum'])

@app.route('/dizzy', methods=['post', 'get'])
def dizzy():
    global end
    form = FlaskForm()
    if request.method == "POST":
        dizzyf = request.form.get("dizzyf")
        dizzys = request.form.get("dizzys")
        if dizzyf is not None and dizzys is not None:
            session["dizzyf"] = dizzyf
            session["dizzys"] = dizzys
            session['pagenum'] += 1
            return redirect(url_for("heart"))
        else:
            return render_template("dsq/dizzy50.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/dizzy50.html", message='', pagenum=session['pagenum'])

@app.route('/heart', methods=['post', 'get'])
def heart():
    global end
    form = FlaskForm()
    if request.method == "POST":
        heartf = request.form.get("heartf")
        hearts = request.form.get("hearts")
        if heartf is not None and hearts is not None:
            session["heartf"] = heartf
            session["hearts"] = hearts
            session['pagenum'] += 1
            return redirect(url_for("weight"))
        else:
            return render_template("dsq/heart51.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/heart51.html", message='', pagenum=session['pagenum'])


@app.route('/weight', methods=['post', 'get'])
def weight():
    global end
    form = FlaskForm()
    if request.method == "POST":
        weightf = request.form.get("weightf")
        weights = request.form.get("weights")
        if weightf is not None and weights is not None:
            session["weightf"] = weightf
            session["weights"] = weights
            session['pagenum'] += 1
            return redirect(url_for("appetite"))
        else:
            return render_template("dsq/weight52.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/weight52.html", message='', pagenum=session['pagenum'])


@app.route('/appetite', methods=['post', 'get'])
def appetite():
    global end
    form = FlaskForm()
    if request.method == "POST":
        appetitef = request.form.get("appetitef")
        appetites = request.form.get("appetites")
        if appetitef is not None and appetites is not None:
            session["appetitef"] = appetitef
            session["appetites"] = appetites
            session['pagenum'] += 1
            return redirect(url_for("sweating"))
        else:
            return render_template("dsq/appetite53.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/appetite53.html", message='', pagenum=session['pagenum'])


@app.route('/sweating', methods=['post', 'get'])
def sweating():
    global end
    form = FlaskForm()
    if request.method == "POST":
        sweatf = request.form.get("sweatf")
        sweats = request.form.get("sweats")
        if sweatf is not None and sweats is not None:
            session["sweatf"] = sweatf
            session["sweats"] = sweats
            session['pagenum'] += 1
            return redirect(url_for("night"))
        else:
            return render_template("dsq/sweating54.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/sweating54.html", message='', pagenum=session['pagenum'])


@app.route('/night', methods=['post', 'get'])
def night():
    global end
    form = FlaskForm()
    if request.method == "POST":
        nightf = request.form.get("nightf")
        nights = request.form.get("nights")
        if nightf is not None and nights is not None:
            session["nightf"] = nightf
            session["nights"] = nights
            session['pagenum'] += 1
            return redirect(url_for("chills"))
        else:
            return render_template("dsq/night55.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/night55.html", message='', pagenum=session['pagenum'])


@app.route('/chills', methods=['post', 'get'])
def chills():
    global end
    form = FlaskForm()
    if request.method == "POST":
        chillsf = request.form.get("chillsf")
        chillss = request.form.get("chillss")
        if chillsf is not None and chillss is not None:
            session["chillsf"] = chillsf
            session["chillss"] = chillss
            session['pagenum'] += 1
            return redirect(url_for("hitemp"))
        else:
            return render_template("dsq/chills57.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/chills57.html", message='', pagenum=session['pagenum'])


@app.route('/hitemp', methods=['post', 'get'])
def hitemp():
    global end

    form = FlaskForm()
    if request.method == "POST":
        hitempf = request.form.get("hitempf")
        hitemps = request.form.get("hitemps")
        if hitempf is not None and chills is not None:
            session["hitempf"] = hitempf
            session["hitemps"] = hitemps
            session['pagenum'] += 1
            return redirect(url_for("lotemp"))
        else:
            return render_template("dsq/hitemp59.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/hitemp59.html", message='', pagenum=session['pagenum'])


@app.route('/lotemp', methods=['post', 'get'])
def lotemp():
    global end

    form = FlaskForm()
    if request.method == "POST":
        lotempf = request.form.get("lotempf")
        lotemps = request.form.get("lotemps")
        if lotempf is not None and lotemps is not None:
            session["lotempf"] = lotempf
            session["lotemps"] = lotemps
            session['pagenum'] += 1
            return redirect(url_for("alcohol"))
        else:
            return render_template("dsq/lotemp60.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/lotemp60.html", message='', pagenum=session['pagenum'])


@app.route('/alcohol', methods=['post', 'get'])
def alcohol():
    global end

    form = FlaskForm()
    if request.method == "POST":
        alcoholf = request.form.get("alcoholf")
        alcohols = request.form.get("alcohols")
        if alcoholf is not None and alcohols is not None:
            session["alcoholf"] = alcoholf
            session["alcohols"] = alcohols
            session['pagenum'] += 1
            return redirect(url_for("throat"))
        else:
            return render_template("dsq/alcohol61.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/alcohol61.html", message='', pagenum=session['pagenum'])


@app.route('/throat', methods=['post', 'get'])
def throat():
    global end
    form = FlaskForm()
    if request.method == "POST":
        throatf = request.form.get("throatf")
        throats = request.form.get("throats")
        if throatf is not None and throats is not None:
            session["throatf"] = throatf
            session["throats"] = throats
            session['pagenum'] += 1
            return redirect(url_for("lymphnodes"))
        else:
            return render_template("dsq/throat62.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/throat62.html", message='', pagenum=session['pagenum'])


@app.route('/lymphnodes', methods=['post', 'get'])
def lymphnodes():
    global end
    form = FlaskForm()
    if request.method == "POST":
        lymphnodesf = request.form.get("lymphnodesf")
        lymphnodess = request.form.get("lymphnodess")
        if lymphnodesf is not None and lymphnodess is not None:
            session["lymphnodesf"] = lymphnodesf
            session["lymphnodess"] = lymphnodess
            session['pagenum'] += 1
            return redirect(url_for("fever"))
        else:
            return render_template("dsq/lymphnodes63.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/lymphnodes63.html", message='', pagenum=session['pagenum'])


@app.route('/fever', methods=['post', 'get'])
def fever():
    global end
    form = FlaskForm()
    if request.method == "POST":
        feverf = request.form.get("feverf")
        fevers = request.form.get("fevers")
        if feverf is not None and fevers is not None:
            session["feverf"] = feverf
            session["fevers"] = fevers
            session['pagenum'] += 1
            return redirect(url_for("graph3"))
        else:
            return render_template("dsq/fever64.html", message=message, pagenum=session['pagenum'])
    return render_template("dsq/fever64.html", message='', pagenum=session['pagenum'])

@app.route('/dsq_dx', methods=['get'])
def graph3():
    return dsq_utils.dsq_diagnose()

@app.route('/about', methods=['post', 'get'])
def about():
    return render_template('about.html')


@app.route('/aboutmecfs', methods=['post', 'get'])
def aboutmecfs():
    return render_template('aboutmecfs.html')

# uncomment to display routes in log
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)

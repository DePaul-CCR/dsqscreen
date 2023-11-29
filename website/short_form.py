from flask import Blueprint, render_template, session, request, redirect, url_for
import utils.short_form_utils as short_form_utils
from utils.general_utils import get_score, get_client_ip

short_form = Blueprint('short_form', __name__)

message = "Please enter a response for both frequency and severity before continuing"

@short_form.route('/soreness', methods=['post', 'get'])
def expem1():
    global pemname
    if request.method == "POST":
        soref = request.form.get("soref")
        sores = request.form.get("sores")
        if soref is not None and sores is not None:
            session["soref"] = soref
            session["sores"] = sores
            session['pagenum'] += 1
            if get_score("soref") >= 0 and get_score("sores") >= 0:
                session['pemscoref'] = session['soref']
                session['pemscores'] = session['sores']
                session['pemscore'] = (get_score('soref') + get_score('sores')) / 2
                pemname = 'soreness15'
                return redirect(url_for("short_form.excog1"))
        else:
            return render_template("short_form/expem1.html", pagenum=session['pagenum'], message=message)
    return render_template("short_form/expem1.html", pagenum=session['pagenum'], message='')

@short_form.route('/attention', methods=['post', 'get'])
def excog1():
    global cogname
    if request.method == "POST":
        attentionf = request.form.get("attentionf")
        attentions = request.form.get("attentions")
        if attentions is not None and attentionf is not None:
            session["attentionf"] = attentionf
            session["attentions"] = attentions
            session['pagenum'] += 1
            if get_score("attentionf") >= 0 and get_score("attentions") >= 0:
                session['cogscoref'] = int(attentionf)
                session['cogscores'] = int(attentions)
                cogname = 'difficulty37'
                session['cogscore'] = (get_score('attentionf') + get_score('attentions')) / 2
                end = True
                return redirect(url_for("short_form.musclepain"))
        else:
            return render_template("short_form/excog1.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/excog1.html", message='', pagenum=session['pagenum'])

@short_form.route('/musclepain', methods=['post', 'get'])
def musclepain():
    global end
    if request.method == "POST":
        musclef = request.form.get("musclef")
        mucles = request.form.get("muscles")
        if musclef is not None and mucles is not None:
            session["musclef"] = musclef
            session["muscles"] = mucles
            session['pagenum'] += 1
            return redirect(url_for("short_form.bloating"))
        else:
            return render_template("short_form/musclepain.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/musclepain.html", message='', pagenum=session['pagenum'])

@short_form.route('/bloating', methods=['post', 'get'])
def bloating():
    global end
    if request.method == "POST":
        bloatf = request.form.get("bloatf")
        bloats = request.form.get("bloats")
        if bloats is not None and bloatf is not None:
            session["bloatf"] = bloatf
            session["bloats"] = bloats
            session['pagenum'] += 1
            return redirect(url_for("short_form.bowel"))
        else:
            return render_template("short_form/bloating.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/bloating.html", message='', pagenum=session['pagenum'])

@short_form.route('/bowel', methods=['post', 'get'])
def bowel():
    global end
    if request.method == "POST":
        bowelf = request.form.get("bowelf")
        bowels = request.form.get("bowels")
        if bowels is not None and bowelf is not None:
            session["bowelf"] = bowelf
            session["bowels"] = bowels
            session['pagenum'] += 1
            return redirect(url_for("short_form.unsteady"))
        else:
            return render_template("short_form/bowel.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/bowel.html", message='', pagenum=session['pagenum'])

@short_form.route('/unsteady', methods=['post', 'get'])
def unsteady():
    global end
    if request.method == "POST":
        unsteadyf = request.form.get("unsteadyf")
        unsteadys = request.form.get("unsteadys")
        if unsteadyf is not None and unsteadys is not None:
            session["unsteadyf"] = unsteadyf
            session["unsteadys"] = unsteadys
            session['pagenum'] += 1
            return redirect(url_for("short_form.cold_limbs"))
        else:
            return render_template("short_form/unsteady.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/unsteady.html", message='', pagenum=session['pagenum'])

@short_form.route('/cold_limbs', methods=['post', 'get'])
def cold_limbs():
    global end
    if request.method == "POST":
        limbsf = request.form.get("limbsf")
        limbss = request.form.get("limbss")
        if limbsf is not None and limbss is not None:
            session["limbsf"] = limbsf
            session["limbss"] = limbss
            session['pagenum'] += 1
            return redirect(url_for("short_form.hot_cold"))
        else:
            return render_template("short_form/limbs.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/limbs.html", message='', pagenum=session['pagenum'])

@short_form.route('/hot_cold', methods=['post', 'get'])
def hot_cold():
    global end
    if request.method == "POST":
        hotf  = request.form.get("hotf")
        hots = request.form.get("hots")
        if hotf is not None and hots is not None:
            session["hotf"] = hotf
            session["hots"] = hots
            session['pagenum'] += 1
            return redirect(url_for("short_form.flu"))
        else:
            return render_template("short_form/hot.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/hot.html", message='', pagenum=session['pagenum'])

@short_form.route('/flu', methods=['post', 'get'])
def flu():
    global end
    if request.method == "POST":
        fluf  = request.form.get("fluf")
        flus = request.form.get("flus")
        if fluf is not None and flus is not None:
            session["fluf"] = fluf
            session["flus"] = flus
            session['pagenum'] += 1
            return redirect(url_for("short_form.smells"))
        else:
            return render_template("short_form/flu.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/flu.html", message='', pagenum=session['pagenum'])

@short_form.route('/smells', methods=['post', 'get'])
def smells():
    global end
    global survey
    if request.method == "POST":
        smellf = request.form.get("smellf")
        smells = request.form.get("smells")
        if smellf is not None and smells is not None:
            session["smellf"] = smellf
            session["smells"] = smells
            session['pagenum'] += 1
            survey='rf14'
            return redirect(url_for('short_form.reduction'))
        else:
            return render_template("short_form/smells.html", message=message, pagenum=session['pagenum'])
    return render_template("short_form/smells.html", message='', pagenum=session['pagenum'])

@short_form.route('/reduction', methods=['post', 'get'])
def reduction():
    msg_reduction = "Please select one of the options before continuing"
    if request.method == 'POST':
        reduction = request.form.get('reduction')
        if reduction is not None:
            session['reduction'] = reduction
            session['pagenum'] += 1
            return redirect(url_for('short_form.graph2'))
        else:
            return render_template("short_form/reduction.html", message=msg_reduction, pagenum=session['pagenum'])
    return render_template("short_form/reduction.html", message='', pagenum=session['pagenum'])

@short_form.route('/short_form_dx', methods=['post', 'get'])
def graph2():
    # store IP for response data export
    session['ip'] = get_client_ip()
    return short_form_utils.short_form_diagnose()
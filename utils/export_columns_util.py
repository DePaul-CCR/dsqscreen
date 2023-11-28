import pandas as pd
import pygsheets
import datetime

def build_dataframe_for_export (session, stage = "dsq"):
  df = pd.DataFrame()
  df['sid'] = [session.sid]
  # stores UTC time timestamp
  df['date'] = datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y")
  df['time'] = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
  df['ip'] = session['ip']
  # add all items currently collected to the data frame
  for item in get_columns_for_stage(stage):
    if session[item]:
      df[item] = [session[item]]
    else:
      df[item] = None
  return df

# def get_service_file_path():

def dump_collected_data_to_sheet(df):
  # TODO: fix this to use environment for prod / debug
  try: 
    gc = pygsheets.authorize(service_file='/etc/secrets/dsqscreen-401016-0e6db07e3d56.json')
  except:
    gc = pygsheets.authorize(service_file='etc/secrets/dsqscreen-401016-0e6db07e3d56.json')

  sh = gc.open('DSQScreen Output')
  wks=sh[0]
  # finds if session_id already exists in the sheet and replaced values if so
  # session_row = wks.find(df['sid'][0])
  # if bool(session_row):
  #   wks.update_values(session_row[0].label, values=df.values.tolist())
  # else:
  wks.update_values("A" + get_next_row(wks), df.values.tolist())

def get_next_row(wks):
  # returns a string of length of column 1 + 1
  return str(len(wks.get_col(1,include_tailing_empty=False)) + 1)

def get_columns_for_stage(stage):
  if stage == "screener":
    return screener_columns
  elif stage == "short_form":
    return screener_columns + sf_columns
  else:
    return screener_columns + sf_columns + dsq_columns

screener_columns = [
"fatiguescoref",
"fatiguescores",
"minexf",
"minexs",
"sleepf",
"sleeps",
"rememberf",
"remembers"]

sf_columns = [
"soref",
"sores",
"attentionf",
"attentions",
"musclef",
"muscles",
"bloatf",
"bloats",
"bowelf",
"bowels",
"unsteadyf",
"unsteadys",
"limbsf",
"limbss",
"hotf",
"hots",
"fluf",
"flus",
"smellf",
"smells",
"reduction"]

dsq_columns = [
"viral",
"heavyf",
"heavys",
"mentalf",
"mentals",
"drainedf",
"draineds",
"napf",
"naps",
"fallf",
"falls",
"stayf",
"stays",
"earlyf",
"earlys",
"alldayf",
"alldays",
"jointpainf",
"jointpains",
"eyepainf",
"eyepains",
"chestpainf",
"chestpains",
"stomachf",
"stomachs",
"headachesf",
"headachess",
"twitchesf",
"twitchess",
"weakf",
"weaks",
"noisef",
"noises",
"lightsf",
"lightss",
"wordf",
"words",
"understandf",
"understands",
"focusf",
"focuss",
"visionf",
"visions",
"depthf",
"depths",
"slowf",
"slows",
"absentf",
"absents",
"bladderf",
"bladders",
"nauseaf",
"nauseas",
"shortf",
"shorts",
"dizzyf",
"dizzys",
"heartf",
"hearts",
"weightf",
"weights",
"appetitef",
"appetites",
"sweatf",
"sweats",
"nightf",
"nights",
"chillsf",
"chillss",
"hitempf",
"hitemps",
"lotempf",
"lotemps",
"alcoholf",
"alcohols",
"throatf",
"throats",
"lymphnodesf",
"lymphnodess",
"feverf",
"fevers",
"intolerant"]

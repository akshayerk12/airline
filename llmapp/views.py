from django.shortcuts import render
import json
import numpy as np
import pandas as pd
from joblib import load
import google.generativeai as palm
from .models import Airline

API_KEY='AIzaSyAE1LnzZV8qgJ6_yjkuvXrgVSqAlD9NxCA'
palm.configure(api_key=API_KEY)
model_id='models/text-bison-001'

model=load('./savedmodels/lr.joblib')

with open('./savedmodels/airline_names.json') as file:
    data=json.load(file)
airline_name=data['airlines']

with open('./savedmodels/prediction_lits.json') as file:
    data=json.load(file)
pred_cols=data['pred_list']

recomend_df=pd.read_csv('./savedmodels/recommendation.csv')

def Welcome(request):
    return render(request,'main.html')

def ReviewAdder(request):
            
    airline=request.POST.get('airline')
    seat_type=request.POST.get('seat_type')
    From_loc=request.POST.get('From')
    To=request.POST.get('To')
    seat_type=request.POST.get('seat_type')
    seat_comfort=request.POST.get('seat_comfort')
    cabin_crew=request.POST.get('cabin_crew')
    ground_service=request.POST.get('ground_service')
    review=request.POST.get('review')

    promt='''
    Do sentimental analysis of the sentence give 1 if it is positive or 0 if it is negative
    '''

    pred=''
    completion=palm.generate_text(
    model=model_id,
    prompt=f"{review}\n{promt}",
    temperature=0.0,
    max_output_tokens=1600,
    candidate_count=1)
    result=int(completion.result)
    if result==1:
        pred='Yes'
    if result==0:
        pred='No'
    
    Airline.objects.create(airline=airline, From_location=From_loc,
                            To_location=To,
                            seat_type=seat_type,
                            seat_comfort=seat_comfort,
                            cabin_crew=cabin_crew,
                            ground_service=ground_service,
                            review=review,
                            result=pred)

    return render(request,'succes.html')

def DecriptionCreator(airline,airline_dict):
    promt=''' Give 20 words decription of this airline'''
    generation=palm.generate_text(
    model=model_id,
    prompt=f"{airline}\n{promt}",
    temperature=0.0,
    max_output_tokens=1600,
    candidate_count=1)
    res=[]
    res.append(generation.result)
    airline_dict[airline]=res
    

def Review(request):
    return render(request,'review.html')

def Suggest(request):
    return render(request,'suggest.html')

def cosine(a,b):
  dot=np.dot(a,b)
  norm_a=np.linalg.norm(a)
  norm_b=np.linalg.norm(b)
  return dot/(norm_a*norm_b)

def Recommend(request):
    airline_dict={}
    
    seattype=request.POST.get('seattype')
    From=request.POST.get('from')
    To=request.POST.get('to')
    depart_time=request.POST.get('depart_time')
    arrival_time=request.POST.get('arrival_time')
    stops=float(request.POST.get('stops'))+1
    days=float(request.POST.get('days'))

    sorted_df=recomend_df[(recomend_df['source_city']==From) & (recomend_df['destination_city']==To)]
    dur=sorted_df['duration'].mode()
    matrix=sorted_df.iloc[:,3:-1]
    columns=matrix.columns.to_list()
    matrix=matrix.to_numpy()
    X=np.zeros(len(columns))

    seat_index=columns.index(seattype)
    depart_index=columns.index(depart_time)
    arrival_index=columns.index(arrival_time)
    stop_index=columns.index('stops')
    duration_index=columns.index('duration')

    X[seat_index]=1
    X[depart_index]=1
    X[arrival_index]=1
    X[stop_index]=stops
    X[duration_index]=2





    similarities = [cosine(X, user) for user in matrix]
    N=3
    top_airlines=np.argsort(similarities)[::-1][:N]
    
    airline_for_lr=[]
    for airline in top_airlines:
        if airline_name[airline+1] not in airline_for_lr:
            airline_for_lr.append(airline_name[airline+1])
        DecriptionCreator(airline_name[airline+1],airline_dict)

    X_predict=np.zeros(len(pred_cols))
    From='from_'+From
    To='to_'+To

    for flight in airline_for_lr:
        seat_index=pred_cols.index(seattype)
        from_index=pred_cols.index(From)
        to_index=pred_cols.index(To)
        stop_index=pred_cols.index('stops')
        start_index=pred_cols.index(depart_time)
        end_index=pred_cols.index(arrival_time)
        days_index=pred_cols.index('days_left')
        airline_index=pred_cols.index(flight)
        dur=pred_cols.index('duration')

        X_predict[seat_index]=1
        X_predict[from_index]=1
        X_predict[to_index]=1
        X_predict[stop_index]=stops
        X_predict[start_index]=1
        X_predict[end_index]=1
        X_predict[days_index]=days
        X_predict[airline_index]=1
        X_predict[dur]=dur

        to_update=airline_dict[flight]
        to_update.append(int(model.predict([X_predict])))
        airline_dict[flight]=to_update
    
    return render(request,'display.html',{'result':airline_dict})
from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
import json
from model import Patient

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get('/')
def hello():
    return {'message':'Patient Management System API'}

@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patient record'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(...,description='Patient ID in DB',example='2')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='sort on basis of age,weight,bmi'),
                  order_by:str = Query('asc',description='sort in asc or desc')):
    valid_feilds = ['age','weight_kg','bmi']
    
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail=f'Invalid Order Filed Select from {valid_feilds}')

    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid Select asc or desc')
    
    data = load_data()
    
    order = True if order_by =='desc' else  False
    
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=order)
    
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):
    
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'Patient added succesfully!'})
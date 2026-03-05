from fastapi import FastAPI,HTTPException,Path,Query
from schema.user_input import UserInput,UpdateStudent
from database.college_management import add_data,view_all_data,view_a_student,delete_data,Sorted_data,update_student
import os
from dotenv import load_dotenv

load_dotenv()
version = os.getenv("APP_VERSION")

app = FastAPI()

@app.get('/')
def info():
    return {"message":"SAITM Students Details API"}

@app.get('/about')
def about():
    return {
        'status':'ok',
        'verison': version,
    }

@app.post('/add_details')
def add_student(st : UserInput):
    try:
        result = add_data(st)
        return result
    except Exception as e:
        raise  HTTPException(status_code=400,detail=str(e))

@app.get('/students')
def view_all():
    return view_all_data()

@app.get('/students/sort')
def sort_student(sort_by: str = Query(...,description='Sort on the basis of st_id, age, dept_id'), order: str = Query('asc',description="sort in asc or desc order")):
    return Sorted_data(sort_column=sort_by,sort_order=order)

@app.get('/students/{st_id}')
def view_student(st_id : int = Path(...,description='ID of student',examples=[261012,261021])):
    return view_a_student(st_id)

@app.patch('/edit_student/{st_id}')
def student_update(st_id: int, details: UpdateStudent):
    updated = update_student(st_id,details)
    if not updated:
        raise HTTPException(status_code=404,detail="Student not found")
    return {"status":"Updated Successfully","data":updated}


@app.delete('/delete/{st_id}')
def delete_student(st_id: int):
        delete_data(st_id)
        return {"message":"Successfully deleted"}
    


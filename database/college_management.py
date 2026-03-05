from sqlalchemy import create_engine,String,ForeignKey,CheckConstraint,func,asc,desc
from sqlalchemy.orm import DeclarativeBase,sessionmaker,relationship,Mapped,mapped_column,joinedload
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

#creating the engine
# format: dialect+driver://username:password@localhost:port/your_db
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url,echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit = False
                            )

#making base class
class Base(DeclarativeBase):
    pass

#creating blueprint of department class
class Department(Base):
    __tablename__ = "departments_detail"
    dept_id : Mapped[int] = mapped_column(primary_key=True)
    dept_name:Mapped[str] = mapped_column(String(50))
    students : Mapped[list["Student"]] = relationship(
        back_populates='department',
        cascade='all, delete-orphan'
    )
    __table_args__ = ({'extend_existing':True})

    def __repr__(self) -> str:
        return f"departments_detail(dept_id = {self.dept_id},dept_name = {self.dept_name})\n"
        
#creating blueprint of student class on join with department class 
class Student(Base):
    __tablename__ = "students_detail"
    st_id : Mapped[int] = mapped_column(primary_key=True)
    st_name : Mapped[str] = mapped_column(String(30))
    age : Mapped[int] 
    email : Mapped[str] = mapped_column(unique=True)
    city : Mapped[str] = mapped_column(String(50))

    dept_id: Mapped[int] = mapped_column(ForeignKey("departments_detail.dept_id"),index=True)   
    department: Mapped["Department"] = relationship(
        back_populates= 'students'
    )
    __table_args__ = (
        CheckConstraint("age>=18 AND age<=100",name = 'age_check'),
        {'extend_existing':True}
        )

    def __repr__(self)-> str:
        return f"students_detail(st_id : {self.st_id},st_name : {self.st_name},age : {self.age},city : {self.city},email:{self.email})\n"

#creating all tables
Base.metadata.create_all(engine)


def view_all_data():
    with SessionLocal() as session:
        students = session.query(Student).options(joinedload(Student.department)).all()
        result = []
        for s in students:
            dic = {"st_id":s.st_id,"St name":s.st_name,"dept name":s.department.dept_name,"dept_id":s.dept_id,"age":s.age,"city":s.city,"email":s.email}
            result.append(dic)
        return result
    
def Sorted_data(sort_column=None, sort_order='asc'):
    with SessionLocal() as session:
        query = session.query(Student).options(joinedload(Student.department))
        valid_fields = ["st_id","age","dept_id"]
        if sort_column in valid_fields and sort_order in ['asc','desc']:
            column = getattr(Student,sort_column)
            query = query.order_by(desc(column) if sort_order=='desc' else asc(column))
            students = query.all()
            result = []
            for s in students:
                dic = {"st_id":s.st_id,"St name":s.st_name,"dept name":s.department.dept_name,"dept_id":s.dept_id,"age":s.age,"city":s.city,"email":s.email}
                result.append(dic)
            return result
        else: raise HTTPException(status_code=400,detail=f"valid fields are: {valid_fields}")



def view_a_student(id):
    with SessionLocal() as session:
        s = session.query(Student).filter_by(st_id = id).first()
        if not s:
            raise HTTPException(status_code=404,detail=f"Student not found with st_id: {id}")
        dic = {"St Id":s.st_id,"St name":s.st_name,"age":s.age,"city":s.city,"email":s.email,"dept name":s.department.dept_name,"dept Id":s.dept_id}
        return dic

def get_st_value():
    with SessionLocal() as session:
        results = session.query(Student.dept_id,func.max(Student.st_id)).group_by(Student.dept_id).all()
        max_ids = dict(results)
        
        result = {}
        for key in [101,102,103,104]:
            if key in max_ids:
                result[key] = int(str(max_ids[key])[5:])
            else:
                result[key] = 0
        return result
    
def add_data(detail):
    with SessionLocal() as session:
        try:
            dept = session.query(Department).filter_by(dept_id=101).first()
            if not dept:
                depts = [
                    Department(dept_id = 101,dept_name="CSE"),
                    Department(dept_id = 102,dept_name="ELECTRONICS"),
                    Department(dept_id = 103,dept_name="AIML"),
                    Department(dept_id = 104,dept_name="DATA SCIENCE")
                ]
                session.add_all(depts)
                session.flush()
            s = Student(st_id = detail.st_id,st_name = detail.st_name,age = detail.age,email = detail.email,city = detail.city,dept_id = detail.dept_id)
            session.add(s)
            session.commit()
            session.refresh(s)
            return s
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400,detail=str(e))


def update_student(stId: int, new_data):
    with SessionLocal() as session:
        student = session.query(Student).filter_by(st_id = stId).first()

        if not student:
            return "Query not Came"
        
        updated_student = new_data.model_dump(exclude_unset=True,exclude_none=True)

        if "dept_name" in updated_student:
            updated_student.pop("dept_name")

        for key, value in updated_student.items():
            setattr(student,key,value)

        session.commit()
        session.refresh(student)
        return student

def delete_data(id):
    with SessionLocal() as session:
        s = session.query(Student).filter_by(st_id = id).first()
        if not s:
            raise HTTPException(status_code=404,detail=f"Student not found with st_id: {id}")

        try:
            session.delete(s)
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=404,detail=print(e))
            
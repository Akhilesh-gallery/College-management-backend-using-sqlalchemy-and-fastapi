from pydantic import BaseModel,Field,field_validator, computed_field
from typing import Annotated,Literal,ClassVar,Optional
from database.college_management import get_st_value

class UserInput(BaseModel):
    _dept_counter : ClassVar[dict[int,int]] = get_st_value()
    
    year : Annotated[int, Field(...,description='Give in which year student is enrolling',examples=[2026,2025])]
    st_name : Annotated[str,Field(...,description='Enter the student name',examples=['Anup Kumar','Ashish Singh'])]
    age : Annotated[int,Field(...,ge=18,lt=80,description='What is age of the student',examples=[18,20,23])]
    city : Annotated[str,Field(...,description='Enter district and state',examples=['Gurugram','Ayodya'])]
    dept_name : Annotated[Literal["CSE","AIML","ELECTRONICS","DATA SCIENCE"], Field(...,description='Select department name of a student',examples=["CSE","AIML","Electronics","Data Science"])]

    @field_validator('st_name','dept_name',mode="before")
    @classmethod
    def validate_names(cls,name):
        return name.upper()
    
    @computed_field
    @property
    def dept_id(self)->int:
        #genrating dept ID
        dept_map = {'CSE':101,'ELECTRONICS':102,'AIML':103,'DATA SCIENCE':104}
        return dept_map[self.dept_name]
    
    @computed_field
    @property
    def st_id(self)->int:
        digit = int("".join(str(self.year)[2:]))
        count = UserInput._dept_counter[self.dept_id] + 1
        return int(f"{digit}{self.dept_id}{count}")
    
    @computed_field
    @property
    def email(self)->str:
        name = self.st_name.split()[0].lower()
        return f"{name}_{self.st_id}@saitm.ac.in"


    def model_post_init(self, __context):
        if self.dept_id in UserInput._dept_counter:
            UserInput._dept_counter[self.dept_id] += 1


class UpdateStudent(BaseModel):
    st_name : Annotated[Optional[str],Field(default=None,description='Enter name of student',examples=[None])]=None
    age : Annotated[Optional[int],Field(default=None,le=80,ge=18,description='Enter the age',examples=[None])]=None
    city : Annotated[Optional[str],Field(default=None, description="Enter your new city",examples=[None])]=None
    dept_name : Annotated[Optional[Literal["CSE","AIML","ELECTRONICS","DATA SCIENCE"]], Field(default=None,description="Enter your new department name",examples=[None])]=None


    @field_validator('st_name','dept_name',mode="before")
    @classmethod
    def validate_names(cls,name):
        if name is not None:
            return name.upper() 
        return name
    
    @computed_field
    @property
    def dept_id(self)-> Optional[int]:
        #genrating dept ID
        if self.dept_name is None:
            return None
        dept_map = {'CSE':101,'ELECTRONICS':102,'AIML':103,'DATA SCIENCE':104}
        return dept_map[self.dept_name]
    
    


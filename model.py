from pydantic import BaseModel,Field,computed_field
from typing import Optional,Annotated,Literal

class Patient(BaseModel):
    
    id:Annotated[str,Field(...,description='ID of patient',examples=['3'])]
    name:Annotated[str,Field(...,description='Name of Patient')]
    age:Annotated[int,Field(...,gt=0,lt=80,description='Age of Patient')]
    gender:Annotated[Literal['Male','Female','others'],Field(...,description='Age of patient')]
    weight_kg:Annotated[float,Field(...,gt=0,description='Weight of patient in kg')]
    height_m:Annotated[float,Field(...,gt=0,description='height of patient in meter')]
    condition:Annotated[str,Field(...,description='Condition of patient')]
    last_visit:Optional[str] = None
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight_kg/(self.height_m**2),2)
        return bmi
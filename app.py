from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal , Annotated
import pickle
from pathlib import Path
import pandas as pd
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ----------------------------------------
# import ml model (load safely and provide helpful error when load fails)
# ----------------------------------------
MODEL_PATH = Path(__file__).resolve().parent / "pridict_model.pkl"
model = None
model_load_error = None

try:
    # Some models pickled with older scikit-learn versions reference
    # `sklearn.compose._column_transformer._RemainderColsList`, which
    # was removed in newer releases. Provide a lightweight alias so
    # unpickling can succeed on newer scikit-learn installations.
    try:
        import sklearn.compose._column_transformer as _ct
        if not hasattr(_ct, "_RemainderColsList"):
            class _RemainderColsList(list):
                pass
            _ct._RemainderColsList = _RemainderColsList
    except Exception:
        # If sklearn isn't installed or the module can't be imported,
        # let the subsequent pickle.load raise the appropriate error.
        pass

    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)
except ModuleNotFoundError as e:
    missing = getattr(e, "name", str(e))
    model_load_error = f"Missing dependency while loading model: {missing}. Install required packages and retry."
except AttributeError as e:
    if "_RemainderColsList" in str(e):
        model_load_error = (
            "ab nhi ho rha hai model load, scikit-learn ke version ka issue hai. Please install scikit-learn version 1.2.2 and retry."
        )
    else:
        model_load_error = str(e)
except Exception as e:
    model_load_error = str(e)


app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
"Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur",
                  "Bilaspur", "Jalandhar", "Noida",
                  "Guntur", "Asansol", "Siliguri"
]


# pydantic model to validate incoming data

class UserInput(BaseModel):
    age:Annotated[int, Field(..., gt=1, description="Age in years")]
    weight:Annotated[float, Field(..., gt=0, description="Weight in kg")]
    height:Annotated[float, Field(..., gt=0, description="Height in m")]
    income_lpa: Annotated[float , Field(..., gt=0, description="Income in lpa")]
    smoker:Annotated[bool, Field(..., description="Smoker or not")]
    city:Annotated[str, Field(..., min_length=1, description="City")]
    occupation: Annotated[Literal['retired', 'unemployed', 'business owner', 'government job', 'student', 'freelancer', 'private job'], Field(..., description='your work occupation')]
# using literal-> for giving options

    @computed_field
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return "middle_aged"
        return 'senior'

    @computed_field
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        

    @computed_field
    
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3




# with the help of this we can allow all origins to access our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # frontend origin
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Insurance Premium Prediction API. Use the /predict endpoint to get predictions."}

@app.post("/predict")
def predict(data: UserInput):


    # input that will be going to model
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'income_lpa': data.income_lpa,
        'city_tier': data.city_tier,
        'occupation': data.occupation

    }])
    
    if model is None:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Model not loaded",
                "details": model_load_error or "Unknown model loading error",
            },
        )

    # make prediction
    try:
        prediction = model.predict(input_df)[0]
        return JSONResponse(content={"predicted category": prediction})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

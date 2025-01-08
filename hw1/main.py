from fastapi import FastAPI, File, UploadFile, Response
from fastapi.encoders import jsonable_encoder
from io import StringIO
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
import pickle
import uvicorn


app = FastAPI()

MODEL_NAME = "models/ridge.pickle"


class Item(BaseModel):
    name: str
    year: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


class Items(BaseModel):
    objects: List[Item]


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['mileage', 'engine', 'max_power']:
        df[col] = df[col].str.extract(r'([\d\.]+)').astype('float')

    return df


def pydantic_model_to_df(model_instance):
    return pd.DataFrame([jsonable_encoder(model_instance)])

@app.get("/")
async def home():
    return {"message": "Сервер живой!!!"}


@app.post("/predict_item")
async def predict_item(item: Item) -> float:
    try:

        df_input = pydantic_model_to_df(item)

        df = preprocess_data(df_input)

        df = df.drop(['name', 'torque'], axis=1)

        with open(MODEL_NAME, 'rb') as model_file:
            model_pipeline = pickle.load(model_file)

        preds = model_pipeline.predict(df)
        result = round(float(preds), 2)

        return result

    except Exception as e:
        print(f"Exception occurred: {e}")

        return {"error": f"An error occurred: {e}"}


@app.post("/predict_items")
async def predict_items(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        df = df.drop(['name', 'torque', 'selling_price'], axis=1)
        df = preprocess_data(df)

        with open(MODEL_NAME, 'rb') as model_file:
            model_pipeline = pickle.load(model_file)

        preds = model_pipeline.predict(df)

        df['selling_price'] = np.round(preds, 2)

        csv_output = df.to_csv(index=False)

        return Response(content=csv_output, media_type='text/csv')

    except Exception as e:
        return {"error": str(e)}
import json

from pandas import DataFrame

def dataframe_to_json(df: DataFrame) -> json:
    data = df.to_json(orient="records")
    parsed = json.loads(data)
    result = {
        'headers': list(df),
        'rows': parsed
    }
    return result
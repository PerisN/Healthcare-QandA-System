import os
import pandas as pd
import minsearch

DATA_PATH = os.getenv("DATA_PATH")

def load_index():
    print(f"Loading data..")  # Debugging line
    df = pd.read_csv('app\sample_data.csv')

    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            "question",
            "answer",
        ],
        keyword_fields=['id']
    )

    index.fit(documents)
    return index
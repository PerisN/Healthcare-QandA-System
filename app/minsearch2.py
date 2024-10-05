import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Index:
    def __init__(self, vector_fields, keyword_fields):
        self.vector_fields = vector_fields
        self.keyword_fields = keyword_fields
        self.vector_matrices = {field: [] for field in vector_fields}
        self.keyword_df = None
        self.docs = []

    def fit(self, docs):
        self.docs = docs
        keyword_data = {field: [] for field in self.keyword_fields}

        for field in self.vector_fields:
            self.vector_matrices[field] = np.array([doc[field] for doc in docs])

        for doc in docs:
            for field in self.keyword_fields:
                keyword_data[field].append(doc.get(field, ''))

        self.keyword_df = pd.DataFrame(keyword_data)

        return self

    def search(self, query_vectors, filter_dict={}, boost_dict={}, num_results=10):
        scores = np.zeros(len(self.docs))

        for field, query_vec in query_vectors.items():
            if field in self.vector_matrices:
                sim = cosine_similarity(query_vec.reshape(1, -1), self.vector_matrices[field]).flatten()
                boost = boost_dict.get(field, 1)
                scores += sim * boost

        # Apply keyword filters
        for field, value in filter_dict.items():
            if field in self.keyword_fields:
                mask = self.keyword_df[field] == value
                scores = scores * mask.to_numpy()

        # Use argpartition to get top num_results indices
        top_indices = np.argpartition(scores, -num_results)[-num_results:]
        top_indices = top_indices[np.argsort(-scores[top_indices])]

        # Filter out zero-score results
        top_docs = [self.docs[i] for i in top_indices if scores[i] > 0]

        return top_docs
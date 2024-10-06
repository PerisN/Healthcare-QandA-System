import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Index:
    """
    A class for indexing and searching documents using both vector and keyword fields.

    This class allows for the creation of a hybrid search index that combines
    vector similarity search with keyword filtering. It supports multiple vector
    fields and keyword fields, allowing for flexible and powerful search capabilities.

    Attributes:
        vector_fields (list): List of field names for vector data.
        keyword_fields (list): List of field names for keyword data.
        vector_matrices (dict): Dictionary of numpy arrays for vector data.
        keyword_df (pandas.DataFrame): DataFrame for keyword data.
        docs (list): List of all indexed documents.

    Methods:
        fit(docs): Index the given documents.
        search(query_vectors, filter_dict, boost_dict, num_results): 
            Search the indexed documents using vector similarity and keyword filtering.
    """

    def __init__(self, vector_fields, keyword_fields):
        self.vector_fields = vector_fields
        self.keyword_fields = keyword_fields
        self.vector_matrices = {field: [] for field in vector_fields}
        self.keyword_df = None
        self.docs = []

    def fit(self, docs):
        """
        Index the given documents.

        Args:
            docs (list): List of documents to index.

        Returns:
            self: Returns the instance itself.
        """
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
        """
        Search the indexed documents using vector similarity and keyword filtering.

        Args:
            query_vectors (dict): Dictionary of query vectors for each vector field.
            filter_dict (dict): Dictionary of keyword filters to apply.
            boost_dict (dict): Dictionary of boost values for each vector field.
            num_results (int): Number of top results to return.

        Returns:
            list: List of top matching documents.
        """
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
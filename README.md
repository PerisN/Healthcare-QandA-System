# Health Assistant - Conversational AI for Health-Related Queries

Navigating health information can be overwhelming, especially when it comes to understanding symptoms, treatments, and wellness tips. Health professionals aren't always readily available, and searching the web can often lead to conflicting or confusing advice.

The Health Assistant provides an AI-powered solution, offering users instant responses to health-related queries. This project leverages large language models (LLMs) to provide a conversational experience that simplifies access to reliable health information.

This project was implemented as part of LLM Zoomcamp, showcasing the practical use of Retrieval-Augmented Generation (RAG) techniques for health-related queries.

## Project Overview

The Health Assistant is designed to assist users in various health-related areas. Whether it’s understanding symptoms or learning about medical treatments, the assistant provides information in an easy-to-use conversational format.

## Key Use Cases

 - Symptom Checker: Users can describe their symptoms, and the assistant suggests possible conditions or treatments, helping them decide if they need to consult a healthcare provider.

- Medication Information: Providing information about common medications, their uses, and possible side effects.

- Dietary Guidance: Offering personalized nutritional advice based on user preferences or health conditions (e.g., low sugar, high fiber).

- Health Alerts & First Aid Tips: Informing users about urgent health issues or offering quick tips for handling emergencies before professional help arrives.

## Dataset

This project utilizes a subset of the [MedQuAD](https://www.kaggle.com/datasets/jpmiller/layoutlm/data?select=medquad.csv) (Medical Question Answering Dataset), a comprehensive collection of medical question-answer pairs. 

Key features include:
1. Source: Derived from 12 NIH websites, including cancer.gov, niddk.nih.gov, GARD, and MedlinePlus Health Topics.
2. Scope: Originally containing 47,457 question-answer pairs covering 37 question types related to diseases, drugs, and medical tests.
3. Question types: Includes categories such as Treatment, Diagnosis, and Side Effects.
4. Sampling method: The dataset was sampled to include only one question per focus area, reducing redundancy and overall volume.
5. Purpose: To promote data science applications in healthcare, particularly in the field of medical question answering.

This curated dataset aims to provide a diverse yet focused collection of medical information, suitable for developing and testing healthcare-oriented data science models and applications.

### Reference
If you use the MedQuAD dataset and/or the collection of 2,479 judged answers, please cite the following paper: "A Question-Entailment Approach to Question Answering". Asma Ben Abacha and Dina Demner-Fushman. BMC Bioinformatics, 2019.

   @ARTICLE{BenAbacha-BMC-2019,
   author = {Asma {Ben Abacha} and Dina Demner{-}Fushman},
   title = {A Question-Entailment Approach to Question Answering},
   journal = {{BMC} Bioinform.},
   volume = {20},
   number = {1},
   pages = {511:1--511:23},
   year = {2019},
   url = {https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4}
   }

## Technology Stack
* Python 3.12.1: Core development
* Docker & Docker Compose: Containerization
* Minsearch: Full-text search
* OpenAI API: Language model integration
* Streamli: User Interface
* PostgreSQL: Database management
* Grafana: Monitoring and visualization
   
## Code Organization

- Main application code is in the `app` folder:
  - `app.py`: Flask API (main entry point)
  - `rag.py`: Core RAG logic
  - `ingest.py`: Data ingestion for knowledge base
  - `minsearch2.py`: In-memory search engine
  - `db.py`: Request/response logging to PostgreSQL
  - `db_prep.py`: Database initialization
  - `test.py`: Random question selector from generated ground truth data for testing
 

### Interface and Data Ingestion

- Flask serves the application as an API
- `ingest.py` handles data ingestion
- In-memory database (`minsearch2.py`) used as knowledge base
- Ingestion runs at application startup (executed in `rag.py`)

## Retrieval and Evaluation Experiments

- Jupyter notebooks in `notebooks` folder
  - `starter-notebook` : Data exploration and rag flow test
  - `ground-truth-data.ipynb` : Evaluation dataset generation
  - `text-search-eval.ipynb` : Retrieval evaluation of text search using misnearch and elastic search
  - `vector-minsearch-eval.ipynb` : Vector experiments using minsearch
  - `vector-eleasticsearch-eval.ipynb` : Vector experiments using elastic search
  - `rag-evaluation.ipynb` : RAG evaluation using combination vectors
  - `rag-evaluation_2.ipynb` : RAG evaluation using boosted parameters

### Retrieval Evaluation Results

#### ElasticSearch 
1. Text search (without boosting):
   - Hit rate : 91%
   - MRR : 86%

2. Text search with boosting:
   - Hit rate : 90% (slightly worse)
   - MRR : 86%

3. Vector Search with Combinations: 
         ```python

        question_answer_vector; Hit Rate: 98%, MRR: 95%
        answer_focus_vector; Hit Rate: 97%, MRR: 93%
        question_answer_focus_vector; Hit Rate: 97%, MRR: 91%
        question_vector; Hit Rate: 96%, MRR: 93%
        question_focus_vector; Hit Rate: 96%, MRR: 92%
        answer_vector; Hit Rate: 96%, MRR: 90%```

#### Minsearch
1. Text search (without boosting):
   - Hit rate : 96%
   - MRR : 92%

2. Text search with tuned boosting:
   - Hit rate : 97.7%
   - MRR : 93%

 Boosting parameters:
   ```python
   boost = {
    'question': 2.209413642492037, 
    'answer': 2.030098462268734, 
    'source': 2.6765387031145362, 
    'focus_area': 0.26081649788824846
   }
   ```

1. Vector Search with Combinations:
        ```python

        question_answer_vector; Hit Rate: 99%  MRR: 96%  
        question_answer_focus_vector; Hit Rate: 0.99%, MRR: 95%
        answer_focus_vector; Hit Rate: 99%, MRR: 93%
        answer_vector; Hit Rate: 98%, MRR: 90%
        question_vector; Hit Rate: 97%, MRR: 93%
        question_focus_vector; Hit Rate: 97%, MRR: 93%```

### RAG Flow Evaluation

Using LLM-as-a-Judge metric (sample) utilizing ```question_answer_vector```:

1. `gpt-4o-mini`:
   - RELEVANT: 88%
   - PARTLY_RELEVANT: 6%%
   - NON_RELEVANT: 6%

2. `gpt-4o`:
   - RELEVANT: 86%
   - PARTLY_RELEVANT : 8%
   - NON_RELEVANT: 6%

`gpt-4o-mini` was chosen for the final implementation.

   

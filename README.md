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

This project utilizes a subset of the MedQuAD (Medical Question Answering Dataset), a comprehensive collection of medical question-answer pairs. Key features include:

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
* Python 3.10: Core development
* Docker & Docker Compose: Containerization
* Minsearch: Full-text search
* OpenAI API: Language model integration
* Flask: API framework
* PostgreSQL: Database management
* Grafana: Monitoring and visualization
   
   
   

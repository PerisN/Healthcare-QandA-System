import json
from time import time
import openai
from openai import OpenAI
import ingest
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# OpenAI API and model configuration
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

model = SentenceTransformer(MODEL_NAME)
index = ingest.load_index()

client = openai.OpenAI()


def minsearch_search(field, query_vector):
    query = {field: query_vector.reshape(1, -1)}
    results = index.search(query_vectors=query, num_results=10)
    return results

def search(question):
    field = 'question_answer'
    query_vector = model.encode([question])
    return minsearch_search(field, query_vector)


def build_prompt(query, search_results):
    prompt_template = """
You're a healthcare assistant AI. Answer the QUESTION based on the CONTEXT provided from a health FAQ database.
Use only the facts from the CONTEXT to provide an accurate, clear, and concise answer.

QUESTION: {question}
CONTEXT: {context}

""".strip()

    context = ""
    
    for doc in search_results:
        context += f"Question: {doc['question']}\nAnswer: {doc['answer']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt, model=OPENAI_MODEL, timeout=10):
    try:
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], timeout=timeout
        )
        answer = response.choices[0].message.content
        token_stats = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return answer, token_stats
    except openai.error.OpenAIError as e:
        logging.error(f"Error with OpenAI API: {e}")
        return "Error in generating response", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


evaluation_prompt_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


def evaluate_relevance(question, answer):
    prompt = evaluation_prompt_template.format(question=question, answer=answer)
    evaluation, tokens = llm(prompt, model="gpt-4o-mini")

    try:
        json_eval = json.loads(evaluation)
        return json_eval, tokens
    except json.JSONDecodeError:
        result = {"Relevance": "UNKNOWN", "Explanation": "Failed to parse evaluation"}
        return result, tokens


def calculate_openai_cost(model, tokens):
    openai_cost = 0

    if model == "gpt-4o-mini":
        openai_cost = (
            tokens["prompt_tokens"] * 0.00015 + tokens["completion_tokens"] * 0.0006
        ) / 1000
    else:
        print("Model not recognized. OpenAI cost calculation failed.")

    return openai_cost


def rag(query, model="gpt-4o-mini"):
    logging.info(f"Running RAG for query: {query}")
    t0 = time()

    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer, token_stats = llm(prompt, model=model)

    relevance, rel_token_stats = evaluate_relevance(query, answer)

    t1 = time()
    took = t1 - t0

    openai_cost_rag = calculate_openai_cost(model, token_stats)
    openai_cost_eval = calculate_openai_cost(model, rel_token_stats)

    openai_cost = openai_cost_rag + openai_cost_eval

    answer_data = {
        "answer": answer,
        "model_used": model,
        "response_time": took,
        "relevance": relevance.get("Relevance", "UNKNOWN"),
        "relevance_explanation": relevance.get(
            "Explanation", "Failed to parse evaluation"
        ),
        "prompt_tokens": token_stats["prompt_tokens"],
        "completion_tokens": token_stats["completion_tokens"],
        "total_tokens": token_stats["total_tokens"],
        "eval_prompt_tokens": rel_token_stats["prompt_tokens"],
        "eval_completion_tokens": rel_token_stats["completion_tokens"],
        "eval_total_tokens": rel_token_stats["total_tokens"],
        "openai_cost": openai_cost,
    }

    return answer_data
logging.info("LLM response generated successfully.")

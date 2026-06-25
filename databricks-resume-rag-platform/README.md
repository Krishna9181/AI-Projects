# Databricks Resume RAG Platform

A production-direction Retrieval-Augmented Generation (RAG) project built fully inside Databricks. This project turns a resume PDF into a searchable knowledge base, retrieves relevant chunks using Databricks Vector Search, and serves grounded answers through a Databricks App chat UI backed by Databricks Foundation Model APIs.

## Project idea

This project demonstrates an end-to-end Databricks-native RAG system:

* Source document ingestion from a PDF resume
* Text extraction and quality checks in a Databricks notebook
* Semantic chunking tuned for resume-style content
* Chunk storage in a Unity Catalog Delta table
* Managed retrieval using Databricks Vector Search
* Grounded answer generation using `databricks-meta-llama-3-3-70b-instruct`
* A Streamlit-based Databricks App that acts as the user-facing chat interface

## Current implementation status

The project currently includes:

* Notebook backend in [RAG Pipeline Blueprint](../RAG%20Pipeline%20Blueprint)
* Delta table: `workspace_7474652187298449.default.rag_resume_chunks`
* Vector Search index: `workspace_7474652187298449.default.resume_index`
* Databricks App: `resume-rag-chat`
* Streamlit app source in this folder

## Architecture

```text
Resume PDF
   -> PDF extraction and validation notebook
   -> semantic chunking
   -> Unity Catalog Delta table
   -> Databricks Vector Search index
   -> retrieval of relevant chunks
   -> Llama 3.3 70B answer generation
   -> Streamlit chat UI in Databricks Apps
```

## Main project files

* `app.py` — Streamlit chat app for asking resume questions
* `app.yaml` — Databricks App runtime configuration
* `requirements.txt` — Python dependencies for the app
* `.gitignore` — common local and Python ignores
* `README.md` — project documentation

## Backend notebook flow

The backend notebook [RAG Pipeline Blueprint](../RAG%20Pipeline%20Blueprint) was developed step by step and currently covers:

1. PDF extraction from the resume file
2. Extraction quality validation
3. Resume-aware chunking strategy
4. Preparation of chunk records for embedding
5. Writing chunk records to Unity Catalog Delta
6. Enabling CDF and primary key constraints
7. Creating and testing the Vector Search index
8. Retrieval and generation workflow in notebook form
9. Refactoring into reusable RAG function logic
10. Extending the same backend idea into a Databricks App UI

## Databricks App behavior

The app does the following:

* Accepts a user question in a chat input
* Queries the Vector Search index for the most relevant chunks
* Builds a grounded context block from retrieved chunks
* Sends the question and context to the Foundation Model API
* Displays the generated answer
* Optionally displays retrieved source chunks and scores

## Required Databricks resources

To run the app successfully, the app service principal needs access to:

* Vector Search index `workspace_7474652187298449.default.resume_index`
  * permission: `Can select`
* Model serving / foundation model endpoint `databricks-meta-llama-3-3-70b-instruct`
  * permission: `Can query`

If the Vector Search resource is added through the app UI, Databricks typically handles the needed UC grants automatically when allowed by object permissions.

## App configuration

### `app.yaml`

The app is configured as a Streamlit app:

```yaml
command:
  - streamlit
  - run
  - app.py
```

It also sets:

* `VECTOR_SEARCH_INDEX`
* `SERVING_ENDPOINT`
* Streamlit headless settings

## Dependencies

Current app dependencies:

```text
streamlit
databricks-sdk
```

## How to run and deploy

### Local project editing in Databricks workspace

Edit the files in this folder and then deploy the app source path from the Databricks Apps UI or CLI.

### App deploy source path

Current deployed app source was originally created from:

```text
/Workspace/Users/saikrishnareddypoluri26@gmail.com/resume-rag-chat
```

If you want this renamed folder to become the new deployment source, redeploy the app from:

```text
/Workspace/Users/saikrishnareddypoluri26@gmail.com/AI-Projects/databricks-resume-rag-platform
```

## Suggested next improvements

* Replace hardcoded environment values with app resources and `valueFrom`
* Add citations in final answers
* Add chat history persistence
* Add evaluation with MLflow
* Add prompt templates and better answer formatting
* Add multi-document support beyond a single resume
* Add feedback buttons for answer quality
* Add automated deployment from GitHub commits

## Git workflow recommendation

This folder is meant to be the Git-tracked project home for the app layer of the RAG system.

Recommended workflow:

1. Make notebook or app improvements
2. Update files in this project folder
3. Review Git diff
4. Commit and push small changes incrementally

## Important note

This project is based on a real resume and may contain personal information. Be careful before making the repository public or sharing source documents directly.

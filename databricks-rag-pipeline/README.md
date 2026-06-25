# Databricks RAG Pipeline

A Databricks-native Retrieval-Augmented Generation (RAG) project that turns a resume PDF into a searchable knowledge base, retrieves relevant chunks with Databricks Vector Search, and serves grounded answers through a Databricks App chat UI backed by Databricks Foundation Model APIs.

## What this project covers

This repository folder captures the current end-to-end implementation of the project:

* PDF ingestion and extraction in Databricks
* Resume-aware semantic chunking
* Chunk storage in a Unity Catalog Delta table
* Managed retrieval with Databricks Vector Search
* Grounded generation with `databricks-meta-llama-3-3-70b-instruct`
* A Streamlit-based Databricks App UI for asking questions against the indexed resume

## Project assets

Current Databricks assets used by the project:

* Notebook: `RAG Pipeline Blueprint`
* Delta table: `workspace_7474652187298449.default.rag_resume_chunks`
* Vector Search index: `workspace_7474652187298449.default.resume_index`
* Databricks App: `resume-rag-chat`

## Architecture

```text
Resume PDF
   -> PDF extraction + validation notebook
   -> semantic chunking
   -> Unity Catalog Delta table
   -> Databricks Vector Search index
   -> top-k retrieval
   -> Foundation Model API generation
   -> Streamlit Databricks App chat UI
```

## Folder contents

* `app.py` — Streamlit app UI and RAG request flow
* `app.yaml` — Databricks App runtime configuration
* `requirements.txt` — app dependencies
* `.gitignore` — common Python and local ignores
* `README.md` — project documentation and setup details

## Backend notebook work completed

The notebook workflow currently includes:

1. Resume PDF extraction using `pypdf`
2. PDF quality checks
3. Sentence-aware semantic chunking tuned for resume content
4. Chunk record preparation for embedding and storage
5. Writing chunks to a Unity Catalog Delta table
6. Enabling Change Data Feed and primary key constraints
7. Creating a Databricks Vector Search index through the UI
8. Testing retrieval quality in the UI and notebook
9. Building reusable retrieval and generation notebook logic
10. Extending the same flow into a Databricks App chat interface

## App behavior

The Streamlit app does the following:

* Accepts a natural language question from the user
* Queries the Vector Search index for relevant resume chunks
* Builds a grounded context block from the retrieved chunks
* Sends the question and context to the foundation model endpoint
* Returns a concise grounded answer
* Optionally displays retrieved source chunks and scores

## Required app permissions

For the app to work, its service principal must be allowed to access both backend services.

### Vector Search

Required index:

* `workspace_7474652187298449.default.resume_index`

Required permission:

* `Can select`

### Foundation model endpoint

Required endpoint:

* `databricks-meta-llama-3-3-70b-instruct`

Required permission:

* `Can query`

If the app UI is used to add these resources, Databricks can automatically wire the corresponding environment references and grants when allowed by permissions on the underlying objects.

## App runtime configuration

The app is configured as a Streamlit app.

```yaml
command:
  - streamlit
  - run
  - app.py
```

Environment variables currently include:

* `VECTOR_SEARCH_INDEX`
* `SERVING_ENDPOINT`
* Streamlit runtime settings

## Dependencies

```text
streamlit
databricks-sdk
```

## Source and deployment paths

Current app deployment source path:

```text
/Workspace/Users/saikrishnareddypoluri26@gmail.com/AI-Projects/databricks-rag-pipeline
```

App URL:

```text
https://resume-rag-chat-7474652187298449.aws.databricksapps.com
```

## Suggested next improvements

* Replace hardcoded env values with app resources and `valueFrom`
* Add citations in the final answer
* Add chat history persistence
* Add MLflow evaluation and answer quality tracking
* Add prompt templates and better formatting
* Support multiple documents beyond a single resume
* Add GitHub-driven deployment automation
* Add user feedback buttons for answer usefulness

## Recommended workflow

1. Improve notebook or app logic
2. Update files in this folder
3. Review Git changes
4. Commit and push in small increments
5. Redeploy the app from this folder when needed

## Privacy note

This project is based on a real resume and may contain personal information. Review the content carefully before making the repository public or uploading raw source documents.

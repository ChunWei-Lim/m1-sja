# Streamlit DuckDB Recruitment Dashboard

## Expected DuckDB tables

Your DuckDB database should contain:

- `job_postings`
- `categories`
- `job_categories`

The app joins them using:

```sql
FROM job_postings AS j
INNER JOIN job_categories AS jc
    ON j.metadata_jobPostId = jc.metadata_jobPostId
INNER JOIN categories AS c
    ON jc.category_id = c.category_id
```

## Files

- `app_duckdb.py`
- `requirements_duckdb.txt`

## Run

```bash
pip install -r requirements_duckdb.txt
streamlit run app_duckdb.py
```

In the sidebar, set the DuckDB database path, for example:

```text
SGJobData.duckdb
```

or

```text
db/jobs.duckdb
```

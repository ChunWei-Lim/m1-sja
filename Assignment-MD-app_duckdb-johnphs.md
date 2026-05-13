# 6m-data-coaching-assignment-project
## Module 1 Assignment Project – Singapore Jobs Analytics
---
## 1. Business Case 

> "As an HR analyst or recruiter, I want to identify high-demand and hard-to-fill roles, so that I can benchmark salaries and prioritise recruitment efforts."

- Business Objective: Identify promising job categories and roles by comparing vacancies, average salary, experience requirements, views, and application counts. 
- Target User: HR analysts and recruiters 
- Business Value Proposition: To identify high-demand roles, benchmark salary offers, and prioritise recruitment strategies for roles with many vacancies but low application rates.

These users can use the app to answer questions such as:

- Which job categories have the highest hiring demand?
- Which roles have the most vacancies?
- Which roles offer the highest salaries?
- Which job categories require more experience?
- Which roles have many vacancies but low applications per vacancy?
- Which roles should recruiters prioritise for active sourcing?

---
## 2. Data Handling & Process (5–8 bullets)
### Software Tools Used
<table>
  <tr>
    <td align="center">
      <img src="https://cdn.simpleicons.org/numpy/013243" width="32"><br>NumPy
    </td>
    <td align="center">
      <img src="https://cdn.simpleicons.org/pandas/150458" width="32"><br>Pandas
    </td>
    <td align="center">
      <img src="https://cdn.simpleicons.org/plotly/3F4F75" width="32"><br>Plotly
    </td>
    <td align="center">
      <img src="https://cdn.simpleicons.org/duckdb/FFF000" width="32"><br>DuckDB
    </td>
    <td align="center">
      🗄️<br>DBGate
    </td>
    <td align="center">
      <img src="https://cdn.simpleicons.org/streamlit/FF4B4B" width="32"><br>Streamlit
    </td>
    <td align="center">
      <img src="https://cdn.simpleicons.org/openai/74AA9C" width="32"><br>ChatGPT
    </td>
  </tr>
</table>

### Database Design 
ERD: Entity Relationship Diagram
![alt text](image.png)

Rationale for performing normalisation:
- The column 'categories' violates first normal form. For relational analysis, each value should be atomic, not a list of values. 
- The data category 'id' is master data. The category name repeats across many job postings. It is cleaner to store each category once in a categories table.
- Dashboard app needs category-level aggregation. This becomes easier when category is a normal column in a relationship table, rather than hidden inside an array.
- Preserves multi-category jobs. Avoids creating only one category column by taking the “first category”.

### Key SQL Used
Dimension table: categories
```sql
CREATE TABLE categories (
    category_id INTEGER NOT NULL PRIMARY KEY,
    category_name VARCHAR NOT NULL
);
```
Bridging Table between job postings and categories. 
- "many-to-many"
- needed because one job posting may belong to more than one category, and one category may contain many job postings.
```sql
CREATE TABLE job_listing_categories (
    listing_id BIGINT NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (listing_id, category_id),
    FOREIGN KEY (listing_id)
        REFERENCES sg_job_data(listing_id),
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
```
The only SQL used in the app is a query
```sql
    SELECT
        j.listing_id,
        j.metadata_jobPostId,
        j.title,
        j.employmentTypes,
        j.positionLevels,
        j.postedCompany_name,
        j.metadata_newPostingDate,
        j.metadata_originalPostingDate,
        j.metadata_expiryDate,
        j.metadata_repostCount,
        j.minimumYearsExperience,
        j.numberOfVacancies,
        j.salary_minimum,
        j.salary_maximum,
        j.salary_type,
        j.average_salary,
        j.metadata_totalNumberOfView,
        j.metadata_totalNumberJobApplication,
        j.status_jobStatus,
        c.category_id,
        c.category_name
    FROM sg_job_data AS j
    INNER JOIN job_listing_categories AS jc
        ON j.listing_id = jc.listing_id
    INNER JOIN categories AS c
        ON jc.category_id = c.category_id
```
### Loading the data into the tables
```python
import duckdb

con = duckdb.connect("sgJobData.db")

con.sql("                                                           \
    CREATE TABLE sg_job_data AS                                     \
    SELECT * FROM read_csv_auto('data/SGJobData.csv', HEADER=TRUE); \
")
```
Populating the categories table
```sql
INSERT INTO categories (category_id, category_name)
SELECT DISTINCT
    CAST(json_extract_string(cat.value, '$.id') AS INTEGER) AS category_id,
    json_extract_string(cat.value, '$.category') AS category_name
FROM sg_job_data j,
     json_each(j.categories::JSON) AS cat
ORDER BY category_id;
```
Populating the job-category relationships
```sql
INSERT INTO job_listing_categories (listing_id, category_id) 
SELECT DISTINCT
    j.listing_id,
    CAST(json_extract_string(cat.value, '$.id') AS INTEGER) AS category_id
FROM sg_job_data j, 
    json_each(j.categories::JSON) AS cat;
```
---
## 3. Dashboard / App (6–10 bullets)
### Filter controls
- 1
- 2
...

Describe and demonstrate your solution:

- Type of solution: dashboard (e.g. Streamlit, Power BI, Tableau) or simple web app.
- Main views:
  - Overview metrics (e.g. total postings, top roles/industries, salary ranges).
  - Drill-down view (by role, industry, location, skills, etc.).
  - Time trend view (e.g. postings over time, salary trends).
- Interactivity: filters, sorting, drill-downs, tooltips where relevant.
- Design choices: layout, chart types, colour scheme, readability.
- How each view directly supports your business objective and target users.

Include 2–4 key screenshots in your written submission (or show live in the presentation).

---
## 4. Presentation (10 mins per team)

Suggested flow:

1. **Business case & objective** (2–3 mins)  
   - Scenario, users, objective, success criteria.
2. **Process & data handling** (3–4 mins)  
   - How you cleaned, transformed, and explored the data.
3. **Dashboard / app walkthrough** (3–4 mins)  
   - Main views, interactions, and how they answer the business question.
4. **Challenges & learnings** (1–2 mins)  
   - Technical/analytical challenges, what you learned, and possible next steps.

---
## Challenges & learnings

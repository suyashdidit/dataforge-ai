SQL_EXPLAIN_PROMPT = """
You are a senior data engineer.

Explain the following SQL query.

Also provide:

1. Purpose
2. Tables involved
3. Performance concerns
4. Optimization suggestions
5. Plain English summary

SQL:

{sql}
"""
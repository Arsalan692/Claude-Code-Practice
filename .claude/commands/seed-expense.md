---
description: Seed dummy expenses for a specific user

argument-hint: "<user-id> <count> <month>"

allowed-tools: Read, Bash(python:*)

---

User input: $ARGUMENTS

Read the database table of expense and understand how the schema looks like

1. Extract these from the arguments: user-id(integer), count(number of expenses to create), months(how many past months to spread across them)
Validate the arguments, in case of missing or wrong argument stop there and through an error message
example: /seed-expense 1 5 10

2. Create the all the expenses for the specific user id in the expenses table, Note: ensure no violation of schema or rules should be made  
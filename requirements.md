## Requirements

I am building an app called Customer Feedback Sentiment Reporter with the following requirements - 


1. Reads a CSV of customer feedback (feedback_id, text, rating) 
-- Do not need to store the data, calculate on the fly
-- the input file format is consistent
-- For now do not worry about file size

2. Computes how many are positive, neutral, or negative based on rating.
-- For computing the reviews, Count ratings >=4 (positive), 3 (neutral), <3 (negative).

3. Sends sample feedback snippets to OpenAI to summarize themes and top 2 improvement suggestions.
-- “Given 50% positive, 25% neutral, 25% negative — summarize key themes and recommend two actions.”

Example Input (feedback.csv)
    ```
    feedback_id,text,rating
    1,"Love the interface, but app crashes sometimes.",4
    2,"Very slow response time and confusing error messages.",2
    3,"Smooth login and dashboard experience.",5
    ```

Write a PRD for a MVP version of the app that I am going to vibe code using openAI codex.

We should think through the following questions:
    1. What is the app
    2. What do I use the app for
    3. What are the patterns behind the app?
    4. How do I make the app most useful for target audience?

## The PRD should contain the following information - 
1. Project Overview: 
   <a brief overview of the project> 

2. Skills Required: 
    1. Python Metrics Json Data Processing 
    2. OpenAI APIs 
    3. UI development using noje js or any other FE framework. 

3. Key Features:
    <write the key features based on above requirements>

4. End Users:
    <Define the end users here>

### Please remember these points - 
1. Use OPENAI Chat Completions and not the newer Responses API
2. Do not use REST, instead USE Python openai package 
3. Use python dotenv to load secrets from a .env file
4. Add a readme to run the steps

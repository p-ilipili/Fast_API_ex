import pandas as pd
import secrets
from fastapi import FastAPI, HTTPException, Depends, Header, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional, List
from typing_extensions import Annotated
import numpy as np

# import questions
dfq = pd.read_csv('questions.csv', sep=',')
# drop questions where mandatory information is missing
dfq = dfq.dropna(subset=['question', 'subject', 'use', 'correct', 'responseA', 'responseB', 'responseC'])
#print(dfq.head(10))

#declare API
api = FastAPI(
    title = "Qui veut gagner de l\'argent en masse",
    description = "QCM",
)

# API Healthcheck
@api.get('/hc', name="API Healthcheck")
def get_hc():
    """Check the status of the API
    """
    return {"The API is running fine"}

# credentials
users_db = [
    {
        'user_id': 1,
        'name': 'alice',
        'password': 'wonderland'
    },
    {
        'user_id': 2,
        'name': 'bob',
        'password': 'builder'
    },
    {
        'user_id': 3,
        'name': 'clementine',
        'password': 'mandarine'
    },
    {
        'user_id': 0,
        'name': 'admin',
        'password': '4dm1N'
    }
]

# get unique/distinct categories and types
mcq_categories = dfq["subject"].unique()
mcq_types = dfq["use"].unique()

# Security
security = HTTPBasic()

def authenticate_user(username: str, password: str) -> dict | None:
    """
    Authenticate the user based on the username and password.
    Returns the user dictionary if valid, otherwise None.
    """
    for user in users_db:
        if (
            secrets.compare_digest(user["name"], username)
            and secrets.compare_digest(user["password"], password)
        ):
            return user
    return None


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """
    Validate the provided username and password using the user database.
    """
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

# use BaseModel for simplified code
class Qstn(BaseModel):
    question: str
    subject : str
    use: str
    correct : List[str]
    responseA : str
    responseB : str
    responseC : str
    responseD : Optional[str] = None
    remark: Optional[str] = None


# add a question
@api.post('/add-question', name="Add a question")
def post_question(current_user: Annotated[dict, Depends(get_current_user)],qstn:Qstn):
    """
        Use this endpoint to add a question.
        This needs admin rights.

        Use the following structure, responseD and remark are optional:
        {
            "question": "What is the capital of France?",
            "subject": "Geography",
            "use": "General Knowledge",
            "correct": ["C","D"],
            "responseA": "Quebec",
            "responseB": "London",
            "responseC": "Berlin",
            "responseD": "La reponse D",
            "remark": "incorrect answers"
        }
    """
    if current_user["name"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admins only",
        )
    print(qstn)
    # Convert the 'correct' list to a comma-separated string
    try:
        qstn_clean = qstn.model_dump()
        qstn_clean['correct'] = ','.join(qstn_clean['correct'])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error processing question data: {e}")
    print(qstn_clean)

    global dfq
    dfq = pd.concat([dfq, pd.DataFrame([qstn_clean])], ignore_index=True)
    dfq.to_csv("questions.csv", index=False)

    return {f"The question {qstn.model_dump()} has been added"}


# get questions
@api.get('/mcq', name="Get the MCQ list")
def get_questions(current_user: Annotated[dict, Depends(get_current_user)], nb_qst: int, q_type: str, q_category: str = Query(...)):
    global dfq
    # limit questions to 5,10 or 20
    if nb_qst not in [5, 10, 20]:
        raise HTTPException(status_code=400, detail="Invalid number of questions. Choose from 5, 10, or 20.")
    
    # Split the category string into a list by commas
    categories = [category.strip() for category in q_category.split(',')]

    
    print(f"Received categories: {q_category}") 

    filtered_questions = dfq[
        (dfq['use'] == q_type) & (dfq['subject'].isin(categories))
    ]

    """
        Get 5,10 or 20 questions.
        Provide the desired number of questions, types and categories amongst the following:
        Categories :
        ['BDD' 'Systèmes distribués' 'Streaming de données' 'Docker'
        'Classification' 'Sytèmes distribués' 'Data Science' 'Machine Learning' 'Automation']

        Types:
        ['Test de positionnement' 'Test de validation' 'Total Bootcamp']
    """

    if filtered_questions.empty:
        raise HTTPException(status_code=404, detail=f"No questions found for the given criteria. Use a category from this list : {dfq["subject"].unique()} and a type from this list : {dfq["use"].unique()}.")

    random_questions = filtered_questions.sample(n=min(nb_qst, len(filtered_questions))).to_dict(orient="records")
    rand_qst = pd.DataFrame(random_questions)

    # Replace NaN values in the list of questions with None because JSON throws errors for empty columns
    random_questions_clean = [
        {key: (None if isinstance(value, float) and np.isnan(value) else value) for key, value in question.items()}
        for question in random_questions
    ]

    rand_qst.to_csv("new_mcq.csv", sep=';',index=False)
    return {"message": "Your MCQ has been created with the following questions and have been inserted in the new_mcq.csv file", "questions": random_questions_clean}
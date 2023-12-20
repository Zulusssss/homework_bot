# Bot Assistant

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/-pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)

## Bot Features:
- Once every 10 minutes, it polls the API of the Practicum service and checks the status of the homework submitted for review.
- When updating the status, the API analyzes the response and sends you a corresponding notification in Telegram.
- Logs his work and informs you about important problems with a message in Telegram.

## Description

The telegram bot accesses the "Practicum" API service.Homework and finds out the status of homework: whether the homework was taken in the review, whether it was checked, and if it was checked, then the reviewer accepted it or returned it for revision.

An example of an assistant bot's response:

```python
{
   "homeworks":[
      {
         "id":123,
         "status":"approved",
         "homework_name":"user__homework_bot-master.zip",
         "reviewer_comment":"all right",
         "date_updated":"2021-12-14T14:40:57Z",
         "lesson_name":"name"
      }
   ],
   "current_date":1581804979
}
```

## Installation

1. Clone a repository:

    ```python
    git clone git@github.com:Zulusssss/homework_bot.git
    ```

2. Go to the project folder:

    ```python
    cd homework_bot/
    ```

3. Install a virtual environment for the project:

    ```python
    python -m venv venv
    ```

4. Activate the virtual environment for the project:

    ```python
    # for OS Linux and macOS
    source venv/bin/activate

    # for Windows OS
    source venv/Scripts/activate
    ```

5. Install dependencies:

    ```python
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

6. Perform migrations at the project level:

    ```python
    cd yatube
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

7. Register a chatbot in Telegram

8. Create a file in the root directory .env for storing environment variables

    ```python
    PRAKTIKUM_TOKEN = 'xxx'
    TELEGRAM_TOKEN = 'xxx'
    TELEGRAM_CHAT_ID = 'xxx'
    ```

9. Run the project locally:

    ```python
    # for OS Linux and macOS
    python homework_bot.py

    # for Windows OS
    python3 homework_bot.py
    ```

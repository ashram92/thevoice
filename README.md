# README

## Technology Used

- Python 3.5
- Sqlite (I selected this so that we don't need to really configure postgres/mysql etc.)
- Django Rest Framework
- ReactJS

## Data Modelling

- I tried to make the modelling as simple as possible, using the inbuilt auth system to 
represent any users who can log into the system - Admins and Mentors
- Every Candidate can only belong in 1 Team who has a Mentor
- Every Candidate can have multiple Activities, which can be scored by 0-n 
Mentors (but only once per mentor/activity combination)
- Averaging and scoring is done on the fly since averages are just a transformation of raw Activity Scores.


## Design Choices

- I decided to use Django Session Auth to reduce complexity. If I was to
build a SPA, I would most likely consider JWT or some sort of token
based auth system.
- I implemented 4 endpoints:
    - Login
    - Logout 
    - Profile - to get current logged in user profile
    - Teams - get retrievable teams for the current user (Admins can retireve all, while Mentors can only retrieve Teams they mentor)
- I try keep all business logic in `api.py` files to keep the models thin.
- I have not really used frontend technology, so I decided to learn React and implement the 
front end in it since it had the easiest learning curve.
- I have not really done browser routing (ReactRouter), but this would be expected in a 
production ready app. 

## Running the application

1. Have python 3.4+ running on system.
2. Create a virtualenv, activiate it, run `pip install -r requirements.txt`
3. Run `rebuild_db.sh` to make a fresh copy of the database
4. Run `python manage.py runserver` and `yarn start` on two terminals.
5. Go to `127.0.0.1:3000`
6. Login Details (Name: Username | Password)
    - Admin: admin | pass123word
    - Bob: Bob | bobbrown
    - Laura: Laura | lauramitchell
    - Steve: Steve | steveclarke


## Things still TODO:

- Unit testing backend/frontend
- Clean up frontend code
- Better error handling and UI/UX for frontend
- Compile frontend and add to django's static to be served via django


## Closing Thoughts:

This task was not challenging from a backend perspective. I did have to learn a frontend
stack to implement the SPA. React seemed quite intuitive, but it did take me
a good amount of hours to understand the data flow using components and the 
React Lifycycle. I have run out of time to really put the finishing touches on 
this solution, but I have listed what I would do in the future to improve the solution
above.

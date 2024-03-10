# Finance Tracker

## App live [here](https://finance-tracker-oboq.onrender.com)

## User stories:

1. ### User has to log in/sign up when they open the application
   1. Setup Log in and Sign up - DONE
   2. Setup CSRF tokens for security - DONE
   3. Setup Authentication - User Flask-Login (didn't use Next because of its unpredicted behaviour)
   4. UI using tailwind CSS - DONE
   5. Salted password - TBD
   6. JWT - TBD
   7. Forgot Password - Add as another user story
   
   ### Screenshots
![Login Page (Web)](https://github.com/elams18/Finance-Tracker/blob/218149289535c76f9319c95404a5c48076292fa2/screenshots/Screenshot%202024-02-11%20at%2010.06.17%E2%80%AFPM.png)
![Login Page (Mobile)](https://github.com/elams18/Finance-Tracker/blob/218149289535c76f9319c95404a5c48076292fa2/screenshots/Screenshot%202024-02-11%20at%2010.06.27%E2%80%AFPM.png)
![Register Page (Web)](https://github.com/elams18/Finance-Tracker/blob/218149289535c76f9319c95404a5c48076292fa2/screenshots/Screenshot%202024-02-11%20at%2010.06.39%E2%80%AFPM.png)
![Register Page (Mobile)](https://github.com/elams18/Finance-Tracker/blob/218149289535c76f9319c95404a5c48076292fa2/screenshots/Screenshot%202024-02-11%20at%2010.06.47%E2%80%AFPM.png)

2. ### User has to create a timesheet with expense
   1. Create expense model with many to one mapping with user
   2. Create POST API to add expense with user ID

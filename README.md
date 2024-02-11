# Finance Tracker

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
![Screenshot 2024-02-11 at 9.56.44 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fpq%2Fg0c0pc095ls90sy9bwb8g2ww0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_aP9nhq%2FScreenshot%202024-02-11%20at%209.56.44%E2%80%AFPM.png)
![Screenshot 2024-02-11 at 9.57.03 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fpq%2Fg0c0pc095ls90sy9bwb8g2ww0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_r1JeVy%2FScreenshot%202024-02-11%20at%209.57.03%E2%80%AFPM.png)
![Screenshot 2024-02-11 at 9.57.33 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fpq%2Fg0c0pc095ls90sy9bwb8g2ww0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_SefDZt%2FScreenshot%202024-02-11%20at%209.57.33%E2%80%AFPM.png)
![Screenshot 2024-02-11 at 9.58.15 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fpq%2Fg0c0pc095ls90sy9bwb8g2ww0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_qjUhhg%2FScreenshot%202024-02-11%20at%209.58.15%E2%80%AFPM.png)

2. ### User has to create a timesheet with expense
   1. Create expense model with many to one mapping with user
   2. Create POST API to add expense with user ID
# Code York App

Website to help teach kids programming in Python.

Does the following:

* Lesson materials and external links students can go to
* Assignments, students enter code into a client editor
    * Editor for each assignment, can run in client, send Ajax message
      back to account to 
* Student accounts
    * Email addresses of students
    * Shows which assignments have been completed / not completed
    * Deadlines of assignments
* Sends email notifications to admin when:
    * Due date of assignment arrives
        * List of users who have completed it on time
        * List of users who have attempted it but failed
        * List of users who made no attempt
    * User completes assignment for first time (after due date)
    * Server side error happens
* Sends email notifications to student when:
    * Assignment is soon but still not finished
    * Assignment has passed and hasn't been finished
        * If user tried assignment but failed, says admin will check
    * New assignment has been issued

Has the following pages:

* Homepage
    * Summary of site
    * Links to all other pages
* Lessons and Links
    * List of every lesson
        * Each lesson's page = text w/ coding examples
    * List of external links
* Login / sign up
    * Two forms, one for login and one to sign up
    * First/last name, email, password
    * Should send verification email to address
* 'My account' page
    * Profile picture, name, email address, password
    * Assignments completed / due
* Assignment programming page (rip off codecademy as much as possible lmao)
    * Assignment in text on left, Ace editor in middle/right (most of screen)
    * Test/Submit buttons at bottom, results screen at top-right
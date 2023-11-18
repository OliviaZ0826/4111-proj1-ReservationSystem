# 4111-proj1-ReservationSystem (Hospital Reservation System)

### Contributers: Lanyue Zhang, Zining Yin

### URL of the app:?????

This repository contains a simple web server example developed for Columbia University's COMS W4111.001 Introduction to Databases course. The web server is built using Flask, a Python web framework, and it demonstrates basic interactions with a PostgreSQL database.

## Our original proposal in Part 1:

Patient Interaction:
Patients will first register a user account for the reservation system. During this registration process, they will provide personal details such as their name, date of birth, email, pertinent medical history and insurance. Then patients will get their unique patient id. After that, patients can search for doctors based on department, specialty and proceed to schedule appointments according to their preferences. Furthermore, patients can keep track of their appointments, with access to comprehensive details, including the doctor's name, available appointment time, and status.
During the payment process, patients are allowed to make payments through the platform linked with their insurance information conveniently.

Doctor Interaction:
Doctors are able to visualize their schedules and patient appointments in a dashboard after login. This feature ensures that they remain organized and informed about their clinical commitments. In addition, doctors also have access to comprehensive patient information, including medical records and insurance details, enabling them to provide personalized care.

## The parts we are achieved in Part 3:

Patient Interaction:
Patients will first register a user account for the reservation system. During this registration process, they will provide personal details such as their name, date of birth, email, pertinent medical history and insurance. Then patients will get their unique patient id. After that, patients can search for doctors based on department, specialty and proceed to schedule appointments according to their preferences. Furthermore, patients can keep track of their appointments, with access to comprehensive details, including the doctor's name, available appointment time, and status.

Doctor Interaction:
Doctors are able to visualize their schedules and patient appointments in a dashboard after login. This feature ensures that they remain organized and informed about their clinical commitments. In addition, doctors also have access to comprehensive patient information, including medical records and insurance details, enabling them to provide personalized care.


## The parts that we choose not to use in Part 3:

Patient Interaction: During the payment process, patients are allowed to make payments through the platform linked with their insurance information conveniently. Also, we do not include pertinent medical history because those information should be asked during the appointment time and sometimes it is private to the patient so that we decide not to include in our patient profile.
Doctor Interaction: None.


## Reason: 

For patient, we find it hard to implement payment through the platform which is not a part of our course's focus.

## The parts that are not a part of our original proposal: 

Doctor can modify the payment ammount for the patient while patient can only see the deadline of pay the payment and payment ammount. 

## Two chosen web pages that are the most interesting in Part 3:

### 1 Patient dashboard
The Patient Dashboard is designed to provide patients with a user-friendly interface to view their personal information, insurance details, upcoming payments, and appointment information. 

Display Patient Information: 
      Patient-specific information is retrieved from the database and dynamically displayed on the page. Information such as patient name, ID, date of birth, and email is presented.
Insurance Information:
      The page lists insurance details retrieved from the database, including Insurance ID, provider, and coverage details. Patients can add new insurance information through a form, and the input is used to update the database.
Payments Due:
      Upcoming payment details are fetched from the database and displayed. No direct database operations are performed on this page.
Appointments:
      Appointment information is retrieved from the database and displayed in a table format. Patients can book new appointments through a form, and the form inputs are used to update the database.

### 2 Doctor dashboard
The Doctor Dashboard is intended for doctors to manage their profile, view upcoming appointments, and handle patient payment information.

Display Doctor Information:
      Doctor-specific details are retrieved from the database and displayed, including the doctor's name, specialty, ID, user ID, and email.
Appointments:
      Upcoming appointments with patient details are fetched from the database and displayed in a table. No direct database operations are performed on this page.
Patient Payments:**
      Payment information for patients is retrieved from the database and presented in a table. Doctors can add new payment information through a form, and the form inputs are used to update the database.


## Usage of the AI tools in Part 3:

Basically, we are using Chatgpt for generating python syntax of the overall project. We also use Chatgpt to generate basic UI elements like checkboxes, menus, or radio buttons to interact with the database. 







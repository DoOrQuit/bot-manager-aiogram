Bot Manager (Aiogram)

This bot utilizes Django server API to make a calls.

Base functionality :

1) Register a new user;
2) Booking for a nail master session using Google Calendar API;


Quickstart:

1) Clone this repository;
2) Install all dependencies from a requirements.txt;
3) Create Google Developer account (if hasn't done it yet);
4) Register a new service email for test and get service_mail.json file for Your personal mail;
5) Get Your calendar ID and insert it in place where GoogleCalendar instance creates (bot/handlers/event_booking_handler);
6) Install Django server to create a User(must have a model with email and password fields) instance utilizing API calls or use a ready-to-use server I've created and kept in repos;
-- Keep a log of any SQL queries you execute as you solve the mystery.

--Find crime scene description.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

--Find more information about the interviews
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

--Find what transactions were made on the day of the crime
SELECT account_number,transaction_type,amount,atm_location FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street';

--Find out more about the atm accounts et1
SELECT * from people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));

--Find information about people coming in and out of bakery
SELECT activity, minute, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

--Find the people that withdrew money and were at the scene of the crime. ET2
SELECT * from people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);

--Find more information about the calls that were made on the day of the crime
SELECT caller, receiver FROM phone_calls WHERE duration < 60 AND year = 2021 AND month = 7 AND day = 28;

--narrow down suspects
SELECT * from people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
AND phone_number IN (SELECT caller FROM phone_calls WHERE duration < 60 AND year = 2021 AND month = 7 AND day = 28);

--get flight info
SELECT * FROM flights WHERE year = 2021 AND day = 29 AND month = 7;

--get passenger info
SELECT passport_number from passengers WHERE flight_id = (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1);


--narrow down suspets
SELECT * from people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN
(SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
AND phone_number IN (SELECT caller FROM phone_calls WHERE duration < 60 AND year = 2021 AND month = 7 AND day = 28)
AND passport_number IN (SELECT passport_number from passengers WHERE flight_id = (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1));

## Description
This app will enable its user to import data about users from the given scv file into Django model and write the contents in the database using built-in Django admin.

Also, the description of API requests needed to get the list of all users and users filtered by date

## Technologies
* Python (3.7.0)
* Django (2.1.1)


## Installation
Install requirement project's packages
```
pip install -r requirements.txt
```

## API 

In order to get the list of all users imported from csv file in JSON format:

* **URL**

  <_localhost:8000/api/users/_> or   <_127.0.0.1::8000/api/users/_>

* **Method:**
  
  `GET`

* **Success Response:**

  * **Code:** 200 <br />
  * **Content:** [{"First Name": "TestName1", "Last Name": "TestSurname1", "Birth Date": "2000-02-04", "Registration date": "2018-05-09", "Order": null}, {"First Name": "TestName2", "Last Name": "TestSurname2", "Birth Date": "2000-02-05", "Registration date": "2018-05-10", "Order": null}, {"First Name": "TestName3", "Last Name": "TestSurname3", "Birth Date": "2000-02-06", "Registration date": "2018-05-11", "Order": null}, {"First Name": "TestName4", "Last Name": "TestSurname4", "Birth Date": "2000-02-07", "Registration date": "2018-05-12", "Order": null}, {"First Name": "TestName5", "Last Name": "TestSurname5", "Birth Date": "2000-02-08", "Registration date": "2018-05-13", "Order": null}, {"First Name": "TestName6", "Last Name": "TestSurname6", "Birth Date": "2000-02-09", "Registration date": "2018-05-14", "Order": null}, {"First Name": "TestName7", "Last Name": "TestSurname7", "Birth Date": "2000-02-10", "Registration date": "2018-05-15", "Order": null}, {"First Name": "TestName8", "Last Name": "TestSurname8", "Birth Date": "2000-02-11", "Registration date": "2018-05-16", "Order": null}, {"First Name": "TestName9", "Last Name": "TestSurname9", "Birth Date": "2000-02-12", "Registration date": "2018-05-17", "Order": null}, {"First Name": "TestName10", "Last Name": "TestSurname10", "Birth Date": "2000-02-13", "Registration date": "2018-05-18", "Order": null}, {"First Name": "TestName11", "Last Name": "TestSurname11", "Birth Date": "2000-02-14", "Registration date": "2018-05-19", "Order": null}, {"First Name": "TestName12", "Last Name": "TestSurname12", "Birth Date": "2000-02-15", "Registration date": "2018-05-20", "Order": null}, {"First Name": "TestName13", "Last Name": "TestSurname13", "Birth Date": "2000-02-16", "Registration date": "2018-05-21", "Order": null}, {"First Name": "TestName14", "Last Name": "TestSurname14", "Birth Date": "2000-02-17", "Registration date": "2018-05-22", "Order": null}, {"First Name": "TestName15", "Last Name": "TestSurname15", "Birth Date": "2000-02-18", "Registration date": "2018-05-23", "Order": null}, {"First Name": "TestName16", "Last Name": "TestSurname16", "Birth Date": "2000-02-19", "Registration date": "2018-05-24", "Order": null}, {"First Name": "TestName17", "Last Name": "TestSurname17", "Birth Date": "2000-02-20", "Registration date": "2018-05-25", "Order": null}, {"First Name": "TestName18", "Last Name": "TestSurname18", "Birth Date": "2000-02-21", "Registration date": "2018-05-26", "Order": null}, {"First Name": "TestName19", "Last Name": "TestSurname19", "Birth Date": "2000-02-22", "Registration date": "2018-05-27", "Order": null}, {"First Name": "TestName20", "Last Name": "TestSurname20", "Birth Date": "2000-02-23", "Registration date": "2018-05-28", "Order": null}] <br />


 
In order to get the list of users filtered by their registration date:

* **URL**

  <_127.0.0.1:8000/api/users/registered/[year]/[month]/[day]/_>

Here the keyword arguments year, month day must be replaced with the necessary year, month and day of user's registration. All the arguments are required!

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"First Name": "TestName6", "Last Name": "TestSurname6", "Birth Date": "2000-02-09", "Registration date": "2018-05-14", "Order": null}]`

  * **Code:** 204 <br />
    **Content:** `{"success": "no users found"}`
 

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "no such user" }`

  


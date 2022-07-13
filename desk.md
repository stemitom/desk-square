
# Desk Square

API for an event management tool (ex. Meetup and EvenBrite) written in drf django.

<!--- If we have only one group/collection, then no need for the "ungrouped" heading -->


## Variables

| Key | Value | Type |
| --- | ------|-------------|
| access |  |  |
| refresh |  |  |
| baseurl | http://localhost:8000 |  |



## Endpoints

* [Authentication](#authentication)
    1. [Sign Up](#1-sign-up)
        * [Sign Up](#i-example-request-sign-up)
    1. [Log In](#2-log-in)
        * [Log In](#i-example-request-log-in)
    1. [Log Out](#3-log-out)
        * [Log Out](#i-example-request-log-out)
    1. [Request Account Activation](#4-request-account-activation)
        * [Request Account Activation](#i-example-request-request-account-activation)
    1. [Activate Account](#5-activate-account)
        * [Activate Account](#i-example-request-activate-account)
    1. [Change Password](#6-change-password)
        * [Change Password](#i-example-request-change-password)
    1. [Request Password Reset](#7-request-password-reset)
        * [Request Password Reset](#i-example-request-request-password-reset)
    1. [Password Reset](#8-password-reset)
* [Organizer](#organizer)
    1. [Create Event](#1-create-event)
        * [Create Event](#i-example-request-create-event)
    1. [List Events](#2-list-events)
        * [List Events](#i-example-request-list-events)
    1. [Retrieve Event](#3-retrieve-event)
        * [Retrieve Event](#i-example-request-retrieve-event)
    1. [Delete Event](#4-delete-event)
        * [Delete Event](#i-example-request-delete-event)
* [Users](#users)
    1. [Event](#1-event)
    1. [ME](#2-me)
        * [ME](#i-example-request-me)

--------



## Authentication



### 1. Sign Up



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{user}}/registration
```



***Body:***

```js        
{
    "username": "testuser",
    "email": "testuser@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password1": "testpass",
    "password2": "testpass",
    "prefix": "Mr.",
    "phone_number": "+2349032419608",
    "job_title": "Student",
    "company": "Wasp IX",
    "website": "https://stemitom.github.io",
    "blog": "https://stemitom.github.io/blog",
    "country": "NG",
    "postal_code": "200106"
}
```



***More example Requests/Responses:***


#### I. Example Request: Sign Up



***Body:***

```js        
{
    "username": "testuser2",
    "email": "testuser2@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password1": "testpass",
    "password2": "testpass",
    "prefix": "Mr.",
    "phone_number": "+2349032419608",
    "job_title": "Student",
    "company": "Wasp IX",
    "website": "https://stemitom.github.io",
    "blog": "https://stemitom.github.io/blog",
    "country": "NG",
    "postal_code": "200106"
}
```



#### I. Example Response: Sign Up
```js
{
    "id": 3,
    "username": "testuser2",
    "email": "testuser2@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "prefix": "Mr.",
    "phone_number": "+2349032419608",
    "job_title": "Student",
    "company": "Wasp IX",
    "website": "https://stemitom.github.io",
    "blog": "https://stemitom.github.io/blog",
    "country": "NG",
    "postal_code": 200106,
    "is_email_verified": false,
    "email_verified_at": null,
    "created_at": "2022-07-13T00:00:39.148020Z",
    "updated_at": "2022-07-13T00:00:39.148021Z"
}
```


***Status Code:*** 201

<br>



### 2. Log In



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{user}}/login
```



***Body:***

```js        
{
    "email": "testuser@gmail.com",
    "password": "testpass"
}
```



***More example Requests/Responses:***


#### I. Example Request: Log In



***Body:***

```js        
{
    "email": "testuser@gmail.com",
    "password": "testpass"
}
```



#### I. Example Response: Log In
```js
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1Nzc1NjUzNywiaWF0IjoxNjU3NjcwMTM3LCJqdGkiOiIxY2NhNzI1YjI5NjM0ZDU3YmJiNDRkZjQ5YThiY2YyMyIsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoidGVzdHVzZXIiLCJlbWFpbCI6InRlc3R1c2VyQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJUZXN0IiwibGFzdF9uYW1lIjoiVXNlciIsInByZWZpeCI6Ik1yLiIsInBob25lX251bWJlciI6IisyMzQ5MDMyNDE5NjA4Iiwiam9iX3RpdGxlIjoiU3R1ZGVudCIsImNvbXBhbnkiOiJXYXNwIElYIiwid2Vic2l0ZSI6Imh0dHBzOi8vc3RlbWl0b20uZ2l0aHViLmlvIiwiYmxvZyI6Imh0dHBzOi8vc3RlbWl0b20uZ2l0aHViLmlvL2Jsb2ciLCJjb3VudHJ5IjoiTkciLCJwb3N0YWxfY29kZSI6MjAwMTA2LCJpc19lbWFpbF92ZXJpZmllZCI6ZmFsc2UsImVtYWlsX3ZlcmlmaWVkX2F0IjpudWxsLCJjcmVhdGVkX2F0IjoiMjAyMi0wNy0xMlQxNzozMzoyNy4wODczMjVaIiwidXBkYXRlZF9hdCI6IjIwMjItMDctMTJUMTc6MzM6MjcuMDg3MzI2WiJ9.BGjJA1smf1GvC8zvlKU1FoAvzDgh_J47ab4YxPNvg4Q",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NjczNzM3LCJpYXQiOjE2NTc2NzAxMzcsImp0aSI6ImQ1ZTM1ODAwMGRiMzQ3Yzg5N2FmZDM1MTg3YzEwMjgzIiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJ0ZXN0dXNlciIsImVtYWlsIjoidGVzdHVzZXJAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IlRlc3QiLCJsYXN0X25hbWUiOiJVc2VyIiwicHJlZml4IjoiTXIuIiwicGhvbmVfbnVtYmVyIjoiKzIzNDkwMzI0MTk2MDgiLCJqb2JfdGl0bGUiOiJTdHVkZW50IiwiY29tcGFueSI6Ildhc3AgSVgiLCJ3ZWJzaXRlIjoiaHR0cHM6Ly9zdGVtaXRvbS5naXRodWIuaW8iLCJibG9nIjoiaHR0cHM6Ly9zdGVtaXRvbS5naXRodWIuaW8vYmxvZyIsImNvdW50cnkiOiJORyIsInBvc3RhbF9jb2RlIjoyMDAxMDYsImlzX2VtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZW1haWxfdmVyaWZpZWRfYXQiOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIyLTA3LTEyVDE3OjMzOjI3LjA4NzMyNVoiLCJ1cGRhdGVkX2F0IjoiMjAyMi0wNy0xMlQxNzozMzoyNy4wODczMjZaIn0.6n4ajF1XAfgjaBYaG7zWrRJ5NRxgnFXneHrJw2_Vuic"
}
```


***Status Code:*** 200

<br>



### 3. Log Out



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{user}}/logout
```



***Body:***

```js        
{
    "refresh": "{{refresh}}",
    "access": "{{access}}"
}
```



***More example Requests/Responses:***


#### I. Example Request: Log Out



***Body:***

```js        
{
    "refresh": "{{refresh}}",
    "access": "{{access}}"
}
```



***Status Code:*** 204

<br>



### 4. Request Account Activation



***Endpoint:***

```bash
Method: GET
Type: 
URL: {{user}}/request-activation
```



***More example Requests/Responses:***


#### I. Example Request: Request Account Activation



***Body: None***



#### I. Example Response: Request Account Activation
```js
{
    "message": "Email verification sent to email! Check your email and use the link to verify your account"
}
```


***Status Code:*** 200

<br>



### 5. Activate Account



***Endpoint:***

```bash
Method: GET
Type: 
URL: {{user}}/activate/Mg/b8h3tq-c3e56c358b1e42970abab3a2449a8391
```



***More example Requests/Responses:***


#### I. Example Request: Activate Account



***Body: None***



#### I. Example Response: Activate Account
```js
{
    "message": "Your account has been activated sucessfully!"
}
```


***Status Code:*** 200

<br>



### 6. Change Password



***Endpoint:***

```bash
Method: PUT
Type: RAW
URL: {{user}}/change-password
```



***Body:***

```js        
{
    "old_pw":"testpass",
    "new_pw": "YUrgANXNDXzq",
    "new_pw_conf": "YUrgANXNDXzq"
}
```



***More example Requests/Responses:***


#### I. Example Request: Change Password



***Body:***

```js        
{
    "old_pw":"testpass",
    "new_pw": "YUrgANXNDXzq",
    "new_pw_conf": "YUrgANXNDXzq"
}
```



#### I. Example Response: Change Password
```js
{}
```


***Status Code:*** 200

<br>



### 7. Request Password Reset



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{user}}/request-password-reset
```



***Body:***

```js        
{
    "email":"loverly@gmail.com"
}
```



***More example Requests/Responses:***


#### I. Example Request: Request Password Reset



***Body:***

```js        
{
    "email":"loverly@gmail.com"
}
```



#### I. Example Response: Request Password Reset
```js
{
    "message": "Please do check your email for further instructions!"
}
```


***Status Code:*** 200

<br>



### 8. Password Reset



***Endpoint:***

```bash
Method: GET
Type: 
URL: 
```



## Organizer



### 1. Create Event



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{event}}/
```



***Body:***

```js        
{
    "title": "Django Meetup - Osun Branch",
    "summary": "APIs in Django",
    "description": "Let's discuss the detailed aspects of DRF and its wonders",
    "url": "https://www.django-rest-framework.org/api-guide/serializers/#modelserializer",
    "category": "Technology",
    "event_type": "Conference",
    "timing_type": "Recurring",
    "tz": "Africa/Lagos",
    "tags": [
        "api", "drf", "backend"
    ],
    "location": {
        "location_type": "Venue",
        "location": "11th Redmond, CA",
        "conference_uri": "https://meet.google.com",
        "lat": "38.4267861",
        "long": "-192.0806032",
        "state": "Osun",
        "country": "NG"
    },
    "tickets": [
        {
            "name": "Ticket #1",
            "description": "VIP Ticket",
            "quantity_available": "100",
            "unit_price": 0.00,
            "max_tickets_per_order": 1
        }
    ]
}
```



***More example Requests/Responses:***


#### I. Example Request: Create Event



***Body:***

```js        
{
    "title": "Django Meetup - Osun Branch",
    "summary": "APIs in Django",
    "description": "Let's discuss the detailed aspects of DRF and its wonders",
    "url": "https://www.django-rest-framework.org/api-guide/serializers/#modelserializer",
    "category": "Technology",
    "event_type": "Conference",
    "timing_type": "Recurring",
    "tz": "Africa/Lagos",
    "tags": [
        "api", "drf", "backend"
    ],
    "location": {
        "location_type": "Venue",
        "location": "11th Redmond, CA",
        "conference_uri": "https://meet.google.com",
        "lat": "38.4267861",
        "long": "-192.0806032",
        "state": "Osun",
        "country": "NG"
    },
    "tickets": [
        {
            "name": "Ticket #1",
            "description": "VIP Ticket",
            "quantity_available": "100",
            "unit_price": 0.00,
            "max_tickets_per_order": 1
        }
    ]
}
```



#### I. Example Response: Create Event
```js
{
    "id": 3,
    "tags": [
        "api",
        "drf",
        "backend"
    ],
    "tz": "Africa/Lagos",
    "location": {
        "id": 3,
        "location_type": "Venue",
        "location": "11th Redmond, CA",
        "conference_uri": "https://meet.google.com",
        "lat": "38.4267861000000000",
        "long": "-192.0806032000000000",
        "state": "Osun",
        "country": "NG"
    },
    "tickets": [
        {
            "id": 3,
            "created_at": "2022-07-13T00:02:30.210295Z",
            "updated_at": "2022-07-13T00:02:30.210302Z",
            "uuid": "cc0bb832-db1c-459f-8819-5e7ac637e92a",
            "name": "Ticket #1",
            "description": "VIP Ticket",
            "quantity_available": 100,
            "unit_price": "0.00000",
            "max_tickets_per_order": 1
        }
    ],
    "created_at": "2022-07-13T00:02:30.190264Z",
    "updated_at": "2022-07-13T00:02:30.190274Z",
    "uuid": "a3490cbc-1f04-4d33-b426-697832a755a1",
    "title": "Django Meetup - Osun Branch",
    "summary": "APIs in Django",
    "description": "Let's discuss the detailed aspects of DRF and its wonders",
    "url": "https://www.django-rest-framework.org/api-guide/serializers/#modelserializer",
    "category": "Technology",
    "event_type": "Conference",
    "timing_type": "Recurring",
    "start_date": "2022-07-13",
    "start_time": null,
    "end_date": "2022-07-13",
    "end_time": null,
    "creator": 2
}
```


***Status Code:*** 201

<br>



### 2. List Events



***Endpoint:***

```bash
Method: GET
Type: 
URL: {{event}}
```



***More example Requests/Responses:***


#### I. Example Request: List Events



***Body: None***



#### I. Example Response: List Events
```js
[
    {
        "id": 3,
        "tags": [
            "api",
            "drf",
            "backend"
        ],
        "tz": "Africa/Lagos",
        "location": {
            "id": 3,
            "location_type": "Venue",
            "location": "11th Redmond, CA",
            "conference_uri": "https://meet.google.com",
            "lat": "38.4267861000000000",
            "long": "-192.0806032000000000",
            "state": "Osun",
            "country": "NG"
        },
        "tickets": [
            {
                "id": 3,
                "created_at": "2022-07-13T00:02:30.210295Z",
                "updated_at": "2022-07-13T00:02:30.210302Z",
                "uuid": "cc0bb832-db1c-459f-8819-5e7ac637e92a",
                "name": "Ticket #1",
                "description": "VIP Ticket",
                "quantity_available": 100,
                "unit_price": "0.00000",
                "max_tickets_per_order": 1
            }
        ],
        "created_at": "2022-07-13T00:02:30.190264Z",
        "updated_at": "2022-07-13T00:02:30.190274Z",
        "uuid": "a3490cbc-1f04-4d33-b426-697832a755a1",
        "title": "Django Meetup - Osun Branch",
        "summary": "APIs in Django",
        "description": "Let's discuss the detailed aspects of DRF and its wonders",
        "url": "https://www.django-rest-framework.org/api-guide/serializers/#modelserializer",
        "category": "Technology",
        "event_type": "Conference",
        "timing_type": "Recurring",
        "start_date": "2022-07-13",
        "start_time": null,
        "end_date": "2022-07-13",
        "end_time": null,
        "creator": 2
    }
]
```


***Status Code:*** 200

<br>



### 3. Retrieve Event



***Endpoint:***

```bash
Method: GET
Type: 
URL: {{event}}/25
```



***More example Requests/Responses:***


#### I. Example Request: Retrieve Event



***Body: None***



#### I. Example Response: Retrieve Event
```js
{
    "id": 3,
    "tags": [
        "api",
        "drf",
        "backend"
    ],
    "tz": "Africa/Lagos",
    "location": {
        "id": 3,
        "location_type": "Venue",
        "location": "11th Redmond, CA",
        "conference_uri": "https://meet.google.com",
        "lat": "38.4267861000000000",
        "long": "-192.0806032000000000",
        "state": "Osun",
        "country": "NG"
    },
    "tickets": [
        {
            "id": 3,
            "created_at": "2022-07-13T00:02:30.210295Z",
            "updated_at": "2022-07-13T00:02:30.210302Z",
            "uuid": "cc0bb832-db1c-459f-8819-5e7ac637e92a",
            "name": "Ticket #1",
            "description": "VIP Ticket",
            "quantity_available": 100,
            "unit_price": "0.00000",
            "max_tickets_per_order": 1
        }
    ],
    "created_at": "2022-07-13T00:02:30.190264Z",
    "updated_at": "2022-07-13T00:02:30.190274Z",
    "uuid": "a3490cbc-1f04-4d33-b426-697832a755a1",
    "title": "Django Meetup - Osun Branch",
    "summary": "APIs in Django",
    "description": "Let's discuss the detailed aspects of DRF and its wonders",
    "url": "https://www.django-rest-framework.org/api-guide/serializers/#modelserializer",
    "category": "Technology",
    "event_type": "Conference",
    "timing_type": "Recurring",
    "start_date": "2022-07-13",
    "start_time": null,
    "end_date": "2022-07-13",
    "end_time": null,
    "creator": 2
}
```


***Status Code:*** 200

<br>



### 4. Delete Event



***Endpoint:***

```bash
Method: DELETE
Type: 
URL: {{event}}/2
```



***More example Requests/Responses:***


#### I. Example Request: Delete Event



***Body: None***



***Status Code:*** 204

<br>



## Users



### 1. Event



***Endpoint:***

```bash
Method: 
Type: 
URL: 
```



### 2. ME



***Endpoint:***

```bash
Method: GET
Type: 
URL: {{user}}/me
```



***More example Requests/Responses:***


#### I. Example Request: ME



***Body: None***



#### I. Example Response: ME
```js
{
    "id": 3,
    "username": "testuser2",
    "email": "testuser2@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "prefix": "Mr.",
    "phone_number": "+2349032419608",
    "job_title": "Student",
    "company": "Wasp IX",
    "website": "https://stemitom.github.io",
    "blog": "https://stemitom.github.io/blog",
    "country": "NG",
    "postal_code": 200106,
    "is_email_verified": false,
    "email_verified_at": null,
    "created_at": "2022-07-13T00:00:39.148020Z",
    "updated_at": "2022-07-13T00:00:39.148021Z"
}
```


***Status Code:*** 200

<br>



---
[Back to top](#desk-square)

>Generated at 2022-07-13 01:30:31 by [docgen](https://github.com/thedevsaddam/docgen)

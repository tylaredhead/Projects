# Project: Inventory Management System

## Description 
The Inventory Management System using a React js frontend combined with a Node js api for login authorisation and a Spring Boot with java for the backend, handling the database queries. This also used MySQL for the relational databases.

This enables user authentication with access tokens to login, enabling the user to enter information to get, update and delete information from the database, with the ability to register new accounts depending on your access role.

#### The project creates an interactive GUI where the user can:  

- Hashes the stored passwords on the express Node js backend for login authorisation.
- Allow different actions depending on your access token, after login credentials have been verified.
- Allow some users to register accounts that enable them to log in.
- Enable users to get, update and delete from a normalised database using the Spring Boot backend using a REST controller. 

## How to use the project? 
For the frontend, in the command prompt at `\\...\\InventoryManagement\\frontend\\inventorymanagement`, run the command `npm run dev` to set the server running.

For the express Node js backend, in the command prompt at `\\...\\InventoryManagement\\loginAuth`, run the command `node server.js` to set the server running.

For the Spring Boot backend, download MySQL Workbench [here](https://www.mysql.com/products/workbench/). Set up a new relational database adding a new model with the following within schema inventory:
- Table: Stock
    - Field: productId INT PRIMARY KEY
    - Field: rating VARCHAR(255)
    - Field: quantity INT UNSIGNED ZEROFILL
    - Field: id INT
- Table: Product
    - Field: productId INT PRIMARY KEY
    - Field: productName VARCHAR(255)
    - Field: productDesc VARCHAR(255)
    - Field: productType VARCHAR(255)
    - Field: supplierId INT
    - Field: price FLOAT UNSIGNED
- Table: Supplier
    - Field: supplierId INT PRIMARY KEY
    - Field: supplierName VARCHAR(255)
    - Field: supplierNo VARCHAR(255)
    - Field: supplierEmail VARCHAR(255)

If the database is running a different port to 3306, this will need to be updated withing the applications.properties within `backend\\src\\main\\resources`. The username and password will also need to be updated. 

## Challenges and future features

- Having not used the frameworks React and Spring Boot before, this meant I had a steep learning curve, finding more efficient methods before and after solutions were created, while errors such as the communication between frontend and backend using api was particuarly challenging before realising CORS needed to be enabled.
- Having initially trying to use the Entity tables to return information, I found initial problems with returning a joined table where there were fields from Stock and Product. To solve this, I created a DTO to be returned which could be instantiated in the service layer.

Other future features include:  
- Although the use of local storage for the login authorisation works to store the username and password entered by the user, this leads to vulnerabilities through Cross Site Scripting, so this needs to be converted to a useState version.
- The ability to create database records.
- Encryption of data before sending - although none of the data is filtered or checked outside of the backend with the passwords being stored within the node js server being hashed, to increase security a RSA encryption could be used.

## What did you learn

1. Importance of scalability and versatility within the design, particurlarly in terms of the filtering in the backend.
2. Importance of condensing options such as Get and Update into a dropdown menu, to enable for simplicity.
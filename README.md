        PRODUCT PRICING AND DISCOUNT MANAGEMENT SYSTEM
GROUP 12 BSCS 1B
1.CHARLES INSON
2.PENIEL LANOY
3.RONALD GOMEZ
4.CRISTIAN ZAFRA
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PROGRESSIVE REPORT: Start designing our admin dashboard, we added some features/function like add prod id, set product price, and view the list of added product, added sidebar overlay button.



*MODULE 1*

In our module 1 we start designing our admin dashboard and we add some features/function on it like add product ID, set PRICE, 
and see the list of the added product and, then we need to fix the problem that when we finished entering the added product ID and set PRICE it will display but when we refresh the browser
it will dissapear so thats the problem are we working now. And we hope we finished our project.

after searching on internet we finally know how the product details will not dissapear we used the code || "localStorage.getItem(productStorageKey);"|| so when we add another product and display, it will never
dissapear when we refresh the browser.

and also we add sidebar overlay button to edit product and edit the price of the product 




-------------------------------------------------------------------------------------------------------------

*MODULE 2*

PROGRESSIVE REPORT: Start making the module 2 our module 2 is discount management system

        
 Features

1. **Hardcoded Discount percent per Rule**

| Discount Rule | Discount % | 
|---------------|-----------|
| Rule 1 | 10% | 
| Rule 2 | 20% | 
| Rule 3 | 30% |
| Rule 4 | 40% | 
| Rule 5 | 50% |

On the expiration date the admin will manual add or edit the time of expiration

 2. **Real-Time Countdown Timer (HH:MM:SS)**
- Displays remaining time in clear `HH:MM:SS` format
- Updates **every second** for live countdown
- Example: `02:15:45` = 2 hours, 15 minutes, 45 seconds remaining

 
 5. **Persistent Storage**
- All discount data including expiration timestamp saved to **LocalStorage**
- Data persists across browser sessions
- No backend database needed

# Viewing Discounts#
The discount table shows:
- Product ID
- Base Price
- Discount %
- Discounted Price
- **⏱️ Expires In** (HH:MM:SS countdown)
- Remove button

LocalStorage Keys

| Key | Purpose | Format |
|---------------|-----------|-------------------|
| pricing_product | All product | JSON array |
| pricing_discounts | All discount with expiration  | JSON array |


Understanding the code:
localStorage:
- Browser's built in storage (like small data base)
- Data stored as JSON strings
- Persists across page reloads 

*MODULE 3*

PROGRESSIVE REPORT 

WE change our discount rule instead of our discount has already assiged an expiration , we changed to manually set the discount duration

we still not finished our module 3 but we start building it

PROGRESSIVE REPORT:
Sorry for the late submission.

Done making module 3 on our project, our module 3 called is discount history management, on this module only the admin can see the discount history of when was the product are added the discount.
After adding discount for the product it will display the information on the discount history log under discount management dashboard.


**PREREQUISITES**
- Laptop huawei 
- VS CODE v1.117
- Python 3.14.4
- Flask v 3.1.3
- GIT v2.54.0
- Github
- Vercel  https://walara.vercel.app/login
- admin uname = gwapo@bisu.edu.ph
- pass = admin
- user uname= pangit@bisu.edu.ph
- pass = user


We have a problem on our module 3 the discount history management because it only work on the local like when we add discount to the product it will only work on local i mean the https//:http://127.0.0.1:5000 
but when we used the live vercel when we start added discount to product it wll not display to the dashboard we ask AI on how to fix but it said we need a DATA BASE but we don't know how to create that so thats the problem we need to fix.

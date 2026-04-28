        PRODUCT PRICING AND DISCOUNT MANAGEMENT SYSTEM
GROUP 12 BSCS 1B
1.CHARLES INSON
2.PENIEL LANOY
3.RONALD GOMEZ
4.CRISTIAN ZAFRA
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PROGRESSIVE REPORT: Start designing our admin dashboard, we added some features/function like add prod id, set product price, and view the list of added product, added sidebar overlay button.



module1:
in our module 1 we start designing our admin dashboard and we add some features/function on it like add product ID, set PRICE, 
and see the list of the added product and, then we need to fix the problem that when we finished entering the added product ID and set PRICE it will display but when we refresh the browser
it will dissapear so thats the problem are we working now. And we hope we finished our project.

after searching on internet we finally know how the product details will not dissapear we used the code || "localStorage.getItem(productStorageKey);"|| so when we add another product and display, it will never
dissapear when we refresh the browser.

and also we add sidebar overlay button to edit product and edit the price of the product 




-------------------------------------------------------------------------------------------------------------


PROGRESSIVE REPORT: Start making the module 2 our module 2 is discount management system

        
 Features

1. **Hardcoded Expiration Duration per Rule**
Each discount rule now has a **fixed expiration time** based on the discount percentage:

| Discount Rule | Discount % | Expiration Duration |
|---------------|-----------|-------------------|
| Rule 1 | 10% | 1 Day |
| Rule 2 | 20% | 2 Days |
| Rule 3 | 30% | 3 Days |
| Rule 4 | 40% | 4 Days |
| Rule 5 | 50% | 7 Days |

*No need to select expiration separately* - it's automatic based on the rule!

 2. **Real-Time Countdown Timer (HH:MM:SS)**
- Displays remaining time in clear `HH:MM:SS` format
- Updates **every second** for live countdown
- Example: `02:15:45` = 2 hours, 15 minutes, 45 seconds remaining

 3. **Auto-Expiration**
- Expired discounts are **automatically removed** from LocalStorage every second
- No manual deletion needed
- Real-time removal from UI

4. **Visual Alert - Expiring Soon**
- Rows **highlight in yellow** when discount expires in less than 1 hour
- Makes it easy to spot soon-to-expire discounts

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


PROGRESSIVE REPORT 

WE change our discount rule instead of our discount has already assiged an expiration , we changed to manually set the discount duration

we still not finished our module 3 but we start building it

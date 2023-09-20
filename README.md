# SightShopHTN2023
(camera recognition and AdHawk Mindlink controls for our program, SightShop)
by Andy, Derek, Derrick, Owen

# Inspiration
Prices for goods across the country have been rapidly increasing over the past couple of years putting a strain on people's wallets. We wanted to help alleviate the pressure that so many Canadians have by building an application that listed multiple prices for the same good allowing for a more informed decision.

# What it does
SightShop uses the built in camera feature of Adhawk's glasses to identify objects within a user's point of view. SightShop then surfs the internet for identified object and lists them out on a table in a separate page for users to compare. The table includes prices, store, and product name.

# How we built it
Adhawk Mindlink tracking data for user controls (blink event) For object identification, we used YOLOv3 pre-trained model to identify objects with the Mindlink cameras. This is then relayed onto a flask web app where the table will also be included on a separate page.

# Challenges we ran into 
One of the biggest challenges we faced was the merging of the camera live stream and the web app itself. There was a lot of trouble setting up the Mindlink itself

# Accomplishments that we're proud of
We're proud of being able to produce a solution using new hardware presented at the booth (Adhawk Mindlink).

# What we learned
We learnt to manipulate Flask and object identification models.

What's next for SightShop
A next step for SightShop is to utilize pupil movement software within the Adhawk Mindlink glasses for a more accurate reading of user's intent for greater accuracy and convenience.

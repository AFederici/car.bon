PennApps XX Hackathon

The app is designed to be a way to gamify personal reducation of CO2.  The way it would work is that you would simply call or text 
a designated number anytime you start or stop the car and its that simple.  You would then be able to log in to your dashboard to 
see your weekly summaries, how you compare against your friends, how you compare against a national average, your progress towards reduction,
and encouraging messages to maybe walk or bike when you can!  Although we didn't complete the interface, I ended up completing the majority of the backend
of this project.  The twilio API was linked to an AWS API instance that acted as a translations layer on top of an AWS Lambda instance.
The lambda project handled the different cases and test processing involved with how to handle various text messages.  Any database storage relied on NOSQL through 
AWS DynamoDB.

# Plagiarism-Check-API
A simple API that can check similarities between 2 texts

Make a post request to /registration to create users
Users have usernames,passwords and tokens
</br>
example:
</br>
{"username": "popo",
"password: "popo"}

Make a post request to /detection to check for similarity
Each check costs 1 token, correct username and password
</br>
example:
</br>
{"username": "popo",
"password: "popo",
"text1: "cats are cool"
"text2: "cats are REAAAAALLY cool"}

Make a post request to /refill to refill your token (the admin_password is "meow", its required.)
</br>
example:
</br>
{
	"username":"popo",
	"admin_password":"meow",
	"refill_amount": 100
}

If you want to run locally, comment out 
</br>
`client = MongoClient('mongodb://db:27017')`
</br>
Comment in
</br>
`client = MongoClient('mongodb://localhost:27017')`

I included docker compose in it so If you have docker, feel free to 
</br>
`docker build`
</br>
`docker compose`

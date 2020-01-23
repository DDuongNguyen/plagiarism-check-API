# plagiarism-check-API
A simple API that can check similarities between 2 texts

Make a post request to /registration to create users
Users have usernames,passwords and tokens
example:
{"username": "popo",
"password: "popo"}

Make a post request to /detection to check for similarity
Each check costs 1 token, correct username and password
example:
{"username": "popo",
"password: "popo",
"text1: "cats are cool"
"text2: "cats are REAAAAALLY cool"}

Make a post request to /refill to refill your token (the admin_password is "meow", its required.)
example:
{
	"username":"popo",
	"admin_password":"meow",
	"refill_amount": 100
}

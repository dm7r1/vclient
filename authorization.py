from superdata.us3r import user
import client.codes as codes

result, app = user.log_in()
if result == codes.LOGGED_IN:
	from main import start_app
	start_app(app)
elif result == codes.NO_DATA:
	print("no user data")
elif result == codes.WRONG_DATA:
	print("wrong user data")
elif result == codes.BUSY_USER:
	print("user is busy")
elif result == codes.NO_SERVER_CONNECTION:
	print("no server connection")

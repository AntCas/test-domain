import os
import webapp2
import jinja2
import cgi #Common Gateway Interface, includes escape (HTML) function

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

#####################################################################################################################
#Index page #testdomainforme.appspot.com/
#####################################################################################################################
class MainHandler(Handler):
	#Prints form
	def write_form(self, error="", month="", day="", year=""):
		template_values = { "error": error, 
							"month": escape_html(month),
							"day": escape_html(day),
							"year": escape_html(year)										
							}
							
		template = jinja_env.get_template("index.html")
		self.write(template.render(template_values))
    #Generate default page
	def get(self):
		self.write_form() #use default values

	#Process user input
	def post(self):
		user_month = self.request.get('month') 
		user_day = self.request.get('day')
		user_year = self.request.get('year')
		
		#Check each value submitted by the user for validity
		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)
		
		if not (month and day and year): #The values entered were not all valid
			#Print the form again with an error message but don't erase what user has written
			error_message = "" #initialize the error message
			
			#Check for each variable individually and add appropriate error message as needed
			if not month:
				error_message += "The month you entered was invalid \n"
			if not day:
				error_message += "The day you entered was invalid \n"
			if not year:
				error_message += "The year you entered was invalid \n"
			
			#Re-print the form with error message(s)
			self.write_form(error_message,
							user_month,user_day,user_year)
		else: #All values were valid
			self.redirect("/thanks") #Redirect user to thanks page

#list of all months in the year
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December'] 

#Create dictionary mapping each month to a three letter abbreviation
month_abbvs = dict((m[:3].lower(), m)for m in months)

#Check month for validity (ie it exists in our list of months)
def valid_month(month):
    if month: 								#If a month was entered else return none
		short_month = month[:3].lower() 	#get the abbreviation
		return month_abbvs.get(short_month) #return the full month name from dictionary 
     
#Check day for validity (ie it is an integer between 0 and 32)
def valid_day(day):
	if day and day.isdigit(): 		#if a day is entered and it was an integer
		day = int(day) 				#convert from string to integer
		if day > 0 and day < 32: 	#Check if day is between 1 - 31
			return day 				#return day 
	
#Check year for validity (is an integer between 1900 and 2020)
def valid_year(year):
	if year and year.isdigit():			  #If a year was entered and it was an integer else return none
		year = int(year)				  #convert from string to integer
		if year >= 1900 and year <= 2020: #Check if year between 1900 - 2020
			return year					  #return year  


#Converts characters like " and & to HTML code so that forms cannot be broken out of by user
def escape_html(s): 
	return cgi.escape(s, quote = True) #escape quotes as well as all default escape characters
	
#####################################################################################################################
#Thanks page for valid data #testdomainforme.com/thanks
#####################################################################################################################
class ThanksHandler(Handler):
	def get(self):
		self.write("Thanks! That's a really valid day!")
		
#####################################################################################################################
#ROT13 #testdomainforme.appspot.com/rot13
#####################################################################################################################
class Rot13Handler(Handler):
	#prints the rot13 form
	def write_rot_form(self, text=""):
		template_values = { "text": escape_html(text)}
							
		template = jinja_env.get_template("rot13.html")
		self.write(template.render(template_values))
		
	def get(self):
		self.write_rot_form()

	def post(self):
		text = self.request.get("text")
		text = rot_13(text)
		self.write_rot_form(text)
		
import string
alpha_list_lower = string.ascii_lowercase # "a...z"
alpha_list_upper = string.ascii_uppercase # "A...Z

#Takes text and applies rot13 to it
#everything that is not an alphabet letter is skipped
#HTML escaping is not handled here
def rot_13(text):
	rot_text = "" #result
	num = 0		  # This is a placeholder to store the location of a character within the string
	for char in text:
		if char in alpha_list_upper: 			#It is an uppercase letter
			num = alpha_list_upper.index(char)  #Get the index of the character within the appropriate alphabet string created above
			if num <=12: 						#All letters up to and including 'm'
				char = alpha_list_upper[num+13] #replace with the letter 13 spots ahead
			else: 								#All letters after 'm'
				char = alpha_list_upper[num-13] #replace with the letter 13 spots behind
			rot_text += char 					#add the new character to the string
		
		elif char in alpha_list_lower: 			#It is a lowercase letter
			num = alpha_list_lower.index(char)
			if num <=12:
				char = alpha_list_lower[num+13]
			else:
				char = alpha_list_lower[num-13]
			rot_text += char
		
		else: #not an alphabet letter
			rot_text += char 
			
	return rot_text		

#####################################################################################################################
#SignUp #testdomainforme.appspot.com/signup
#####################################################################################################################
class SignUpHandler(Handler):
	#Default values
	def write_signup_form(self, username="", username_error="", password="", password_error="", verify="", email="", email_error=""):
		template_values = { "username": escape_html(username),
							"username_error": escape_html(username_error), 
							"password": escape_html(password),
							"password_error": escape_html(password_error),
							"verify": escape_html(verify),
							"email": escape_html(email),
							"email_error": escape_html(email_error)
							}
							
		template = jinja_env.get_template("signup.html")
		self.write(template.render(template_values))
			
	def get(self):
		self.write_signup_form()
		
	def post(self):
		#Get variables from user
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		
		#Check each value submitted by the user for validity
		username_error = valid_username(username)
		password_error = valid_password(password, verify)
		email_error = valid_email(email)
		
		#If input was valid send user to success page
		if not username_error and not password_error and not email_error:
			global variable
			variable = username
			self.redirect("/welcome")
		else: #If input was invalid, regenerate the form
			self.write_signup_form(username, username_error, password, password_error, verify, email, email_error)
	
import re #Regular Expressions

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	if USER_RE.match(username):
		return ""
	else:
		return "Invalid Username"
	
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password, verify):
	if password == verify:
		if PASS_RE.match(password):
			return ""
		else:
			return "Invalid Password"
	else:
		return "Passwords did not match"

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	if email == "":
		return ""
	elif EMAIL_RE.match(email):
		return ""
	else:
		return "Invalid Email"

#####################################################################################################################		
#Welcome Handler
#####################################################################################################################
class WelcomeHandler(Handler):
	def get(self):
		self.write("Welcome ")
		self.write(variable)
#####################################################################################################################		
#Blog #testdomainforme.appspot.com/basicblog 
#####################################################################################################################
class Entry(db.Model):
	title = db.StringProperty(required = True) #Throw exception if Entry does not have a title parameter of type string
	entry = db.TextProperty(required = True) 	   #Throw exception if Entry does not have an entry parameter of type text
	created = db.DateTimeProperty(auto_now_add = True) #Record time submitted

	
class BasicBlogHandler(Handler):
	def render_front(self, title="", entry="", error=""):
		entrys = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC")
		self.render("basicblog.html", title=title, entry=entry, error=error, entrys=entrys)
		
	def get(self):
		self.render_front()

#####################################################################################################################		
#Blog #testdomainforme.appspot.com/basicblog/newpost
#####################################################################################################################
class NewPostHandler(Handler):
	def render_newpost(self, title="", entry="", error=""):
		self.render("newpost.html", title=title, entry=entry, error=error)
		
	def get(self):
		self.render_newpost()
		
	def post(self):
		title = self.request.get("title")
		entry = self.request.get("entry")
		
		if title and entry:
			a = Entry(title=title,entry=entry)
			a.put()
			
			self.redirect("/basicblog")	
		else:
			error = "We need both a title and something to post!"
			self.render_front(title, entry, error)

#Maps URLs to Handlers
app = webapp2.WSGIApplication([ ('/', MainHandler),
								('/thanks',ThanksHandler),
								('/rot13',Rot13Handler),
								('/signup',SignUpHandler),
								('/welcome',WelcomeHandler),
								('/basicblog',BasicBlogHandler),
								('/basicblog/newpost',NewPostHandler)
								], debug=True)

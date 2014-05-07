test-domain
===========

practice with GoogleApp engine, basic blog, rot13, user signup, error handling

URLS available:
    ('/', MainHandler)
    Error checking on birthdate. 
		('/thanks',ThanksHandler)
		Thanks for signing up! Confirms that your birthday was entered correctly.
		('/rot13',Rot13Handler)
		Applies rot 13 cypher to any text entered by assigning each letter of the alphabet a number.
		Every letter entered gets shifted by 13. ie hello -> urryb
		('/signup',SignUpHandler)
		sign up for a new account. Validates your information, checks for errors.
		('/welcome',WelcomeHandler)
		confirms that you signed up properly
		('/basicblog',BasicBlogHandler)
		serves a VERY basic blog that anyone is free to add too.
		('/basicblog/newpost',NewPostHandler)
		Add a new post to the blog.

import re, random

# Define variables
name = "Greg"
weather = "cloudy"

bot_template = "BOT : {0}"
user_template = "USER : {0}"

rules = {
	'Yo quiero (.*)': [
		'¿Por que quieres {0}?',
		'¿Para que quieres {0}?'
	],
	'Te acuerdas (.*)': [
		'Claro que me acuerdo {0}, por?',
		'Me cuesta acordarme {0}'
	]
}

ruless = {
  'I want (.*)': [
    'What would it mean if you got {0}',
    'Why do you want {0}',
    "What's stopping you from getting {0}"
  ],
  'do you remember (.*)': [
    'Did you think I would forget {0}',
    "Why haven't you been able to forget {0}",
    'What about {0}',
    'Yes .. and?'
  ],
  'do you think (.*)': [
    'if {0}? Absolutely.', 'No chance'
  ],
  'if (.*)': [
    "Do you really think it's likely that {0}",
    'Do you wish that {0}',
    'What do you think about {0}',
    'Really--if {0}'
  ]
}

# Define a dictionary with the predefined responses
responses = {
  "what's your name?": [
      "my name is {0}".format(name),
      "they call me {0}".format(name),
      "I go by {0}".format(name)
   ],
  "what's today's weather?": [
      "the weather is {0}".format(weather),
      "it's {0} today".format(weather)
    ],
  "default": ["default message"]
}

# Define a function that responds to a user's message: respond
def respond(message):
	# print(rules)
	# Call match_rule
	response = match_rule(rules, message)
	print('response1:', response)
	if '{0}' in response:
		# Replace the pronouns in the phrase
		# phrase = replace_pronouns(response)
		phrase = remplazar_pronombres(response)
		print('phrase: ', phrase)
		# Include the phrase in the response
		response = response.format(phrase)

    # Concatenate the user's message to the end of a standard bot respone
    # bot_message = "I can hear you! You said: " + message
    # Return the result
	return response

# Define a function that sends a message to the bot: send_message
def send_message(message):
    # Print user_template including the user_message
    print(user_template.format(message))
    # Get the bot's response to the message
    response = respond(message)
    # Print the bot template including the bot's response.
    print(bot_template.format(response))

# print(send_message("what's your name?"))
# print(send_message("what's today's weather?"))
# print(send_message("hola"))

# Define match_rule()
def match_rule(rules, message):
	response, phrase = "default", None
	# Iterate over the rules dictionary
	for pattern, responses in rules.items():
		# Create a match object
		match = re.search(pattern, message)
		if match is not None:
			response = random.choice(responses)
		# print('pattern: ', pattern, 'response: ', response)
		# print('match', match)
		# Choose a random response

			print('response: ', response)
			if '{0}' in response:
				# phrase = remplazar_pronombres(response)
				phrase = match.group(1)
		# print('phrase:', phrase)
		# Return the response and phrase
	return response.format(phrase)

# Test match_rule
# print(match_rule(rules, "do you remember your last birthday"))

def remplazar_pronombres(message):
	message = message.lower()
	if 'mi' in message:
		return re.sub('mi', 'tu', message)
	if 'tu' in message:
		return re.sub('tu', 'mi', message)

	return message

# Define replace_pronouns()
def replace_pronouns(message):

    message = message.lower()
    if 'me' in message:
        # Replace 'me' with 'you'
        return re.sub('me', 'you', message)
    if 'my' in message:
        # Replace 'my' with 'your'
        return re.sub('my', 'your', message)
    if 'your' in message:
        # Replace 'your' with 'my'
        return re.sub('your', 'my', message)
    if 'you' in message:
        # Replace 'you' with 'me'
        return re.sub('you', 'me', message)

    return message

# print(replace_pronouns("my last birthday"))
# print(replace_pronouns("when you went to Florida"))
# print(replace_pronouns("I had my own castle"))

send_message("Te acuerdas de mi")
send_message("Yo quiero tu leche")
# send_message("I want a robot friend")
# send_message("what if you could be anything you wanted")
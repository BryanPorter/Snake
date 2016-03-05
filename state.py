# Bryan Porter A01519722

class State(object):
# defines functions which are then inherited by game, score and title
	def __init__(self):
		pass

	def exit(self):
#	State is finished, perform cleanup
		pass

	def reason(self):
#	Conditional or logic to see if the current state needs to end, and a new one started
		pass

	def act(self):
#	Automatic Behavior like refreshing image
		pass

class StateMachine(object):

	def __init__(self, host, first_state=None):
		self.host = host
		self.current_state = first_state

	def transition(self, new_state):
#	Transition to a new State
		self.current_state.exit()  ##destructor for previous state

		self.current_state = new_state  ##sets current state to be the new state

		# provide state references to host object and fsm instance
		self.current_state.host = self.host
		self.current_state.fsm = self

	def update(self):
		if self.current_state: # only update if we have a state
			new_state = self.current_state.reason()

			if new_state: # if reason provides new state do transition
				self.transition(new_state)
			else: # otherwise act with current state
				self.current_state.act()
				
				
				
				
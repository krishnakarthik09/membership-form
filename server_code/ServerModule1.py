import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
#@anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def submit(name,weight,address,personal,mobile,email,plan):
  app_tables.gym.add_row(name=name,weight=weight,address=address,personal=personal,mobile=mobile,email=email,plan=plan)
  anvil.email.send(to="krishnakarthik967@gmail.com",subject="Response from Gym app",text=f"""
Name: {name}
Mobile: {mobile}
Address: {address}
Weight: {weight}
Personal Training: {personal}
Plan: {plan}
""")
  anvil.email.send(to=f"{email}",subject="Response from Gym Fitzone Gym",text=f"""
Hello {name},

Your FitZone Gym membership registration is successful.

Selected Plan: {plan}

Our team will contact you soon.

Thank You.
""")
  

from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

    # Any code you write here will run before the form opens.

  @handle("outlined_button_1", "click")
  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    name =self.text_box_1.text
    mobile=int(self.text_box_3.text)
    weight =int(self.text_box_2.text)
    address = self.text_area_1.text
    personal=self.check_box_1.checked
    anvil.server.call('submit',name=name,address=address,weight=weight,personal=personal,mobile=mobile)
    Notification('Your response has been recorded').show()


 

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.js.window.open(
      "https://krishnakarthik09.github.io/fitzone-gym-website/",
      "_self"
    )
  

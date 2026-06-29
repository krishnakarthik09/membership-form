from ._anvil_designer import AddSubscriptionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class AddSubscription(AddSubscriptionTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    names = anvil.server.call('get_all_member_names')
    self.member_dropdown.items = names
    self.result_label.text = ""

  @handle("save_button", "click")
  def save_button_click(self, **event_args):
    member_name = self.member_dropdown.selected_value
    plan = self.plan_box.text
    status = self.status_box.text
    start_date = self.start_date_picker.date
    renewal_date = self.renewal_date_picker.date
    payment_date = self.payment_date_picker.date
    amount_text = self.amount_box.text

    if not member_name:
      self.result_label.text = "Please select a member."
      return
    if not plan or not status:
      self.result_label.text = "Plan and status are required."
      return
    if not amount_text or not amount_text.replace('.', '', 1).isdigit():
      self.result_label.text = "Enter a valid amount."
      return

    amount = float(amount_text)

    anvil.server.call(
      'add_subscription',
      member_name, plan, status,
      start_date, renewal_date, amount, payment_date
    )

    self.result_label.text = f"Saved subscription for {member_name}!"
    self.plan_box.text = ""
    self.status_box.text = ""
    self.amount_box.text = ""
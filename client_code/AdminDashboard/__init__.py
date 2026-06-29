from ._anvil_designer import AdminDashboardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AdminDashboard(AdminDashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.members_grid.visible = False
    self.total_members_label.visible = False
    self.active_label.visible = False
    self.expired_label.visible = False
    self.revenue_label.visible = False

  @handle("unlock_button", "click")
  def unlock_button_click(self, **event_args):
     print("Button clicked!")
    entered = self.password_box.text
    if anvil.server.call('check_admin_password', entered):
      self.password_box.visible = False
      self.unlock_button.visible = False
      self.load_dashboard()
    else:
      alert("Wrong password.")

  def load_dashboard(self):
    data = anvil.server.call('get_dashboard_data')

    total = len(data)
    active = len([d for d in data if d['status'] == 'Active'])
    expired = len([d for d in data if d['status'] == 'Expired'])
    revenue = sum([d['amount_paid'] for d in data if d['amount_paid']])

    self.total_members_label.text = f"Total Members: {total}"
    self.active_label.text = f"Active: {active}"
    self.expired_label.text = f"Expired: {expired}"
    self.revenue_label.text = f"Revenue: ₹{revenue}"

    self.total_members_label.visible = True
    self.active_label.visible = True
    self.expired_label.visible = True
    self.revenue_label.visible = True

    self.members_grid.items = data
    self.members_grid.visible = True
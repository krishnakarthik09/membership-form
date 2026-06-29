import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
from datetime import date

ADMIN_PASSWORD = "karthik123"  # change this to your own password

@anvil.server.callable
def check_admin_password(password):
  return password == ADMIN_PASSWORD

@anvil.server.callable
def get_dashboard_data():
  rows = []
  today = date.today()

  for member in app_tables.gym.search():
    subs = list(app_tables.subscriptions.search(member=member))
    subs.sort(key=lambda s: s['payment_date'] or date.min, reverse=True)
    latest = subs[0] if subs else None

    status = "No subscription"
    plan = "—"
    renewal_date = None
    amount_paid = None
    payment_date = None

    if latest:
      plan = latest['plan'] or "—"
      renewal_date = latest['renewal_date']
      amount_paid = latest['amount_paid']
      payment_date = latest['payment_date']
      if renewal_date and renewal_date < today:
        status = "Expired"
      else:
        status = (latest['status'] or "Active").capitalize()

    rows.append({
      "name": member['name'],
      "mobile": member['mobile'],
      "email": member['email'],
      "plan": plan,
      "status": status,
      "renewal_date": renewal_date,
      "amount_paid": amount_paid,
      "payment_date": payment_date,
      "payment_count": len(subs),
    })

  return rows


  
@anvil.server.callable
def get_payment_history(member_name):
  """Returns full payment history for one member, most recent first."""
  member = app_tables.gym.get(name=member_name)
  if not member:
    return []
  subs = list(app_tables.subscriptions.search(member=member))
  subs.sort(key=lambda s: s['payment_date'] or date.min, reverse=True)
  return [
    {
      "plan": s['plan'],
      "amount_paid": s['amount_paid'],
      "payment_date": s['payment_date'],
      "renewal_date": s['renewal_date'],
      "status": s['status'],
    }
    for s in subs
  ]

@anvil.server.callable
def add_subscription(member_name, plan, status, start_date, renewal_date, amount_paid, payment_date):
  member = app_tables.gym.get(name=member_name)
  if not member:
    raise Exception("Member not found")
  app_tables.subscriptions.add_row(
    member=member,
    plan=plan,
    status=status,
    start_date=start_date,
    renewal_date=renewal_date,
    amount_paid=amount_paid,
    payment_date=payment_date,
  )
@anvil.server.callable
def get_all_member_names():
  return [m['name'] for m in app_tables.gym.search()]
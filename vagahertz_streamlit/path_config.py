import os

root_data_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data"
)

unique_users_json_path = os.path.join(root_data_path, "unique_users_json")
os.makedirs(unique_users_json_path, exist_ok=True)

unique_users_qrcode_path = os.path.join(root_data_path, "unique_users_qrcode")
os.makedirs(unique_users_qrcode_path, exist_ok=True)

next_event_qrcode_path = os.path.join(root_data_path, "event_users_qrcode")
os.makedirs(next_event_qrcode_path, exist_ok=True)

root_data_public_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data_public"
)
statuto_path = os.path.join(root_data_public_path, "STATUTO_VAGAHERTZ.pdf")
informativa_path = os.path.join(root_data_public_path, "MODULO-ISCRIZIONE-CON-INFORMATIVA.pdf")

logo_path = os.path.join(root_data_public_path, "vagahertz-logo-2.png")

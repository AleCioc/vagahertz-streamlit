import streamlit as st
import os

from vagahertz_streamlit.gcloud_utils import *

st.title("Security test")

# print(os.getenv("JSON_KEY_GCLOUD"))

#storage_client = initialize_storage_client(store_json_key_from_env())

#st.write(list_blobs("vagahertz", storage_client))

#upload_blob(
#    "vagahertz",
#    "data/unique_users_json/a-a-a.json",
#    "unique_users_json/a-a-a.json",
#    storage_client
#)

if False:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL
    username = "vagahertz@gmail.com"
    password = "yqqb stlh mfqm loid"  # Use the 16-character app password

    sender_email = "vagahertz@gmail.com"
    receiver_email = "alessandro@ciociola.me"
    subject = "Automated Email from Python"
    body = "This is a test email sent from a Python script."

    # Construct the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Encrypts the email
        server.login(username, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()


if False:
    import pandas as pd

    tables = pd.read_html("https://it.wikipedia.org/wiki/Codice_fiscale")

    for table in tables:
        st.write(table)

    tables[0].to_csv(os.path.join(root_data_public_path, "tabella_mesi_nascita.csv"))
    tables[1].to_csv(os.path.join(root_data_public_path, "tabella_caratteri_controllo_pari.csv"))
    tables[2].to_csv(os.path.join(root_data_public_path, "tabella_caratteri_controllo_dispari.csv"))
    tables[3].to_csv(os.path.join(root_data_public_path, "tabella_resto.csv"))
    tables[4].to_csv(os.path.join(root_data_public_path, "tabella_omocodia.csv"))

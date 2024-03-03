import json
import datetime
import base64
import os.path
import qrcode

from codicefiscale import codicefiscale

import streamlit as st

from vagahertz_streamlit.path_config import *


def get_pdf_file_content_as_base64(path):
    with open(path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes


st.title('Registrazione utente')

st.header("Inserisci i tuoi dati")

with st.form("my_form"):
    cols = st.columns((1, 1), gap="large")

    nome = cols[0].text_input('Nome')
    cognome = cols[1].text_input('Cognome')
    sesso_di_nascita = cols[0].selectbox('Sesso di nascita', ['Maschio', 'Femmina', 'Non specificato'])
    data_di_nascita = cols[1].date_input(
        'Data di nascita',
        min_value=datetime.date(1900, 1, 1),
        value=datetime.date(2000, 1, 1)
    )
    luogo_di_nascita = cols[0].text_input('Luogo di nascita')
    provincia_di_nascita = cols[1].text_input('Provincia di nascita')
    codice_fiscale_inserito = cols[0].text_input('Codice fiscale')

    # try:
    #     codice_fiscale_auto = codicefiscale.encode(
    #         lastname=cognome,
    #         firstname=nome,
    #         gender="M",
    #         birthdate=str(data_di_nascita),
    #         birthplace=luogo_di_nascita + " (" + provincia_di_nascita + ")",
    #     )
    #
    #     st.info("Codice fiscale calcolato: " + codice_fiscale_auto)
    #     # st.text_input("Codice fiscale calcolato (modifica se ci sono errori): ", value=codice_fiscale_auto)
    # except:
    #     codice_fiscale_auto = None
    #     st.info("Inserisci tutte le informazioni per calcolare codice fiscale")

    indirizzo_di_residenza = cols[1].text_input('Indirizzo di residenza')
    numero_civico_residenza = cols[0].text_input('Numero civico')
    cap_residenza = cols[1].text_input('CAP')
    provincia_residenza = cols[0].text_input("Provincia di residenza")
    comune_residenza = cols[1].text_input("Comune di residenza")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Clicca per creare nuovo utente")

    if submitted and codice_fiscale_inserito is not None:
        user_info_dict = dict(
            nome=nome,
            cognome=cognome,
            data_di_nascita=data_di_nascita.__str__(),
            luogo_di_nascita=luogo_di_nascita,
            provincia_di_nascita=provincia_di_nascita,
            sesso_di_nascita=sesso_di_nascita,
            codice_fiscale=codice_fiscale_inserito,
            indirizzo_di_residenza=indirizzo_di_residenza,
            numero_civico_residenza=numero_civico_residenza,
            cap_residenza=cap_residenza,
            provincia_residenza=provincia_residenza,
            comune_residenza=comune_residenza
        )
        st.session_state["user_info_dict"] = user_info_dict

# st.write(f"Nome: {nome}")
# st.write(f"Cognome: {cognome}")
# st.write(f"Data di nascita: {data_di_nascita}")
# st.write(f"Luogo di nascita: {luogo_di_nascita}")
# st.write(f"Sesso di nascita: {sesso_di_nascita}")
# st.write(f"Codice Fiscale: {codice_fiscale_inserito}")
# st.write(f"Indirizzo di residenza: {indirizzo_di_residenza}")

pdf_file_content = get_pdf_file_content_as_base64(statuto_path)

st.header("Scarica statuto")
st.download_button(
    label="Clicca per scaricare statuto",
    data=pdf_file_content,
    file_name="STATUTO_VAGAHERTZ.pdf",
    mime="application/octet-stream"
)

st.header("Conferma registrazione")

trattamento_dati_check = st.checkbox("Acconsento al trattamento dei dati secondo...")
statuto_check = st.checkbox("Confermo la presa visione dello statuto secondo...")

if st.session_state["user_info_dict"] is not None:

    st.write(st.session_state["user_info_dict"])

    st.info("Se i dati sono corretti, clicca il pulsante sottostante per salvare il nuovo utente")
    save_user_button = st.button("Salva utente")
    if save_user_button:

        if trattamento_dati_check and statuto_check:
            user_code = "-".join([nome, cognome, codice_fiscale_inserito])
            st.balloons()
            st.success("Utente " + user_code + " registrato con successo!")
            with open(os.path.join(unique_users_json_path, user_code + ".json"), "w") as f:
                json.dump(st.session_state["user_info_dict"], f, indent=4)


            img = qrcode.make(user_code)
            img.save(os.path.join(unique_users_qrcode_path, user_code + ".png"))

            st.image(os.path.join(unique_users_qrcode_path, user_code + ".png"))

            st.write("Grazie per la registrazione!")
            st.session_state["user_info_dict"] = None
        else:
            st.info("Conferma di acconsentire al trattamento dati e aver preso visione dello statuto")
else:
    st.info("Completa tutti i campi per completare la registrazione")

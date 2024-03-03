import json
import datetime
import base64
import os.path

import pandas as pd
import qrcode

from codicefiscale import codicefiscale

import streamlit as st

from vagahertz_streamlit.path_config import *


def get_pdf_file_content_as_base64(path):
    with open(path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes


def check_data_format(_user_info_dict):
    _user_info_dict
    pass


@st.cache_data
def read_excel_cities():
    return pd.read_excel(
        os.path.join(root_data_public_path, "Codici-statistici-e-denominazioni-al-01_01_2024.xlsx")
    )

@st.cache_data
def read_provinces():
    return pd.read_csv(os.path.join(root_data_public_path, "provinces_df.csv"), index_col=0)


if "user_info_dict" not in st.session_state:
    st.session_state["user_info_dict"] = None


st.image(logo_path)

st.title("Benvenut*!")

st.markdown("Questa è la pagina di registrazione e tesseramento digitale di VagaHertz.")

st.markdown(
    """
    Con la tessera digitale potrai:
    - aaa
    - bbb
    - ccc
    """
)

st.title('Registrazione')

st.markdown("""
    Compilando il form sottostante e confermando la registrazione 
    otterrai una tessera digitale VagaHertz per l'anno 2024."""
)

st.header("Dati anagrafici")

cols = st.columns((1, 1), gap="small")

nome = cols[0].text_input('Nome')
cognome = cols[1].text_input('Cognome')
sesso_di_nascita = cols[0].selectbox(
    'Sesso di nascita', ['Maschio', 'Femmina', 'Non specificato']
)
data_di_nascita = cols[1].date_input(
    'Data di nascita',
    min_value=datetime.date(1900, 1, 1),
    value=datetime.date(2000, 1, 1)
)

provinces_df = read_provinces()
provinces_list = provinces_df.Codice.values

italy_cities_names_df = read_excel_cities()

provincia_di_nascita = cols[0].selectbox(
    'Provincia di nascita', options=provinces_list, index=8
)
italy_province_cities_list = italy_cities_names_df.loc[
    italy_cities_names_df["Sigla automobilistica"] == provincia_di_nascita,
    "Denominazione in italiano"
].values

comune_di_nascita = cols[1].selectbox(
    'Comune di nascita', options=italy_province_cities_list
)

codice_fiscale_inserito = cols[0].text_input('Codice fiscale')

try:
    assert len(codice_fiscale_inserito) == 16
except:
    st.warning("Inserisci un codice fiscale valido")

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

st.header("Residenza")

cols = st.columns((4, 1, 1), gap="small")

indirizzo_di_residenza = cols[0].text_input('Indirizzo di residenza')
numero_civico_residenza = cols[1].text_input('Numero civico')
cap_residenza = cols[2].text_input('CAP')

cols = st.columns((1, 1), gap="small")

provincia_residenza = cols[0].selectbox(
    'Provincia di residenza', options=provinces_list, index=8
)
italy_province_cities_list_ = italy_cities_names_df.loc[
    italy_cities_names_df["Sigla automobilistica"] == provincia_residenza,
    "Denominazione in italiano"
].values

comune_residenza = cols[1].selectbox(
    'Comune di residenza', options=italy_province_cities_list_
)

#comune_residenza = cols[0].text_input("Comune di residenza")
#provincia_residenza = cols[1].text_input("Provincia di residenza")


st.header("Scarica statuto")

st.markdown("Prima di confermare, scarica e leggi il nostro Statuto.")

pdf_file_content = get_pdf_file_content_as_base64(statuto_path)

st.download_button(
    label="Clicca per scaricare statuto",
    data=pdf_file_content,
    file_name="STATUTO_VAGAHERTZ.pdf",
    mime="application/octet-stream"
)

st.header("Conferma registrazione")

with st.form("user_registration_form"):

    trattamento_dati_check = st.checkbox("Acconsento al trattamento dei dati secondo...")
    statuto_check = st.checkbox("Confermo la presa visione dello statuto secondo...")

    st.info("Se i dati sono corretti, clicca il pulsante sottostante per salvare il nuovo utente")

    submitted = st.form_submit_button("Clicca per confermare i dati inseriti e creare nuovo utente")


    if submitted and codice_fiscale_inserito is not None:

        user_info_dict = dict(
            nome=nome,
            cognome=cognome,
            data_di_nascita=data_di_nascita.__str__(),
            luogo_di_nascita=comune_di_nascita,
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

    if st.session_state["user_info_dict"] is not None:

        # st.write(st.session_state["user_info_dict"])

        if submitted:

            if trattamento_dati_check and statuto_check:

                user_code = "-".join([nome, cognome, codice_fiscale_inserito])
                user_unique_json_path = os.path.join(unique_users_json_path, user_code + ".json")
                if not os.path.exists(user_unique_json_path):
                    st.balloons()

                    with open(user_unique_json_path, "w") as f:
                        json.dump(st.session_state["user_info_dict"], f, indent=4)

                    img = qrcode.make(user_code)
                    img.save(os.path.join(unique_users_qrcode_path, user_code + ".png"))

                    st.image(os.path.join(unique_users_qrcode_path, user_code + ".png"))

                    st.success("Utente " + user_code + " registrato con successo!")
                    st.success("Grazie per la registrazione!")

                    st.session_state["user_info_dict"] = None

                else:
                    st.error("Esiste già un utente registrato con questo codice fiscale!")

            else:
                st.info("Conferma di acconsentire al trattamento dati e aver preso visione dello statuto")
    else:
        st.warning("Completa tutti i campi per completare la registrazione")

# st.write(f"Nome: {nome}")
# st.write(f"Cognome: {cognome}")
# st.write(f"Data di nascita: {data_di_nascita}")
# st.write(f"Luogo di nascita: {luogo_di_nascita}")
# st.write(f"Sesso di nascita: {sesso_di_nascita}")
# st.write(f"Codice Fiscale: {codice_fiscale_inserito}")
# st.write(f"Indirizzo di residenza: {indirizzo_di_residenza}")

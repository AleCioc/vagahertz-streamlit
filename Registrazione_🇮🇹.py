import re
import datetime
import pandas as pd

import qrcode
from email_validator import validate_email

from vagahertz_streamlit.gcloud_utils import *
from vagahertz_streamlit.st_pages_utils import *


st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

clear_all_but_first_page("Registrazione_🇮🇹.py")


def get_pdf_file_content_as_base64(path):
    with open(path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes


def contains_lowercase(s):
    return any(char.islower() for char in s)


def validate_codice_fiscale(cf):
    # Check the overall length
    if len(cf) != 16:
        return False

    # 1-3 characters: uppercase letters for surname
    if not re.match(r'^[A-Z]{3}', cf):
        return False

    # 4-6 characters: uppercase letters for name
    if not re.match(r'^[A-Z]{3}[A-Z]{3}', cf):
        return False

    # 7-8 characters: year, 9: month, 10-11: day, 12-15: place, 16: checksum
    # More detailed checks can be added here based on specific rules for each part
    # For now, we simply ensure they are alphanumeric and match the expected positions
    if not re.match(r'^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z0-9]{4}[A-Z]$', cf):
        return False

    return True


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
if "valid_codice_fiscale" not in st.session_state:
    st.session_state["valid_codice_fiscale"] = False
if "valid_email" not in st.session_state:
    st.session_state["valid_email"] = False

storage_client = initialize_storage_client(store_json_key_from_env())

st.image(logo_path)

st.title("Benvenut*!")

st.markdown(
    """
    Questa è la pagina di registrazione e tesseramento digitale di VagaHertz.
    """
)

st.markdown(
    """
    Compilando il form sottostante e confermando la registrazione 
    otterrai una tessera digitale VagaHertz per l'anno 2024 con cui 
    potrai accedere agli eventi dell' associazione.
    """
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

from codicefiscale import codicefiscale
from fuzzywuzzy import fuzz

try:
    codice_fiscale_auto = codicefiscale.encode(
        lastname=cognome,
        firstname=nome,
        gender="M",
        birthdate=str(data_di_nascita),
        birthplace=comune_di_nascita,
    )

    # st.text_input("Codice fiscale calcolato (modifica se ci sono errori): ", value=codice_fiscale_auto)

except:

    codice_fiscale_auto = None

try:
    # st.info("Codice fiscale calcolato: " + codice_fiscale_auto)
    # st.write(fuzz.ratio(codice_fiscale_inserito.lower(), codice_fiscale_auto.lower()))
    assert fuzz.ratio(codice_fiscale_inserito.lower(), codice_fiscale_auto.lower()) > 80
    assert validate_codice_fiscale(codice_fiscale_inserito)
    assert not contains_lowercase(codice_fiscale_inserito)
    st.session_state["valid_codice_fiscale"] = True
    cols[0].success("Formato codice fiscale valido!")
except:
    cols[0].warning("Formato codice fiscale non valido!")

user_email = cols[1].text_input('Email')
try:
    valid = validate_email(user_email)
    user_email = valid.normalized
    st.session_state["valid_email"] = True
    cols[1].success("Formato indirizzo email valido!")
except:
    cols[1].warning("Formato email non valido!")

st.header("Residenza")

cols = st.columns((1, 1), gap="small")

provincia_residenza = cols[0].selectbox(
    'Provincia di residenza', options=provinces_list, index=8
)
italy_province_cities_list_ = italy_cities_names_df.loc[
    italy_cities_names_df["Sigla automobilistica"] == provincia_residenza,
    "Denominazione in italiano"
].values

comune_residenza = cols[1].selectbox(
    'Comune di residenza',
    options=italy_province_cities_list_
)

cols = st.columns((4, 1, 1), gap="small")

indirizzo_di_residenza = cols[0].text_input('Indirizzo di residenza')
numero_civico_residenza = cols[1].text_input('Numero civico')
cap_residenza = cols[2].text_input('CAP')

st.header("Statuto e informativa privacy")

st.write("Scarica statuto e informativa, prendi visione e acconsenti al trattamento dati.")
cols_downloads = st.columns((1, 1), gap="small")

#cols_downloads[0].header("Statuto")
#cols_downloads[1].header("Informativa privacy")

pdf_file_content = get_pdf_file_content_as_base64(statuto_path)

cols_downloads[0].download_button(
    label=":arrow_down: Clicca per scaricare lo statuto",
    data=pdf_file_content,
    file_name="STATUTO_VAGAHERTZ.pdf",
    mime="application/octet-stream"
)


informativa_file_content = get_pdf_file_content_as_base64(informativa_path)

cols_downloads[1].download_button(
    label=":arrow_down: Clicca per scaricare l'informativa privacy",
    data=informativa_file_content,
    file_name="INFORMATIVA_VAGAHERTZ.pdf",
    mime="application/octet-stream"
)

statuto_check = cols_downloads[0].checkbox("Confermo la presa visione dello statuto")

trattamento_dati_check = cols_downloads[1].checkbox(
    "Confermo la presa visione dell'informativa e acconsento al trattamento dati"
)

st.header("Conferma registrazione")

with st.form("user_registration_form"):

    st.subheader("Conferma registrazione e invia tessera")

    # if st.session_state["valid_codice_fiscale"]:
    #     pass
    # else:
    #     st.warning("Completa tutti i campi per completare la registrazione!")
    #
    # if st.session_state["valid_codice_fiscale"] and st.session_state["valid_email"]:
    #     pass
    # else:
    #     st.warning("Completa tutti i campi per completare la registrazione!")

    submitted = st.form_submit_button(
        " :arrow_right: Clicca per confermare i dati inseriti e creare nuova tessera :arrow_left:"
    )

    if submitted:

        if trattamento_dati_check and statuto_check\
                and st.session_state["valid_codice_fiscale"] and st.session_state["valid_email"]:

            user_code = "-".join([nome, cognome, codice_fiscale_inserito])

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
                comune_residenza=comune_residenza,
                email=user_email,
                codice_fiscale_calcolato=codice_fiscale_auto,
                user_code=user_code
            )

            valid_info = True
            for k in user_info_dict:
                if len(user_info_dict[k]) == 0:
                    valid_info = False

            if valid_info:

                st.session_state["user_info_dict"] = user_info_dict

                user_unique_json_path = os.path.join(unique_users_json_path, user_code + ".json")

                blobs = list_blobs("vagahertz", "unique_users_json", storage_client)
                blob_names = [blob.name.replace("unique_users_json/", "") for blob in blobs]

                if not user_code + ".json" in blob_names:

                    st.balloons()

                    # with open(user_unique_json_path, "w") as f:
                    #     json.dump(st.session_state["user_info_dict"], f, indent=4)

                    # upload_blob(
                    #     "vagahertz",
                    #     user_unique_json_path,
                    #     "unique_users_json/" + user_code + ".json",
                    #     storage_client
                    # )

                    qrcode_user = qrcode.make(user_code)
                    qrcode_user.save(os.path.join(unique_users_qrcode_path, user_code + ".png"))

                    upload_blob(
                        "vagahertz",
                        os.path.join(unique_users_qrcode_path, user_code + ".png"),
                        "unique_users_qrcode/" + user_code + ".png",
                        storage_client
                    )

                    user_current_event_check_url = "https://vagahertz-backoffice.streamlit.app/Controlla_accesso?user_code=" + user_code
                    qrcode_user_current_event = qrcode.make(user_current_event_check_url)
                    qrcode_user_current_event.save(
                        os.path.join(next_event_qrcode_path, user_code + ".png")
                    )

                    upload_blob(
                        "vagahertz",
                        os.path.join(unique_users_qrcode_path, user_code + ".png"),
                        "events_access/non-solo-techno_2024-03-16/" + user_code + ".png",
                        storage_client
                    )

                    st.success("Tessera registrata con successo!")
                    st.success("Grazie per la registrazione!")

                    st.subheader("QR code per l'evento")
                    st.image(os.path.join(next_event_qrcode_path, user_code + ".png"))

                    st.session_state["user_info_dict"] = None

                else:

                    st.error("Esiste già un utente registrato con questo codice fiscale!")

            else:

                st.error("Mmmm sembra che ci sia stato un errore.")
                st.info("""
                    Verifica di aver inserito tutti i dati correttamente.
                """)

        else:

            st.error("Mmmm sembra che ci sia stato un errore.")
            st.info("""
                Verifica di aver inserito tutti i dati correttamente.
            """)
            st.info("""
                Verifica di aver confermato la presa visione di statuto e informativa trattamento dati.
            """)
            st.info("""
                Se hai effettuato correttamente entrambe le operazioni, contatta l'associazione.
            """)
    else:
        pass


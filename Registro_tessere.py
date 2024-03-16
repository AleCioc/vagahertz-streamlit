from vagahertz_streamlit.gcloud_utils import *

st.set_page_config(page_title="Registro tessere")

st.title('Registro tessere')

text_input_container = st.empty()

st.session_state["passkey"] = text_input_container.text_input("Inserire passkey", label_visibility="hidden", type="password")

if st.session_state["passkey"] == st.secrets["PASSKEY"]:

    text_input_container.empty()
    st.session_state["passkey"] = "NAN"

    storage_client = initialize_storage_client(store_json_key_from_env())
    blobs = storage_client.list_blobs("vagahertz")

    blobs = list_blobs("vagahertz", "unique_users_json", storage_client)

    users_df = create_users_df_from_json_files(
        "vagahertz",
        "unique_users_json",
        storage_client
    )
    users_df.loc[users_df.provincia_di_nascita.apply(lambda s: len(s) == 2), "nazione_di_nascita_auto"] = "Italia"

    from geopy.geocoders import Nominatim

    def get_country_from_city(city):
        time.sleep(1)
        geolocator = Nominatim(user_agent="vagahertz-0")
        location = geolocator.geocode(city, addressdetails=True)

        if location and 'address' in location.raw and 'country' in location.raw['address']:
            return location.raw['address']['country']
        else:
            return "Country not found or ambiguous city name provided."

    users_df.loc[users_df.provincia_di_nascita.apply(lambda s: len(s) > 2), "nazione_di_nascita_auto"] = \
        users_df.loc[users_df.provincia_di_nascita.apply(lambda s: len(s) > 2), "luogo_di_nascita"].apply(
            get_country_from_city
        )

    users_df["codice_fiscale_sistema"] = users_df.codice_fiscale
    users_df["email_sistema"] = users_df.email
    users_df.to_csv(os.path.join(root_data_path, "users_df.csv"))
    upload_blob(
        "vagahertz",
        os.path.join(root_data_path, "users_df.csv"),
        "users_df.csv",
        storage_client
    )
    users_df = users_df.sort_values(
        "registration_timestamp_utc", ascending=True
    )
    users_df["sequenziale_tessera"] = range(len(users_df))
    users_df["sequenziale_tessera"] = users_df["sequenziale_tessera"] + 1

    with st.expander("Guarda registro completo"):
        # users_df
        users_df_to_show = users_df[[
            "registration_timestamp_utc",
            "sequenziale_tessera",
            "nome",
            "cognome",
            "codice_fiscale_sistema",
            "email_sistema",
        ] + [col for col in users_df if "nascita" in col] + [
            col for col in users_df if "residenza" in col
        ]].sort_values(
            "registration_timestamp_utc", ascending=True
        ).set_index("registration_timestamp_utc", drop=True)
        users_df_to_show
        users_df_to_show.to_csv(os.path.join(root_data_path, "users_df_to_show.csv"))

    st.header("Pagamento tessera")

    st.subheader("Convalidare il QR code per Non Solo Techno DOPO che il pagamento tessera + evento è stato effettuato!")

    st.header("Non Solo Techno")

    storage_client = initialize_storage_client(store_json_key_from_env())
    blobs = storage_client.list_blobs("vagahertz")

    blobs = list_blobs(
        "vagahertz",
        "events_access/non-solo-techno_2024-03-16/",
        storage_client
    )

    users_df = create_users_df_from_json_files(
        "vagahertz",
        "events_access/non-solo-techno_2024-03-16/",
        storage_client
    )
    if not len(users_df):
        users_df = pd.DataFrame(columns=["user_code"])

    st.subheader("Lista ingressi")
    with st.expander("Clicca per visualizzare ingressi"):
        users_df
else:
    st.error("Non hai i permessi per consultare il registro!")

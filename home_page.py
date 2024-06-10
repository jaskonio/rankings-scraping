import streamlit as st
import pandas as pd
import numpy as np
import cronochip_service

st.title('Cronochip scraping')

dorsal_value = st.text_input('Dorsal', placeholder='1234,4321,..')

disabled_submit = True

if dorsal_value:
    disabled_submit = False

if st.button("Submit", type="primary", disabled=disabled_submit):
    print(dorsal_value)

    cronochip = cronochip_service.CronoChipService()

    dorsals = [dorsal.strip() for dorsal in dorsal_value.split(',')]
    data, message_error = cronochip.getByDorsals('18', dorsals)

    if message_error is not None:
        st.caption(message_error)

    if data is not None:
        st.dataframe(data)

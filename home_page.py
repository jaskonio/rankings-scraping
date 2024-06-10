import streamlit as st
import pandas as pd
import numpy as np
import cronochip_service

st.title('Cronochip scraping')

dorsal_value = st.text_input('Dorsal')

if st.button("Submit", type="primary"):
    cronochip = cronochip_service.CronoChipService()
    print(dorsal_value)
    data = cronochip.getByDorsal('18', dorsal_value)
    st.dataframe(data)

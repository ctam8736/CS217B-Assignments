from collections import Counter
from operator import itemgetter

import streamlit as st
import pandas as pd
import altair as alt

from spacy_docs import SpacyDocument


example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")


# st.set_page_config(layout='wide')
st.markdown('## spaCy Named Entity Recognition')

text = st.text_area('Text to process', value=example, height=100)

doc = SpacyDocument(text)

entities = doc.get_entities()
dependencies = doc.get_dependencies()
tokens = doc.get_tokens()
counter = Counter(tokens)
words = list(sorted(counter.most_common(30)))

# https://pandas.pydata.org
chart = pd.DataFrame({
    'frequency': [w[1] for w in words],
    'word': [w[0] for w in words]})

# https://pypi.org/project/altair/
bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')

st.markdown(f'Total number of tokens: {len(tokens)}<br/>'
            f'Total number of types: {len(counter)}', unsafe_allow_html=True)

# https://docs.streamlit.io/library/api-reference/data/st.table
st.table(entities)

# https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
st.altair_chart(bar_chart)

st.markdown('## spaCy Dependency Parsing')

st.table(dependencies)

dependency_types = [dep[1] for dep in dependencies]
dep_type_counter = Counter(dependency_types)
deps = list(sorted(dep_type_counter.most_common(30)))

dep_chart = pd.DataFrame({
    'frequency': [d[1] for d in deps],
    'dep_type': [d[0] for d in deps]})

dep_bar_chart = alt.Chart(dep_chart).mark_bar().encode(x='dep_type', y='frequency')

st.altair_chart(dep_bar_chart)
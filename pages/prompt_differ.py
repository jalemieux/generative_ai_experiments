
import streamlit as st
import json
import datetime
from bs4 import BeautifulSoup

import core
from core.completion import OllamaCompletion
from core.converser import Converser


#from core.completion import OllamaCompletion


@st.cache_resource
def ollama():
    return OllamaCompletion(model="llama3.1", default_temperature=0.0)

@st.cache_data
def content():
    with open("./jira.htm", 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

prompts = [
    {
        "name" : "intent_class_prompt",
        "content": """
You are a text analysis expert specializing in intent classification. Your task is to analyze the web page content and identify the underlying intents behind the information presented. Please perform the following steps:
Intent Identification: Analyze the content and classify the primary and secondary intents of the author. Determine what the author is trying to achieve with this content (e.g., inform, persuade, entertain, promote a product, etc.).
Intent Categorization: For each identified intent, provide a brief explanation of why you classified it as such, referencing specific parts of the content that led to your conclusion.
Present your findings clearly, listing each intent and its corresponding explanation.
"""
    },
    {    "name" : "key_info_prompt",
    "content": """
You are an expert in information extraction and text analysis. Your task is to analyze the content of a given web page content and extract the most critical pieces of information. Please perform the following steps:
Identify Key Information: Carefully examine the content and extract the essential details, such as important facts, statistics, recommendations, calls to action, or any other significant points.
Prioritize Relevance: Focus on extracting information that is most relevant and valuable for someone who needs to quickly understand the core message of the content.
Organize Extracted Information: Present the extracted information in a clear and organized manner, grouped by categories or themes if applicable.
Ensure that the extracted information is concise and directly reflects the most important aspects of the content.
"""},
    {"name": "summary_prompt",
     "content":"""
You are a text summarization expert. Your task is to read the content of a given web page content and create a concise summary that captures the most important points. Please perform the following steps:
Condense Information: Summarize the main ideas and essential details of the content in a way that is easy to understand and captures the core message.
Maintain Clarity: Ensure that the summary is coherent, clear, and accurately represents the original content without losing important context.
Focus on Key Points: Highlight the most critical points, avoiding unnecessary details, while ensuring the summary reflects the full scope of the original content.
Provide the summary in a few well-structured sentences or paragraphs.
"""
     }

]

columns = st.columns(len(prompts))
for i, col in enumerate(columns):
    p = prompts[i]
    with col:
        st.subheader(p['name'])
        #st.write(p['content'])
        c = Converser(completion=ollama(),
                        instruction=p['content'],
                        persist=f"./{p['name']}.json")
        c.response(f"web page content: {content()}")
        st.markdown(c.last_message())



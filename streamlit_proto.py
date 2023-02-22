
from steamship import Block, File, RuntimeEnvironments, Steamship, check_environment
from steamship.utils.url import Verb
import streamlit as st


st.title("Fylo Health: Pre-MVP Prototype")

client = Steamship(workspace = "julie-workspace")

api = client.use(package_handle="test-qa-with-sources")


question = st.text_input("Ask me a general question about birth control.", "What are my options for birth control?")
st.write("You entered:", question)

## this is going to be something we'll play with a lot
prompt_addition = " Please answer in a way that a 16 year old would understand."
question = question + prompt_addition

st.write("Awaiting results - please be patient. This may take a few moments.")

response = api.invoke("/qa_with_sources", query=question)

st.title("Response")
st.write("Answer: ",f"{response['output_text'].strip()}")

last_line = response["output_text"].splitlines()[-1:][0]

if "SOURCES: " not in last_line:
            print(last_line)
            print("This is my best guess. I do not currently have a good answer for this question in my sources.")
else:
    sources_list = last_line[len("SOURCES: ") :]

    for source in sources_list.split(","):
        st.write(f"\nSource text ({source.strip()}):")
        for input_doc in response["input_documents"]:
                    metadata = input_doc.get("metadata", {})
                    src = metadata["source"]
                    if source.strip() == src:
                        content = input_doc.get("page_content", "Source text missing")
                        content = " ".join(content.split()) #get rid of dumb spacing
                        st.write(content)

            







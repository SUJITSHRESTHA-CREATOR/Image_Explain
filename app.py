import streamlit as st
import google.generativeai as genai
import os
import PIL.Image
import pandas as pd



#key setup
os.environ["GOOGLE_API_KEY"] = "put_your_api_key_here"
genai.configure(api_key = os.environ["GOOGLE_API_KEY"])


#model loading
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

#function
def image_to_text(img):
    response = model.generate_content(img)
    return response.text

def image_and_query(img, query):
    response = model.generate_content([img, query])
    return response.text


# #lsting the models
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)

#app creation
st.title("Text Generator through Image")
st.write("Upload an Image and get details")


upload_image = st.file_uploader("Upload an Image", type=['png', 'jpg', 'jpeg'])
query = st.text_input("Write something about the image")


if st.button("Generate"):
    if upload_image and query is not None:
        img = PIL.Image.open(upload_image)
        st.image(img, caption="Uploaded Image", width=300)
        
        
        extracted_details = image_to_text(img)
        st.subheader("Extracted Details...")
        st.write(extracted_details)
        
        
        
        generated_details = image_and_query(img, query)
        st.subheader("Generated Details...")
        st.write(generated_details)
        
        
        
        #saving to csv file
        data = {"Extracted Details": [extracted_details], "Generated Details": [generated_details]}

        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)

        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="details.csv",
            mime="text/csv"
        )
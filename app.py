import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import os
from dotenv import load_dotenv
from streamlit_carousel import carousel

# Load environment variables from the .env file
load_dotenv()

# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv('openai_key'))

# Configure the generation settings for the AI model
generation_config = {
  "temperature": 1,  # Controls randomness: higher values make output more random
  "top_p": 0.95,     # Controls diversity via nucleus sampling
  "top_k": 40,       # Controls diversity via top-k sampling
  "max_output_tokens": 8192,  # Maximum length of the generated content
  "response_mime_type": "text/plain",  # Output format
}

# Configure Gemini API client
genai.configure(api_key=os.getenv('gemini_api_key'))

# Initialize the generative AI model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Streamlit web app title and description
st.title("BlogCraft: Your AI Writing Companion")
st.subheader("Now You Can Create Your Blogs Using AI")

# Sidebar for user inputs to generate the blog
with st.sidebar:
    st.title("Input Your Blog Details")
    st.subheader("Enter Details of the Blog You Want to Generate")
    Blog_title = st.text_input("Blog Title")  # Text input for blog title
    Keywords = st.text_area('Keywords')  # Text area for keywords
    num_words = st.slider('Number of words', min_value=250, max_value=1000)  # Slider for word count
    num_img = st.number_input("Number of Images", min_value=1, max_value=5, step=1)  # Number input for images
    submit_button = st.button("Generate Blog")  # Button to submit the request

# Generate the AI prompt for the blog content based on user inputs
prompt = [f'Generate a Comprehensive, Engaging Blog relevant to this title: {Blog_title} and these keywords: {Keywords} without exceeding the following number of words: {num_words}']

# Generate content for the blog using the AI model
response = model.generate_content(prompt)

# Generate images for the blog using OpenAI's DALL-E model
img_response = client.images.generate(
  model="dall-e-3",
  prompt=f"Generate a Blog Post Image using the title: {Blog_title}",
  size="1024x1024",  # Image size
  quality="standard",  # Image quality
  n=num_img,  # Number of images to generate
)

# Extract the image URLs from the API response
image_urls = [image.url for image in img_response.data]

# Prepare the image data for display in a carousel format
images = [dict(title=f'Image{i+1}', text=f'{Blog_title}', interval=None, img=f'{image_urls[i]}') for i in range(len(image_urls))]

# Display the generated content and images if the user presses the "Generate Blog" button
if submit_button:
    st.title('Your Blog Images:')
    carousel(items=images, width=1)  # Display the images in a carousel format
    st.title('Your Blog Post')  # Display the blog title
    st.write(response.text)  # Display the generated blog content

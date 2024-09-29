import streamlit as st
import os

# Set page configuration
st.set_page_config(page_title="Seoul Science Park")

# The list of items and their names
fullOrder = [
    "001@도르래@Pulley", "002@아르키메데스 운동 장치 사용 방법@Instructions for using the Archimedes motion device", "003@정글짐 이용안내@Instructions for using the jungle gym"
]

# Parse items and names into separate lists
itemList = []
nameList_KOR = []
nameList_ENG = []

for itm in fullOrder:
    splitedItm = itm.split('@')
    itemList.append(splitedItm[0])
    nameList_KOR.append(splitedItm[1])
    nameList_ENG.append(splitedItm[2])

itemLength = len(itemList)

# Function to handle modulo operation for cycling through items
def mod(number, modulo):
    return (number % modulo + modulo) % modulo

# Initialize session state variables from query parameters
query_params = st.query_params
if 'itemNo' not in st.session_state:
    st.session_state['itemNo'] = query_params.get('item', [itemList[0]])[0]
if 'lang' not in st.session_state:
    st.session_state['lang'] = query_params.get('lang', ['kor'])[0]

itemNo = st.session_state['itemNo']
lang = st.session_state['lang']

# Validate itemNo
if itemNo not in itemList:
    itemNo = itemList[0]
    st.session_state['itemNo'] = itemNo
index = itemList.index(itemNo)

# (0) Pre-header Section
pre_header_col1, pre_header_col2, pre_header_col3 = st.columns([1, 3, 1])

# Custom CSS to style the button correctly, make it larger, remove underline, and align it to the right
st.markdown("""
    <style>
    div.stButton > button {
        background-color: transparent;
        border: none;
        color: #000;
        font-size: 50px !important; /* Increased font size */
        cursor: pointer;
        text-decoration: none !important; /* Remove underline */
        float: right; /* Align the button to the right */
    }
    div.stButton > button:hover {
        color: #007BFF; /* Change text color on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Toggle button for switching language
with pre_header_col3:
    # Display the button with the current language label
    if lang == 'kor':
        if st.button("🌐"):
            st.session_state['lang'] = 'eng'
            st.session_state['itemNo'] = itemNo
            # Update the query parameters
            st.session_state['query_params'] = {"lang": 'eng', "item": itemNo}
    else:
        if st.button("🌐"):
            st.session_state['lang'] = 'kor'
            st.session_state['itemNo'] = itemNo
            # Update the query parameters
            st.session_state['query_params'] = {"lang": 'kor', "item": itemNo}


# Header Section: Display the title dynamically based on the selected language
header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

# Display the Title in the center column based on the language
with header_col2:
    title = nameList_KOR[index] if st.session_state['lang'] == 'kor' else nameList_ENG[index]
    # Using inline CSS to increase the font size of the title
    st.markdown(f"<h1 style='text-align: center; font-size: 40px;'>{title}</h1>", unsafe_allow_html=True)

# Add a horizontal line (divider) between the title and audio
st.markdown("<hr style='border: 1px solid #ccc; margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)

# Audio Player Section
audio_file_path = os.path.join("mp3files", f"{itemNo}{st.session_state['lang']}.mp3")
audio_col = st.container()

with audio_col:
    if os.path.exists(audio_file_path):
        st.audio(audio_file_path)
    else:
        st.write("Audio file not found.")


# Content Display Area
text_file_path = os.path.join("textfiles", f"{itemNo}{st.session_state['lang']}.txt")
content_col = st.container()  # Container for the content area

with content_col:
    if os.path.exists(text_file_path):
        with open(text_file_path, "r", encoding="utf-8") as file:
            st.write(file.read())
    else:
        st.write("Text file not found.")

bottom_col1, bottom_col2 = st.columns([1, 1])


# Custom CSS to make the buttons stick to the bottom and be placed next to each other
st.markdown("""
    <style>
    /* Container to hold both buttons next to each other */
    .fixed-bottom-buttons {
        position: fixed;
        bottom: 10px; /* Adjust this value to control how far from the bottom the buttons are */
        left: 10px; /* Adjust this to position from the left */
        display: flex;
        gap: 10px; /* Space between the buttons */
        z-index: 1000; /* Ensure the buttons stay on top of other elements */
    }

    /* Style for the buttons themselves */
    .fixed-bottom-buttons button {
        background-color: #f0f0f0; /* Button background color */
        border: 1px solid #ccc; /* Button border */
        font-size: 16px; /* Adjust font size */
        padding: 10px 20px; /* Adjust padding for larger/smaller buttons */
        cursor: pointer;
    }

    /* Optional: Styling on hover */
    .fixed-bottom-buttons button:hover {
        background-color: #ddd; /* Change background color on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Create a container to hold both buttons
st.markdown("<div class='fixed-bottom-buttons'>", unsafe_allow_html=True)

# Place the buttons directly next to each other
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("←", key='prev_button'):
        prev_index = (index - 1) % itemLength
        st.session_state['itemNo'] = itemList[prev_index]
        st.session_state['query_params'] = {"item": itemList[prev_index], "lang": lang}

with col2:
    if st.button("→", key='next_button'):
        next_index = (index + 1) % itemLength
        st.session_state['itemNo'] = itemList[next_index]
        st.session_state['query_params'] = {"item": itemList[next_index], "lang": lang}

st.markdown("</div>", unsafe_allow_html=True)

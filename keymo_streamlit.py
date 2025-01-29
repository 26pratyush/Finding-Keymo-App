import streamlit as st
import itertools
import time
import string

def bruteforce_attack(password):
    chars = string.printable.strip()
    attempts = 0
    for length in range(1, len(password) + 1):
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            guess = ''.join(guess)
            st.session_state['brute_force_attempts'].append(guess)
            if guess == password:
                return (attempts, guess)
    return (attempts, None)

# Initialize session state if not already set
if 'password' not in st.session_state:
    st.session_state['password'] = ""
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = 0
if 'time_taken' not in st.session_state:
    st.session_state['time_taken'] = 0.0
if 'cracked_password' not in st.session_state:
    st.session_state['cracked_password'] = None
if 'brute_force_attempts' not in st.session_state:
    st.session_state['brute_force_attempts'] = []

# Page Navigation
page = st.sidebar.radio("Navigation", ["Welcome", "Enter Password", "Brute Force Attempts", "Cracked Password"])

if page == "Welcome":
    st.title("Welcome to Finding Key-mo")
    st.write("This tool demonstrates a brute-force attack on a password.")
    st.write("Use the sidebar to navigate through the pages.")
    st.write("Passwords having more than 3 characters cannot be cracked due to streamlit memory constraints.")

elif page == "Enter Password":
    st.title("Enter Password")
    password = st.text_input("Enter Password (0-3 characters only):", type="password")
    if st.button("Crack Password"):
        if password:
            st.session_state['password'] = password
            st.session_state['brute_force_attempts'] = []
            start_time = time.time()
            attempts, cracked_password = bruteforce_attack(password)
            end_time = time.time()
            st.session_state['attempts'] = attempts
            st.session_state['time_taken'] = end_time - start_time
            st.session_state['cracked_password'] = cracked_password
            st.success("Password cracking in progress! Check the other pages for details.")
        else:
            st.error("Please enter a password.")

elif page == "Brute Force Attempts":
    st.title("Brute Force Attempts")
    st.write("Below are the attempted passwords:")
    if st.session_state['brute_force_attempts']:
        st.text_area("Attempts", "\n".join(st.session_state['brute_force_attempts']), height=300)
    else:
        st.write("No attempts yet. Enter a password first.")

elif page == "Cracked Password":
    st.title("Cracked Password Result")
    if st.session_state['cracked_password']:
        st.success(f"Password cracked in {st.session_state['attempts']} attempts!")
        st.write(f"Cracked Password: **{st.session_state['cracked_password']}**")
        st.write(f"Time Taken: **{st.session_state['time_taken']:.2f} seconds**")
    else:
        st.warning("No password has been cracked yet. Enter a password first.")

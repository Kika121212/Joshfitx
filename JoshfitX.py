import streamlit as st 
import pandas as pd

# Load client data from CSV
def load_data(): 
    return pd.read_csv("Client.csv")

def authenticate(client_data, username, password): 
    client_row = client_data[(client_data['Name'] == username) & (client_data['Password'] == password)]
    return client_row if not client_row.empty else None

# Streamlit App
def main(): 
    st.title("Joshfitx Fitness Centre")

    menu = ["Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Client Login")
        username = st.text_input("Enter Your Name")
        password = st.text_input("Enter Your Password", type="password")
        
        if st.button("Login"):
            client_data = load_data()
            client_info = authenticate(client_data, username, password)
            
            if client_info is not None:
                st.success(f"Welcome, {client_info['Name'].values[0]}!")
                st.write("### Your Profile")
                
                # Print the columns for debugging
                st.write("Columns available in client_info:", client_info.columns.tolist())

                # Handle missing columns
                try:
                    st.write(f"*Height:* {client_info['Height'].values[0]} cm")
                except KeyError:
                    st.error("Height information is missing.")
                
                try:
                    st.write(f"*Weight:* {client_info['Weight'].values[0]} kg")
                except KeyError:
                    st.error("Weight information is missing.")
                
                try:
                    st.write(f"*Age:* {client_info['Age'].values[0]}")
                except KeyError:
                    st.error("Age information is missing.")
            else:
                st.error("Invalid Username or Password")

if __name__ == "__main__": 
    main()

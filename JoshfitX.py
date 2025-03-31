import streamlit as st
import pandas as pd

# Load client data from CSV
def load_data():
    return pd.read_csv("Client.csv")

def authenticate(client_data, username, password):
    client_row = client_data[(client_data['Name'] == username) & (client_data['Password'] == password)]
    return client_row if not client_row.empty else None

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
                
                tabs = st.tabs(["Profile Details", "Diet Chart"])
                with tabs[0]:
                    st.write("### Your Profile")
                    st.write(f"*Client No:* {client_info['Client No'].values[0]}")
                    st.write(f"*Name:* {client_info['Name'].values[0]}")
                    st.write(f"*Height:* {client_info['Height'].values[0]} cm")
                    st.write(f"*Weight:* {client_info['Weight'].values[0]} kg")
                    st.write(f"*Age:* {client_info['Age'].values[0]}")
                    st.write(f"*BMR:* {client_info['BMR'].values[0]}")
                
                with tabs[1]:
                    st.write("### Diet Chart")
                    display_diet_chart(client_info)
            else:
                st.error("Invalid Username or Password")

def display_diet_chart(client_info):
    # Radio buttons for Day-Odd and Day-Even
    day_type = st.radio("Select Day Type", ('Day-Odd', 'Day-Even'))

    # Determine the columns to display based on the selected day type
    if day_type == 'Day-Odd':
        columns_to_display = ['Breakfast 1', 'Morning Snack 1', 'Lunch 1', 'Evening Snack 1', 'Dinner 1', 'Other 1']
    elif day_type == 'Day-Even':
        columns_to_display = ['Breakfast 2', 'Morning Snack 2', 'Lunch 2', 'Evening Snack 2', 'Dinner 2']

    # Filter the client's data
    client_data = client_info[columns_to_display]

    # Display the table
    st.write(client_data)

if __name__ == "__main__":
    main()

import streamlit as st 
import pandas as pd
import tkinter as tk
from tkinter import ttk

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
def display_diet_chart(selected_day_type):
    # Read the Client.csv file
    df = pd.read_csv('Client.csv')

    # Determine the columns to display based on the selected day type
    if selected_day_type == 'Day-Odd':
        columns_to_display = ['Breakfast 1', 'Morning Snack 1', 'Lunch 1', 'Evening Snack 1', 'Dinner 1']
    else:
        columns_to_display = ['Breakfast 2', 'Morning Snack 2', 'Lunch 2', 'Evening Snack 2', 'Dinner 2']

    # Create a new window to display the table
    window = tk.Toplevel(root)
    window.title('Diet Chart')

    # Create the table
    tree = ttk.Treeview(window)
    tree['columns'] = columns_to_display

    # Define the column headings
    for col in columns_to_display:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    # Insert the data into the table
    for index, row in df.iterrows():
        tree.insert('', 'end', values=[row[col] for col in columns_to_display])

    tree.pack(expand=True, fill='both')

# Create the main window
root = tk.Tk()
root.title("Diet Chart")

# Create radio buttons for Day-Odd and Day-Even
day_type = tk.StringVar(value='Day-Odd')  # Default selection

radio_day_odd = tk.Radiobutton(root, text='Day-Odd', variable=day_type, value='Day-Odd', command=lambda: display_diet_chart(day_type.get()))
radio_day_even = tk.Radiobutton(root, text='Day-Even', variable=day_type, value='Day-Even', command=lambda: display_diet_chart(day_type.get()))

radio_day_odd.pack()
radio_day_even.pack()

root.mainloop()
            else:
                st.error("Invalid Username or Password")

if __name__ == "__main__": 
    main()

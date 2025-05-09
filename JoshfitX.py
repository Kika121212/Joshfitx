import streamlit as st
import pandas as pd
st.set_page_config(page_title="JoshFitX", layout="wide")
# Load client data from CSV
def load_data():
    return pd.read_csv("Client.csv")

# Load food data from CSV
def load_food_data():
    return pd.read_csv("food.csv")

def authenticate(client_data, username, password):
    client_row = client_data[(client_data['Name'] == username) & (client_data['Password'] == password)]
    return client_row if not client_row.empty else None

def main():
    st.title("Joshfitx Fitness Centre")

    # Menu options
    menu = ["Login Page", "BMR Calculator"]

    # Create a sidebar with buttons for each menu option
    st.sidebar.title("Menu")
    for option in menu:
        if st.sidebar.button(option):
            st.session_state.menu_choice = option

    # Default to the first menu option if no button has been clicked yet
    if "menu_choice" not in st.session_state:
        st.session_state.menu_choice = menu[0]

    choice = st.session_state.menu_choice

    if choice == "Login Page":
        st.subheader("Client Login")
        username = st.text_input("Enter Your Name", key="username")
        password = st.text_input("Enter Your Password", type="password", key="password")
        
        if st.button("Login", key="login_button"):
            client_data = load_data()
            client_info = authenticate(client_data, username, password)
            
            if client_info is not None:
                st.session_state.logged_in = True
                st.session_state.client_info = client_info
                st.success(f"Welcome, {client_info['Name'].values[0]}!")
                display_dashboard()
            else:
                st.error("Invalid Username or Password")

    elif choice == "BMR Calculator":
        st.subheader("BMR Calculator")
        height = st.number_input("Enter Your Height (cm)", min_value=0, key="height")
        weight = st.number_input("Enter Your Weight (kg)", min_value=0, key="weight")
        age = st.number_input("Enter Your Age", min_value=0, key="age")
        gender = st.selectbox("Select Your Gender", ["Male", "Female"], key="gender")

        if st.button("Calculate BMR", key="calculate_bmr"):
            if gender == "Male":
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

            st.success(f"Your BMR is: {bmr}")

    if "logged_in" in st.session_state and st.session_state.logged_in:
        display_dashboard()
        
def display_dashboard():
    client_info = st.session_state.client_info

    tabs = st.tabs(["Profile Details", "Diet Chart", "Diet Checker"])
    with tabs[0]:
        st.write("### Your Profile")
        st.write(f"*User ID:* {client_info['Client No'].values[0]}")
        st.write(f"*Name:* {client_info['Name'].values[0]}")
        st.write(f"*Height:* {client_info['Height'].values[0]} cm")
        st.write(f"*Weight:* {client_info['Weight'].values[0]} kg")
        st.write(f"*Age:* {client_info['Age'].values[0]}")
        st.write(f"*BMR:* {client_info['BMR'].values[0]}")
    
    with tabs[1]:
        st.write("### Diet Chart")
        display_diet_chart(client_info)

    with tabs[2]:
        st.write("### Diet Checker")
        display_diet_checker()

def display_diet_chart(client_info):
    # Determine the columns to display for Day-Odd
    columns_day_odd = ['Breakfast 1', 'Morning Snack 1', 'Lunch 1', 'Evening Snack 1', 'Dinner 1', 'Other 1']
    
    # Determine the columns to display for Day-Even
    columns_day_even = ['Breakfast 2', 'Morning Snack 2', 'Lunch 2', 'Evening Snack 2', 'Dinner 2', 'Other 2']
    
    # Filter the client's data for both day types
    client_data_day_odd = client_info[columns_day_odd]
    client_data_day_even = client_info[columns_day_even]
    
    # Display the data one under another
    st.write("### Day-Odd Diet")
    st.write(client_data_day_odd)
    
    st.write("### Day-Even Diet")
    st.write(client_data_day_even)

def display_diet_checker():
    food_data = load_food_data()
    food_items = food_data['Food'].tolist()

    if 'diet_rows' not in st.session_state:
        st.session_state.diet_rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    total_calories = 0

    for row in st.session_state.diet_rows:
        cols = st.columns(4)
        food_item = cols[0].selectbox(f"Food Item {row+1}", food_items, key=f"food_{row}_selectbox")
        quantity = cols[1].number_input(f"Quantity {row+1}", min_value=0, key=f"quantity_{row}_numberinput")
        if food_item:
            calories_per_g = food_data[food_data['Food'] == food_item]['Calories (kcal/g)'].values[0]
            calories = calories_per_g * quantity
            cols[2].write(f"Total Calories: {calories}")
            total_calories += calories
        if cols[3].button("Delete Row", key=f"delete_{row}_button"):
            st.session_state.diet_rows.remove(row)
            st.experimental_rerun()  # Trigger rerun

    st.write(f"**Total Calories Consumed:** {total_calories}")

    # Retrieve BMR from the logged-in client info
    client_info = st.session_state.client_info
    bmr = client_info['BMR'].values[0]

    # Calculate remaining diet
    remaining_diet = bmr - total_calories
    st.write(f"**Remaining Diet (Calories):** {remaining_diet}")

    if st.button("Add Row"):
        st.session_state.diet_rows.append(max(st.session_state.diet_rows) + 1)
        st.experimental_rerun()  # Trigger rerun

if __name__ == "__main__":
    main()

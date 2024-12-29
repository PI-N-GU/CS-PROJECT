import streamlit as st
import sqlite3

# Function to classify food based on nutritional values
def classify_food(calories, proteins):
    if calories < 200 and proteins > 10:
        return "Healthy"
    elif 200 <= calories < 500 and proteins >= 5:
        return "Moderately Healthy"
    else:
        return "Unhealthy"

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('food_classification.db')
    return conn

# Function to create the table if it doesn't exist
def create_table():
    conn = create_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS food_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL UNIQUE,
                calories REAL NOT NULL,
                proteins REAL NOT NULL,
                classification TEXT NOT NULL
            )
        ''')
    conn.close()

# Function to insert food data into the database
def insert_food_data(food_name, calories, proteins, classification):
    conn = create_connection()
    with conn:
        conn.execute('''
            INSERT INTO food_data (food_name, calories, proteins, classification)
            VALUES (?, ?, ?, ?)
        ''', (food_name, calories, proteins, classification))
    conn.close()

# Function to retrieve food data from the database by food name
def get_food_data_by_name(food_name):
    conn = create_connection()
    with conn:
        cursor = conn.execute('SELECT * FROM food_data WHERE food_name = ?', (food_name,))
        data = cursor.fetchone()
    conn.close()
    return data

# Function to retrieve all food data from the database
def get_all_food_data():
    conn = create_connection()
    with conn:
        cursor = conn.execute('SELECT * FROM food_data')
        data = cursor.fetchall()
    conn.close()
    return data

# Function to delete food data from the database
def delete_food_data(food_name):
    conn = create_connection()
    with conn:
        conn.execute('DELETE FROM food_data WHERE food_name = ?', (food_name,))
    conn.close()

# Main program
def main():
    create_table()  # Ensure the table is created

    st.title("Food Classification Program")
    
    # Collecting food details from the user
    food_name = st.text_input("Enter the name of the food item:")
    calories = st.number_input("Enter the calories in the food item:", min_value=0.0)
    proteins = st.number_input("Enter the proteins (in grams) in the food item:", min_value=0.0)
    
    if st.button("Classify Food"):
        # Check if the food item already exists in the database
        existing_data = get_food_data_by_name(food_name)
        if existing_data:
            # If it exists, fetch and display the existing classification
            st.success(f"The food item '{food_name}' already exists in the database.")
            st.write(f"Calories: {existing_data[2]}, Proteins: {existing_data[3]}, Classification: {existing_data[4]}")
        else:
            # Classifying the food
            classification = classify_food(calories, proteins)
            
            # Inserting the food data into the database
            insert_food_data(food_name, calories, proteins, classification)
            
            # Displaying the result
            st.success(f"The food item '{food_name}' is classified as: {classification}")

    # Option to view the database
    if st.button("View Database"):
        food_data = get_all_food_data()
        if food_data:
            st.write("Food Classification Database:")
            for row in food_data:
                st.write(f"ID: {row[0]}, Name: {row[1]}, Calories: {row[2]}, Proteins: {row[3]}, Classification: {row[4]}")
        else:
            st.write("The database is empty.")

    # Option to delete a food item
    st.subheader("Delete Food Item")
    food_to_delete = st.selectbox("Select a food item to delete:", [item[1] for item in get_all_food_data()] if get_all_food_data() else [])
    
    if st.button("Delete Food Item"):
        if food_to_delete:
            delete_food_data(food_to_delete)
            st.success(f"The food item '{food_to_delete}' has been deleted from the database.")
        else:
            st.warning("Please select a food item to delete.")

# Running the main function
if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import plotly.express as px
import openai  # Ensure this is installed: pip install openai

# Set up your OpenAI API key
openai.api_key = "api_key"

# App title
st.title("Dynamic Data Visualization App with LLM Integration")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# If a file is uploaded
if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("Uploaded Dataset:")
    st.dataframe(df)

    # Text input for user prompt
    user_prompt = st.text_input("Describe the graph you want (e.g., 'Create a bar chart with X as Age and Y as Salary'):")

    # Generate graph button
    if st.button("Generate Graph"):
        if user_prompt:
            try:
                # Prepare the prompt for the API
                messages = [
                    {"role": "system", "content": "You are a data visualization assistant."},
                    {"role": "user", "content": f"The dataset columns are: {', '.join(df.columns)}. {user_prompt}."}
                ]
                
                # Call OpenAI GPT-4 API
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Use a supported model
                    messages=messages,
                    max_tokens=200,
                    temperature=0.3
                )
                
                # Parse the response
                parsed_response = response['choices'][0]['message']['content']
                st.write("LLM's Interpretation:", parsed_response)

                # Example: Assuming the LLM returns something like this:
                # {"chart_type": "Bar", "x_axis": "Age", "y_axis": "Salary"}
                chart_params = eval(parsed_response)  # Be cautious with eval or replace with `json.loads` if response is in JSON

                # Extract chart details
                chart_type = chart_params.get("chart_type")
                x_axis = chart_params.get("x_axis")
                y_axis = chart_params.get("y_axis")

                # Generate the chart
                if chart_type == "Bar":
                    fig = px.bar(df, x=x_axis, y=y_axis)
                elif chart_type == "Line":
                    fig = px.line(df, x=x_axis, y=y_axis)
                elif chart_type == "Scatter":
                    fig = px.scatter(df, x=x_axis, y=y_axis)
                elif chart_type == "Boxplot":
                    fig = px.box(df, x=x_axis, y=y_axis)
                else:
                    st.write("The LLM could not determine a valid chart type.")

                # Display the graph
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a prompt to generate a graph.")

# Inform user to upload a file
else:
    st.info("Please upload a CSV file to proceed.")

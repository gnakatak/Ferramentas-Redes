import streamlit as st
import requests
import json

def postman_interface():
    """
    Renders a simple HTTP request tool (Postman-like) in Streamlit.
    Allows users to send GET, POST, PUT, and DELETE requests with custom headers and body.
    Displays the response status, headers, and body.
    """
    st.title("Simple HTTP Request Tool (Postman-like)")
    st.write("Make GET, POST, PUT, and DELETE requests to test your APIs.")

    # Input field for the URL
    # Default URL provided for easy testing with a public API
    url = st.text_input("URL", "https://jsonplaceholder.typicode.com/todos/1")

    # Dropdown for selecting the HTTP method
    method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])

    # Section for Headers input
    st.subheader("Headers (JSON format)")
    # Text area for users to input headers as a JSON string
    headers_input = st.text_area("Enter headers as JSON (optional)", "{}")
    
    headers = {}
    try:
        # Attempt to parse the headers input as JSON
        if headers_input:
            headers = json.loads(headers_input)
    except json.JSONDecodeError:
        # Display an error if the JSON is invalid
        st.error("Invalid JSON for headers. Please check your syntax.")
        return # Stop execution if headers are invalid

    # Section for Request Body input (only for POST and PUT methods)
    body = ""
    if method in ["POST", "PUT"]:
        st.subheader("Request Body (JSON format)")
        # Text area for users to input the request body as a JSON string
        # Updated label to explicitly mention "payload"
        body_input = st.text_area("Enter request body (payload) as JSON (optional)", "")
        try:
            # Attempt to parse the body input as JSON
            if body_input:
                body = json.loads(body_input)
        except json.JSONDecodeError:
            # Display an error if the JSON is invalid
            st.error("Invalid JSON for request body (payload). Please check your syntax.")
            return # Stop execution if body is invalid

    # Button to send the request
    if st.button("Send Request"):
        # Basic validation for URL
        if not url:
            st.warning("Please enter a URL.")
            return

        st.info(f"Sending {method} request to {url}...")

        try:
            response = None
            # Perform the request based on the selected method
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                # For POST, the 'json' parameter sends the body as JSON
                response = requests.post(url, headers=headers, json=body)
            elif method == "PUT":
                # For PUT, the 'json' parameter sends the body as JSON
                response = requests.put(url, headers=headers, json=body)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)

            if response:
                # Display the response details
                st.subheader("Response")
                st.write(f"**Status Code:** {response.status_code}")

                st.subheader("Response Headers")
                # Convert response headers to a dictionary and display as JSON
                st.json(dict(response.headers))

                st.subheader("Response Body")
                try:
                    # Try to display the response body as JSON if possible
                    st.json(response.json())
                except json.JSONDecodeError:
                    # If not valid JSON, display as plain text
                    st.text(response.text)
            else:
                st.error("An unexpected error occurred. No response received.")

        # Catch common request exceptions for better error handling
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Could not connect to the URL. Please check the URL and your internet connection.")
        except requests.exceptions.Timeout:
            st.error("Timeout Error: The request timed out.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

# This block allows the module to be run directly for testing purposes

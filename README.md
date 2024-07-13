
# EHS Sign Form Application

## Overview

The EHS Sign Form application is a web-based tool for generating laboratory hazard information signs. Users can fill out a form to input contact information, select laboratory hazards, and generate a PDF sign in either horizontal or vertical orientation.

## Features

- Input and manage contact information for primary, alternate, and principal investigator contacts.
- Select laboratory hazards from a predefined list.
- Generate a PDF of the sign in horizontal or vertical orientation.
- Automatically adjust text formatting and handle form validation.

## Dependencies

The application relies on several Python packages and external libraries to function correctly:

- Flask
- WeasyPrint
- datetime

Additionally, for WeasyPrint to function correctly, you must have the GTK and related libraries installed on your system.

## Installation

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)

### Steps

1. **Clone the Repository**

   ```
   git clone https://github.com/your-username/ehs-sign-form.git
   cd ehs-sign-form
   ```


2. **Set Up Virtual Environment**

   ```
   python -m venv venv
   ```


3. **Activate the Virtual Environment**

   - On Windows:

     ```
     source venv/Scripts/activate
     ```

   - On macOS/Linux:

     ```
     source venv/bin/activate
     ```

4. **Install Python Dependencies**

   ```
   pip install -r requirements.txt
   ```


5. **Install GTK and Related Libraries**

   For Windows users, you can use MSYS2 to install the necessary libraries:

   - Download and install MSYS2 from [msys2.org](https://www.msys2.org/).
   - Open the MSYS2 MinGW 64-bit terminal and run the following commands:

     ```
     pacman -Syu
     pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-cairo mingw-w64-x86_64-gdk-pixbuf2 mingw-w64-x86_64-pango
     ```

   - Ensure MSYS2 paths are included in your system's PATH environment variable:

     
     ```
     export PATH=/c/msys64/mingw64/bin:$PATH
     ```


## Usage

1. **Run the Application**


   ```
   flask run
   ```

   Alternatively, you can run the application using the `python` command:

   ```
   python signapp.py
   ```


2. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:5000`.

3. **Fill Out the Form**

   Enter the required information in the form fields. Select the hazards present in your laboratory. Choose the desired orientation for the PDF sign (horizontal or vertical).

4. **Generate the PDF**

   Click the submit button. The application will process the form data and generate a PDF sign with the specified information.

## Directory Structure

```
ehs-sign-form/
│
├── static/
│   ├── css/
│   │   ├── horizontalstyle.css
│   │   ├── verticalstyle.css
│   └── images/
│       ├── 00EMPTY.png
│       ├── 01radioactive.png
│       ├── ... (other hazard icons)
│
├── templates/
│   ├── index.html
│   ├── horizontal.html
│   └── vertical.html
│
├── venv/ (virtual environment)
│
├── app.py
├── requirements.txt
└── README.md
```

## Requirements File

Here’s an example `requirements.txt` file that lists the necessary Python packages:

```
Flask==3.0.3
WeasyPrint==62.3
```

## Contact Information

For questions, issues, or contributions, please contact [prtruesdell@gmail.com].

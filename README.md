
# EHS Sign Form Application

## Overview

The EHS Sign Form application is intended as a web-based tool for generating laboratory hazard information signs. Users can fill out a form to input contact information, laboratory hazards, and other parameters, and the app will automatically generate a sign as a PDF from pre-formatted HTML/CSS templates. The application can be integrated with EHS systems for accurate and efficient rollout of required signage.

## Features

- Intuitive and responsive user interface
- Automates sign creation, increasing efficiency by 80%

## Dependencies

The application relies on a few Python packages and external libraries to function correctly:

- Flask
- WeasyPrint (for PDF handling)
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
│   │   ├── horiz_bio_style.html
│   │   └── vert_bio_style.html
│   └── images/
│       ├── 00EMPTY.png
│       ├── 01radioactive.png
│       ├── 01radioactive.svg
│       ├── ... (13 other hazard icons)
│
├── templates/
│   ├── index.html
│   ├── horizontal.html
│   ├── vertical.html
│   ├── horiz_bio.html
│   └── vert_bio.html
│
├── venv/ (virtual environment)
│
├── signapp.py
├── requirements.txt
└── README.md
```

## Requirements 

```
Flask==3.0.3
WeasyPrint==62.3
PyInstaller==6.9.0

```

## Contact Information

For questions, issues, or contributions, please contact [prtruesdell@gmail.com].
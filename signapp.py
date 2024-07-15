import os
from flask import Flask, render_template, request, make_response, url_for
from datetime import datetime
from weasyprint import HTML, CSS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='EHS Sign Form')

@app.route('/submit', methods=['POST'])
def submit():
    error_message = None

    # Extract form data for contacts
    pi_first_name = request.form.get('pi_first_name')
    pi_last_name = request.form.get('pi_last_name')
    phone_pi = request.form.get('phone_pi')
    phone_pi_secondary = request.form.get('phone_pi_secondary')

    primary_first_name = request.form.get('primary_first_name')
    primary_last_name = request.form.get('primary_last_name')
    phone_primary = request.form.get('phone_primary')
    phone_secondary = request.form.get('phone_secondary')

    alternate_first_name = request.form.get('alternate_first_name')
    alternate_last_name = request.form.get('alternate_last_name')
    phone_alternate = request.form.get('phone_alternate')
    phone_secondary_alternate = request.form.get('phone_secondary_alternate')

    # Initialize phone output variables
    pi_phone_output = phone_pi
    primary_phone_output = phone_primary

    # Check if alternate contact fields are empty
    if not alternate_first_name and not alternate_last_name and not phone_alternate and not phone_secondary_alternate:
        # If PI and Primary Contact fields are the same
        if (pi_first_name == primary_first_name and
            pi_last_name == primary_last_name and
            phone_pi == phone_primary and
            phone_pi_secondary == phone_secondary):

            # Check if the secondary phone field is empty
            if not phone_pi_secondary:
                # Set an error message if at least two contact numbers are required
                error_message = "At least two contact numbers are required."
            else:
                # Clear alternate contact fields
                alternate_first_name = ''
                alternate_last_name = ''
                phone_alternate = ''
                phone_secondary_alternate = ''
                # Set PI phone output to phone_pi_secondary
                pi_phone_output = phone_pi_secondary
        else:
            # Maintain original phone output variables
            pi_phone_output = phone_pi
            primary_phone_output = phone_primary
    else:
        # If alternate contact fields are not empty, use the user-provided data
        alternate_first_name = request.form['alternate_first_name']
        alternate_last_name = request.form['alternate_last_name']
        phone_alternate = request.form['phone_alternate']
        phone_secondary_alternate = request.form['phone_secondary_alternate']

        # Additional logic for PI and Primary Contact fields
        if phone_pi == phone_primary:
            if not phone_pi_secondary and not phone_secondary:
                # Both PI and Primary Contact fields to be populated with the primary phone
                pi_phone_output = phone_primary
                primary_phone_output = phone_primary
            elif phone_pi_secondary == phone_secondary:
                # Primary Contact field to be populated with the primary phone and PI contact field with the secondary phone
                pi_phone_output = phone_pi_secondary
                primary_phone_output = phone_primary
            else:
                pi_phone_output = phone_primary
                primary_phone_output = phone_primary
        else:
            pi_phone_output = phone_pi
            primary_phone_output = phone_primary

    # If there's an error, render the form with the error message
    if error_message:
        return render_template('index.html', error_message=error_message)

    # Extract form data for Laboratory Hazards
    hazards = {
        'radioactive': '01radioactive.png',
        'xray': '02xray.png',
        'laser': '03laser.png',
        'biohazard': '04BSL2.png',
        'cancer': '05cancer.png',
        'toxic': '06toxic.png',
        'reproductive': '07reproductive_toxin.png',
        'corrosive': '08corrosive.png',
        'ultraviolet': '09ultraviolet.png',
        'flammablem': '10flammable_materials.png',
        'oxidizing': '11oxidizing.png',
        'water': '12water.png',
        'flammableg': '13flammable_gas.png',
        'nflammableg': '14non_flammable_gas.png',
    }

    # Create a list of selected hazard icons with proper URLs
    selected_hazards = [f'{request.host_url}static/images/{hazards[hazard]}' for hazard in hazards if hazard in request.form]

    # Ensure there are 10 icons, filling with EMPTY.png if necessary
    while len(selected_hazards) < 10:
        selected_hazards.append(f'{request.host_url}static/images/00EMPTY.png')

    # Check if PI after-hours phone is the same as the primary contact after-hours phone
    if phone_pi == phone_primary:
        phone_pi = phone_pi_secondary

    # Extract form data for Laboratory Information
    department = request.form['department']
    building = request.form['building']
    room_number = request.form['room_number']

    # Prepare data for the template
    context = {
        'room': room_number,
        'building': building,
        'primary_contact': f"{primary_first_name} {primary_last_name}",
        'primary_phone': primary_phone_output,
        'alternate_contact': f"{alternate_first_name} {alternate_last_name}",
        'alternate_phone': phone_alternate,
        'pi_contact': f"{pi_first_name} {pi_last_name}",
        'pi_phone': pi_phone_output,
        'department': department,
        'date_updated': datetime.today().strftime('%m/%d/%Y'),
        'hazard_icons': selected_hazards  # Use the full URL directly
    }

    # Determine which template to render based on the orientation, default to horizontal
    orientation = request.form.get('orientation', 'horizontal')
    if orientation == 'vertical':
        template = 'vertical.html'
    else:
        template = 'horizontal.html'

    # Render the HTML template with context
    html = render_template(template, **context)

    # Generate PDF from the rendered HTML
    pdf = HTML(string=html, base_url=request.host_url).write_pdf(
        stylesheets=[CSS(string='@page { size: 8.5in 11in; margin: 0in; }')]
    )

    # Print CSS path for debugging
    css_path = url_for('static', filename='css/horizontalstyle.css', _external=True)
    print("CSS path:")
    print(css_path)

    # Create a response to send the PDF back to the client
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=lab_sign.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)

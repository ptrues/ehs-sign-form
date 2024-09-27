import os
from flask import Flask, render_template, request, make_response, url_for
from datetime import datetime
from weasyprint import HTML, CSS

app = Flask(__name__)

# Define your buildings list as before
buildings = [
    {"code": "000", "building": "Institute Of Marine Sciences"},
    # ... (other building entries)
    {"code": "999", "building": "UNC Children's Hospital-Raleigh"}
]

@app.route('/')
def home():
    return render_template('index.html', title='EHS Sign Form', buildings=buildings)

@app.route('/submit', methods=['POST'])
def submit():
    error_message = None

    # Extract form data for contacts
    PI_first_name = request.form.get('PI_first_name')
    PI_last_name = request.form.get('PI_last_name')
    PI_after_hours = request.form.get('PI_phone')  # Corrected mapping
    PI_phone = request.form.get('PI_after_hours')  # Corrected mapping

    primary_first_name = request.form.get('primary_first_name')
    primary_last_name = request.form.get('primary_last_name')
    primary_after_hours = request.form.get('primary_after_hours')
    primary_phone = request.form.get('primary_phone')

    alternate_first_name = request.form.get('alternate_first_name')
    alternate_last_name = request.form.get('alternate_last_name')
    alternate_after_hours = request.form.get('alternate_phone')  # Corrected mapping
    alternate_phone = request.form.get('alternate_after_hours')  # Corrected mapping

    # Initialize a set to track unique phone numbers
    unique_phones = set()

    # Assign phone numbers, prioritizing emergency phones
    primary_phone_output = primary_after_hours
    unique_phones.add(primary_after_hours)

    if PI_after_hours and PI_after_hours not in unique_phones:
        PI_phone_output = PI_after_hours
        unique_phones.add(PI_after_hours)
    else:
        PI_phone_output = PI_phone
        if PI_phone:
            unique_phones.add(PI_phone)

    if alternate_after_hours and alternate_after_hours not in unique_phones:
        alternate_phone_output = alternate_after_hours
        unique_phones.add(alternate_after_hours)
    else:
        alternate_phone_output = alternate_phone
        if alternate_phone:
            unique_phones.add(alternate_phone)

    # Validate at least two unique contact numbers
    if len(unique_phones) < 2:
        error_message = "At least two unique contact numbers are required."
        return render_template(
            'index.html',
            title='EHS Sign Form',
            buildings=buildings,
            error_message=error_message,
            request_form=request.form
        )

    # Extract form data for Laboratory Hazards
    hazards = {
        'radioactive': '01radioactive.svg',
        'xray': '02xray.svg',
        'laser': '03laser.svg',
        'biohazard': '04BSL2.svg',
        'cancer': '05cancer.svg',
        'toxic': '06toxic.svg',
        'reproductive': '07reproductive_toxin.svg',
        'corrosive': '08corrosive.svg',
        'ultraviolet': '09ultraviolet.svg',
        'flammablem': '10flammable_materials.svg',
        'oxidizing': '11oxidizing.svg',
        'water': '12water.svg',
        'flammableg': '13flammable_gas.svg',
        'nflammableg': '14non_flammable_gas.svg',
    }

    # Create a list of selected hazard icons with proper URLs
    selected_hazards = [
        f'{request.host_url}static/images/{hazards[hazard]}'
        for hazard in hazards
        if hazard in request.form
    ]

    # Ensure there are 10 icons, filling with EMPTY.png if necessary
    while len(selected_hazards) < 10:
        selected_hazards.append(f'{request.host_url}static/images/00EMPTY.png')

    # Extract form data for Laboratory Information
    department = request.form.get('department')
    building = request.form.get('building')
    room_number = request.form.get('room_number')

    # Find the building code based on the selected building
    building_code = next((b['code'] for b in buildings if b['building'] == building), 'unknown')

    # Create the filename in the format "code-room_number.pdf"
    filename = f"{building_code}-{room_number}.pdf"

    # Prepare data for the template
    context = {
        'room': room_number,
        'building': building,
        'primary_contact': f"{primary_first_name} {primary_last_name}",
        'primary_phone': primary_phone_output,
        'alternate_contact': f"{alternate_first_name} {alternate_last_name}",
        'alternate_phone': alternate_phone_output,
        'PI_contact': f"{PI_first_name} {PI_last_name}",
        'PI_phone': PI_phone_output,
        'department': department,
        'date_updated': datetime.today().strftime('%m/%d/%Y'),
        'hazard_icons': selected_hazards
    }

    # Determine if 'biohazard' is selected
    biohazard_selected = 'biohazard' in request.form

    # Extract biohazard-specific data if 'biohazard' is selected
    if biohazard_selected:
        # Extract Biosafety Level
        bsl = request.form.get('bsl', 'Not specified')

        # Extract Biological Agents (list of selected options)
        biological_agents = request.form.getlist('biological_agents')

        # If 'Other' is selected, include the specified text
        if 'Other' in biological_agents:
            other_agent = request.form.get('other_biological_agent', '')
            biological_agents = [agent for agent in biological_agents if agent != 'Other']
            if other_agent:
                biological_agents.append(other_agent)

        # Join biological agents into a string
        biological_agents_str = ', '.join(biological_agents) if biological_agents else 'None specified'

        # Extract Vaccines Required (list)
        vaccines = request.form.getlist('vaccines')
        vaccines_str = ', '.join(vaccines) if vaccines else 'None required'

        # Extract Medical Surveillance Required (list)
        medical_surveillance = request.form.getlist('medical_surveillance')
        medical_surveillance_str = ', '.join(medical_surveillance) if medical_surveillance else 'None required'

        # Update context with biohazard-specific data
        context.update({
            'bsl': bsl,
            'biological_agents': biological_agents_str,
            'vaccines': vaccines_str,
            'medical_surveillance': medical_surveillance_str,
        })

    # Render the appropriate template based on orientation and biohazard selection
    orientation = request.form.get('orientation', 'horizontal')

    if biohazard_selected:
        if orientation == 'vertical':
            template = 'vert_bio.html'  # Use your vertical biohazard template
        else:
            template = 'horiz_bio.html'  # Use your horizontal biohazard template
    else:
        if orientation == 'vertical':
            template = 'vertical.html'  # Use your standard vertical template
        else:
            template = 'horizontal.html'  # Use your standard horizontal template

    html = render_template(template, **context)

    # Generate PDF from the rendered HTML
    pdf = HTML(string=html, base_url=request.host_url).write_pdf(
        stylesheets=[CSS(string='@page { size: 8.5in 11in; margin: 0in; }')]
    )

    # Create a response to send the PDF back to the client
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="{filename}"'

    return response

if __name__ == '__main__':
    app.run(debug=True)

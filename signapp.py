import os
from flask import Flask, render_template, request, make_response, url_for
from datetime import datetime
from weasyprint import HTML, CSS

app = Flask(__name__)


buildings = [
{"code": "000", "building": "Institute Of Marine Sciences"},
{"code": "003", "building": "Ackland Art Museum"},
{"code": "004", "building": "Alumni Bldg"},
{"code": "010", "building": "Coker Hall"},
{"code": "013", "building": "Davie Hall"},
{"code": "021", "building": "Howell Hall"},
{"code": "026", "building": "Manning Hall"},
{"code": "029", "building": "Mitchell Hall"},
{"code": "039", "building": "Phillips Hall"},
{"code": "041", "building": "Coastal Proc. Env. Health Lab"},
{"code": "046", "building": "Wilson Hall"},
{"code": "048", "building": "Fordham Hall"},
{"code": "069", "building": "Kenan Labs"},
{"code": "079", "building": "Hanes Art Center"},
{"code": "081", "building": "Morehead Chemistry Labs"},
{"code": "086", "building": "Caudill Labs"},
{"code": "087", "building": "Chapman Hall"},
{"code": "094", "building": "IMS Fisheries Research Lab"},
{"code": "152", "building": "Morehead Planetarium"},
{"code": "165", "building": "Franklin Street, 134 E."},
{"code": "200", "building": "Beard Hall"},
{"code": "201", "building": "Rosenau Hall"},
{"code": "202", "building": "MacNider Hall"},
{"code": "204", "building": "UNC Hospitals"},
{"code": "207", "building": "Medical School Wing B"},
{"code": "208", "building": "Medical School Wing D"},
{"code": "209", "building": "First Dental"},
{"code": "210A", "building": "Koury OHS"},
{"code": "211", "building": "Brauer Hall"},
{"code": "212", "building": "Francis Owen Blood Research Lab"},
{"code": "214", "building": "Carrington Hall"},
{"code": "217", "building": "Taylor Hall"},
{"code": "219", "building": "Berryhill Hall"},
{"code": "221", "building": "Medical School Wing C"},
{"code": "228", "building": "Brinkhous-Bullitt Bldg"},
{"code": "229", "building": "Burnett-Womack Bldg"},
{"code": "231", "building": "Mary Ellen Jones"},
{"code": "236", "building": "Glaxo Research Building"},
{"code": "237", "building": "Lineberger Cancer Research Center"},
{"code": "238", "building": "McGavran-Greenberg Hall"},
{"code": "239", "building": "Baity Lab"},
{"code": "240", "building": "Aycock Family Medicine"},
{"code": "242", "building": "Thurston-Bowles Bldg"},
{"code": "243", "building": "EPA Bldg"},
{"code": "245", "building": "Neurosciences Research Bldg"},
{"code": "247", "building": "Medical Biomolecular Research Bldg"},
{"code": "327", "building": "Medical Research Bldg B"},
{"code": "351", "building": "NeuroSciences Hospital"},
{"code": "357", "building": "Kerr Hall"},
{"code": "358", "building": "Hooker Research Center"},
{"code": "359", "building": "Genetic Medicine Research Bldg"},
{"code": "360", "building": "Marsico Hall"},
{"code": "363", "building": "Roper Hall"},
{"code": "462", "building": "Art Studio Bldg"},
{"code": "468", "building": "Fetzer Hall"},
{"code": "469", "building": "Taylor Campus Health"},
{"code": "491", "building": "Franklin Square"},
{"code": "605A", "building": "UNC Heart Center at Meadowmont"},
{"code": "614", "building": "Smith Middle School Addition"},
{"code": "625", "building": "ITS Manning"},
{"code": "649", "building": "Environment, Health And Safety Bldg"},
{"code": "658", "building": "Houpt Physician Office Building"},
{"code": "673", "building": "Kannapolis Nutrition Research"},
{"code": "674", "building": "Murray Hall"},
{"code": "676", "building": "Genome Sciences Building"},
{"code": "709C", "building": "Market St, 100 - Southern Village"},
{"code": "745", "building": "Venable Hall"},
{"code": "940", "building": "UNC Eastowne Medical Office Building"},
{"code": "950", "building": "UNC-IDSS"},
{"code": "961A", "building": "Southport Building 2"},
{"code": "980N", "building": "Carolina Crossing B"},
{"code": "980R", "building": "Carolina Crossing C"},
{"code": "984Q", "building": "Quadrangle 6101"},
{"code": "998C", "building": "121 S Estes Drive"},
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
    PI_phone = request.form.get('PI_phone')
    PI_after_hours = request.form.get('PI_after_hours')

    primary_first_name = request.form.get('primary_first_name')
    primary_last_name = request.form.get('primary_last_name')
    primary_phone = request.form.get('primary_phone')
    primary_after_hours = request.form.get('primary_after_hours')

    alternate_first_name = request.form.get('alternate_first_name')
    alternate_last_name = request.form.get('alternate_last_name')
    alternate_phone = request.form.get('alternate_phone')
    alternate_after_hours = request.form.get('alternate_after_hours')

    # Initialize phone output variables for PI and Primary Contact
    primary_phone_output = primary_after_hours or primary_phone
    PI_phone_output = PI_after_hours if PI_after_hours != primary_after_hours else PI_phone

    # Initialize a set to track unique phone numbers
    unique_phones = set([primary_phone_output, PI_phone_output])

    # Check for two unique phone numbers initially
    if len(unique_phones) < 2:
        error_message = "At least two unique contact numbers are required."
        return render_template('index.html', title='EHS Sign Form', buildings=buildings, error_message=error_message, request_form=request.form)

    # Assign the alternate contact's phone only if it's unique
    if alternate_phone not in unique_phones:
        alternate_phone_output = alternate_phone
        unique_phones.add(alternate_phone)
    else:
        # Try to use the alternate's emergency phone if it's unique
        if alternate_after_hours and alternate_after_hours not in unique_phones:
            alternate_phone_output = alternate_after_hours
            unique_phones.add(alternate_after_hours)
        else:
            # If neither alternate phone is unique, assign a unique phone from PI or Primary Contact
            if PI_phone not in unique_phones:
                alternate_phone_output = PI_phone
                unique_phones.add(PI_phone)
            elif PI_after_hours not in unique_phones:
                alternate_phone_output = PI_after_hours
                unique_phones.add(PI_after_hours)
            elif primary_phone not in unique_phones:
                alternate_phone_output = primary_phone
                unique_phones.add(primary_phone)
            elif primary_after_hours not in unique_phones:
                alternate_phone_output = primary_after_hours
                unique_phones.add(primary_after_hours)
            else:
                error_message = "At least two unique contact numbers are required."
                return render_template('index.html', title='EHS Sign Form', buildings=buildings, error_message=error_message, request_form=request.form)

    # Final validation to ensure two unique phone numbers are present
    if len(unique_phones) < 2:
        error_message = "At least two unique contact numbers are required."
        return render_template('index.html', title='EHS Sign Form', buildings=buildings, error_message=error_message, request_form=request.form)

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
    selected_hazards = [f'{request.host_url}static/images/{hazards[hazard]}' for hazard in hazards if hazard in request.form]

    # Ensure there are 10 icons, filling with EMPTY.png if necessary
    while len(selected_hazards) < 10:
        selected_hazards.append(f'{request.host_url}static/images/00EMPTY.png')

    # Extract form data for Laboratory Information
    department = request.form.get('department')
    building = request.form.get('building')
    room_number = request.form.get('room_number')

    # Find the building code based on the selected building
    building_code = next((b['code'] for b in buildings if b['building'] == building), 'unknown')

    # Create the filename in the format "code-room_number"
    filename = f"{building_code}-{room_number}.pdf"

    # Prepare data for the template
    context = {
        'room': room_number,
        'building': building,
        'primary_contact': f"{primary_first_name} {primary_last_name}",
        'primary_phone': primary_phone_output,
        'alternate_contact': f"{alternate_first_name} {alternate_last_name}",
        'alternate_phone': alternate_phone_output,  # Updated to use the correct variable
        'PI_contact': f"{PI_first_name} {PI_last_name}",
        'PI_phone': PI_phone_output,
        'department': department,
        'date_updated': datetime.today().strftime('%m/%d/%Y'),
        'hazard_icons': selected_hazards
    }


    # Render the appropriate template based on the orientation
    orientation = request.form.get('orientation', 'horizontal')
    template = 'vertical.html' if orientation == 'vertical' else 'horizontal.html'
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
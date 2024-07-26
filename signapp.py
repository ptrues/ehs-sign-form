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

    # Check if PI after-hours phone is the same as the primary contact after-hours phone
    if phone_pi == phone_primary:
        phone_pi = phone_pi_secondary

    # Extract form data for Laboratory Information
    department = request.form['department']
    building = request.form['building']
    room_number = request.form['room_number']

    # Find the building code based on the selected building
    building_code = next((b['code'] for b in buildings if b['building'] == building), 'unknown')

    # Create the filename in the format "code-room_number"
    filename = f"{building_code}-{room_number}.pdf"

    # Debugging print statements
    print(f"Building: {building}")
    print(f"Building Code: {building_code}")
    print(f"Room Number: {room_number}")
    print(f"Filename: {filename}")

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

    # Create a response to send the PDF back to the client
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="{filename}"'

    return response

if __name__ == '__main__':
    app.run(debug=True)

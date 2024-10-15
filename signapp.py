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
    return render_template('index.html', buildings=buildings)

@app.route('/submit', methods=['POST'])
def submit():
    error_message = None

    # Extract form data for contacts
    PI_first_name = request.form.get('PI_first_name')
    PI_last_name = request.form.get('PI_last_name')
    PI_emergency_phone = request.form.get('PI_phone')  
    PI_regular_phone = request.form.get('PI_after_hours') 

    primary_first_name = request.form.get('primary_first_name')
    primary_last_name = request.form.get('primary_last_name')
    primary_emergency_phone = request.form.get('primary_after_hours')
    primary_regular_phone = request.form.get('primary_phone')

    alternate_first_name = request.form.get('alternate_first_name')
    alternate_last_name = request.form.get('alternate_last_name')
    alternate_emergency_phone = request.form.get('alternate_phone')  
    alternate_regular_phone = request.form.get('alternate_after_hours')  

    # Initialize a set to track unique phone numbers
    unique_phones = set()

    # Assign phone numbers, prioritizing emergency phones
    primary_phone_output = primary_emergency_phone
    unique_phones.add(primary_emergency_phone)

    if PI_emergency_phone and PI_emergency_phone not in unique_phones:
        PI_phone_output = PI_emergency_phone
        unique_phones.add(PI_emergency_phone)
    else:
        PI_phone_output = PI_regular_phone
        if PI_regular_phone:
            unique_phones.add(PI_regular_phone)

    if alternate_emergency_phone and alternate_emergency_phone not in unique_phones:
        alternate_phone_output = alternate_emergency_phone
        unique_phones.add(alternate_emergency_phone)
    else:
        alternate_phone_output = alternate_regular_phone
        if alternate_regular_phone:
            unique_phones.add(alternate_regular_phone)

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
        'biohazard': '04biohazard.svg',
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
        selected_agents = request.form.getlist('biological_agents')

        # If 'Other' is selected, include the specified text
        if 'Other' in selected_agents:
            other_agent = request.form.get('other_biological_agent', '')
            selected_agents = [agent for agent in selected_agents if agent != 'Other']
            if other_agent:
                selected_agents.append(other_agent)

        # Define the mapping of subcategories to main categories
        agent_mapping = {
            'Animal Source Material': {
                'Animal source material (clinical specimens)': 'clinical specimens',
                'Animal source material (tissue/cell culture)': 'tissue/cell culture',
                'Animal source material (other)': 'other',
            },
            'Human Source Material': {
                'Human source material (clinical specimens)': 'clinical specimens',
                'Human source material (tissue/cell culture)': 'tissue/cell culture',
                'Human source material (other)': 'other',
            },
            'Non-Human Primate Source Material': {
                'Non-human primate source material (R. macaque derived)': 'R. macaque derived',
                'Non-human primate source material (other)': 'other',
            },
            'Fungi': {
                'Fungi (culturing)': 'culturing',
                'Fungi (bioassay/other)': 'bioassay/other',
            },
            'Bacteria': {
                'Bacteria (culturing)': 'culturing',
                'Bacteria (bioassay/other)': 'bioassay/other',
            },
            'Virus': {
                'Virus (culturing)': 'culturing',
                'Virus (bioassay/other)': 'bioassay/other',
            },
            'Recombinant/Synthetic Nucleic Acids': {
                'Plasmids': 'plasmids',
                'Viral vectors': 'viral vectors',
                'Recombinant/synthetic nucleic acids (other)': 'other',
            },
            'Other Biological Agents': {
                'Biological toxin': 'biological toxin',
                'Prions': 'prions',
                # 'Other' is handled separately
            },
        }

        # Initialize a dictionary to hold the grouped agents
        grouped_agents = {}

        # Process selected agents
        for agent in selected_agents:
            found = False
            for main_category, subcategories in agent_mapping.items():
                if agent in subcategories:
                    found = True
                    if main_category not in grouped_agents:
                        grouped_agents[main_category] = []
                    grouped_agents[main_category].append(subcategories[agent])
                    break
            if not found:
                # Handle agents not in the mapping (e.g., 'Other' specified by the user)
                if 'Other' not in grouped_agents:
                    grouped_agents['Other'] = []
                grouped_agents['Other'].append(agent)

        # Build the formatted string
        biological_agents_list = []
        for main_category, subcats in grouped_agents.items():
            subcats_str = ', '.join(subcats)
            biological_agents_list.append(f"{main_category} ({subcats_str})")
        biological_agents_str = ', '.join(biological_agents_list)

        # Define the vaccine abbreviation mapping
        vaccine_abbreviations = {
            'Anthrax': 'Anthrax',
            'Bacille Calmette-Guérin (BCG)/ Tuberculosis (TB) Disease': 'BCG/TB',
            'Cholera': 'Cholera',
            'COVID-19 Vaccine and Current Booster': 'COVID-19',
            'DTaP/Tdap/Td (Pertussis, Tetanus, and Diphtheria)': 'DTaP/Tdap/Td',
            'Hepatitis A': 'HepA',
            'Hepatitis B': 'HepB',
            'Hib (Haemophilus Influenzae type B)': 'Hib',
            'Human Papillomavirus (HPV)': 'HPV',
            'Influenza': 'Flu',
            'Japanese Encephalitis': 'JE',
            'MMR (Measles, Mumps and Rubella)': 'MMR',
            'MMRV (Measles, Mumps, Rubella, and Varicella)': 'MMRV',
            'Meningococcal': 'Meningococcal',
            'Pertussis': 'Pertussis',
            'Pneumococcal': 'Pneumococcal',
            'Polio': 'Polio',
            'Rabies': 'Rabies',
            'Rotavirus': 'RV',
            'Vaccinia (Smallpox) Vaccine': 'Smallpox',
            'Tetanus': 'Tetanus',
            'Tick-borne Encephalitis Virus (TBEV)': 'TBE',
            'Typhoid (Salmonella serotype Typhi)': 'Typhoid',
            'Varicella (Chickenpox)': 'VAR',
            'Yellow Fever': 'YF',
            'Zoster (Shingles)': 'Zoster (Shingles)',
        }

        # Extract Vaccines Required (list)
        vaccines = request.form.getlist('vaccines')

        # Map the selected vaccines to their abbreviations
        abbreviated_vaccines = [vaccine_abbreviations.get(vaccine, vaccine) for vaccine in vaccines]

        vaccines_str = ', '.join(abbreviated_vaccines) if abbreviated_vaccines else ''

        # Extract Medical Surveillance Required (list)
        medical_surveillance = request.form.getlist('medical_surveillance')
        medical_surveillance_str = ', '.join(medical_surveillance) if medical_surveillance else ''

        # Combine vaccines and medical surveillance into a single string
        if not vaccines and not medical_surveillance:
            occupational_health_requirements = 'None required'
        else:
            # Create a list to hold the selected items
            ohr_list = []
            if vaccines_str:
                ohr_list.append(f"Vaccines ({vaccines_str})")
            if medical_surveillance_str:
                ohr_list.append(f"Medical Surveillance ({medical_surveillance_str})")
            occupational_health_requirements = ', '.join(ohr_list)

        # Update context with biohazard-specific data
        context.update({
            'bsl': bsl,
            'biological_agents': biological_agents_str,
            'occupational_health_requirements': occupational_health_requirements,
        })
    

    # Render the appropriate template based on orientation and biohazard selection
    orientation = request.form.get('orientation', 'horizontal')

    if biohazard_selected:
        if orientation == 'vertical':
            template = 'vert_bio.html'  # Use vertical biohazard template
        else:
            template = 'horiz_bio.html'  # Use horizontal biohazard template
    else:
        if orientation == 'vertical':
            template = 'vertical.html'  # Use standard vertical template
        else:
            template = 'horizontal.html'  # Use standard horizontal template

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

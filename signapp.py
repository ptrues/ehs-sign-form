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
    # Extract form data for PI (Principal Investigator)
    pi_first_name = request.form['pi_first_name']
    pi_last_name = request.form['pi_last_name']
    phone_pi = request.form['phone_pi']
    phone_emer = request.form.get('phone_emer')

    # Extract form data for Primary Contact
    primary_first_name = request.form['primary_first_name']
    primary_last_name = request.form['primary_last_name']
    phone_primary = request.form['phone_primary']
    phone_secondary = request.form.get('phone_secondary')

    # Extract form data for Alternate Contact
    alternate_first_name = request.form.get('alternate_first_name')
    alternate_last_name = request.form.get('alternate_last_name')
    phone_alternate = request.form.get('phone_alternate')
    phone_secondary_alternate = request.form.get('phone_secondary_alternate')

    # Extract form data for Laboratory Information
    department = request.form['department']
    building = request.form['building']
    room_number = request.form['room_number']

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

    # Print paths for debugging
    print("Selected hazard icons paths:")
    for hazard in selected_hazards:
        print(url_for('static', filename=f'images/{hazard}', _external=True))

    # Ensure there are 10 icons, filling with EMPTY.png if necessary
    while len(selected_hazards) < 10:
        selected_hazards.append(f'{request.host_url}static/images/00EMPTY.png')

    # Prepare data for the template
    context = {
        'room': room_number,
        'building': building,
        'primary_contact': f"{primary_first_name} {primary_last_name}",
        'primary_phone': phone_primary,
        'alternate_contact': f"{alternate_first_name} {alternate_last_name}",
        'alternate_phone': phone_alternate,
        'pi_contact': f"{pi_first_name} {pi_last_name}",
        'pi_phone': phone_pi,
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

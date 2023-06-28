from flask import Flask, render_template, request, send_file, send_from_directory
import qrcode
import zipfile
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', nb_series=2)

@app.route('/generate', methods=['POST'])
def generate():
    nb_series = int(request.form['nb_series'])
    series_names = [request.form.get(f'series_name_{i}', f"Série {i+1}") for i in range(nb_series)]
    qrcodes_counts = [int(request.form.get(f'qrcodes_count_{i}', 0)) for i in range(nb_series)]
    start_numbers = [int(request.form.get(f'start_number_{i}', 1)) for i in range(nb_series)]

    zip_filename = 'qrcodes.zip'  # Nom du fichier ZIP

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for serie in range(nb_series):
            series_name = series_names[serie]
            qrcodes_count = qrcodes_counts[serie]
            start_number = start_numbers[serie]

            for compteur in range(start_number, start_number + qrcodes_count):
                prefixe = series_name
                data = f"{prefixe} numéro: {compteur}"
                filename = f"{prefixe}_{compteur}.png"

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                img.save(filename)
                print(f"QR Code {compteur} généré : {filename}")

                # Ajouter le fichier au fichier ZIP
                zip_file.write(filename)

    return f'/download/{zip_filename}'


@app.route('/generate_single', methods=['POST'])
def generate_single():
    series_name = request.form.get('series_name', "Série unique")
    start_number = int(request.form.get('start_number', 1))

    zip_filename = 'qrcodes.zip'  # Nom du fichier ZIP

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        prefixe = series_name
        data = f"{prefixe} numéro: {start_number}"
        filename = f"{prefixe}_{start_number}.png"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR Code généré : {filename}")

        # Ajouter le fichier au fichier ZIP
        zip_file.write(filename)

    return f'/download/{zip_filename}'

        # return 'Les codes QR ont été générés avec succès !'

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    directory = os.path.dirname(__file__)
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

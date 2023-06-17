from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', nb_series=1)

@app.route('/generate', methods=['POST'])
def generate():
    nb_series = int(request.form['nb_series'])
    series_names = [request.form.get(f'series_name_{i}', f"Série {i+1}") for i in range(nb_series)]
    qrcodes_counts = [int(request.form.get(f'qrcodes_count_{i}', 0)) for i in range(nb_series)]

    for serie in range(nb_series):
        series_name = series_names[serie]
        qrcodes_count = qrcodes_counts[serie]

        for compteur in range(1, qrcodes_count + 1):
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

    return 'Les codes QR ont été générés avec succès !'

if __name__ == '__main__':
    app.run(debug=True)

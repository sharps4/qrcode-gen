from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

def generer_qrcodes(nb_total, series):
    compteur = 1
    serie_index = 0

    for i in range(nb_total):
        if compteur > series[serie_index]['nombre']:
            serie_index = (serie_index + 1) % len(series)
            compteur = 1

        prefixe = series[serie_index]['prefixe']
        nom_serie = series[serie_index]['nom']

        data = f"Données du code QR {compteur} de la série {nom_serie}"
        filename = f"{prefixe}_{compteur}_serie{nom_serie}.png"

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
        print(f"Code QR {compteur} de la série {nom_serie} généré : {filename}")

        compteur += 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nb_total = int(request.form['nb_total'])
        series = []

        nb_series = request.form.get('nb_series', 0, type=int)

        for i in range(nb_series):
            prefixe = request.form[f"prefixe_{i+1}"]
            nom = request.form[f"nom_{i+1}"]
            nombre = int(request.form[f"nombre_{i+1}"])

            series.append({
                'prefixe': prefixe,
                'nom': nom,
                'nombre': nombre
            })

        generer_qrcodes(nb_total, series)
        return render_template('result.html', nb_total=nb_total)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

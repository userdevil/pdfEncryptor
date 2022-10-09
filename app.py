from flask import*
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
name = ""
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/success', methods = ['GET', 'POST'])
def display_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        passwrd = request.form["pass"]
        ent = "Encrypted-"+filename


        f.save(app.config['UPLOAD_FOLDER'] + filename)

        path = app.config['UPLOAD_FOLDER'] + filename

        from PyPDF2 import PdfFileWriter, PdfFileReader


        pdfwriter = PdfFileWriter()
        pdf = PdfFileReader(path)
        for page_num in range(pdf.numPages):
            pdfwriter.addPage(pdf.getPage(page_num))
        passw = passwrd


        pdfwriter.encrypt(passw)
        with open(ent, 'wb') as f:
            pdfwriter.write(f)
            flash(u'File Encrypted Sucessfully')
    return send_file(ent, as_attachment=True)

@app.errorhandler(500)
def server_error(e):
    return template_rendered("500.html"),500

@app.errorhandler(404)
def resource_not_found(e):
    return render_template("404.html"), 404

@app.route('/sitemap.xml')
def site_map():
  return render_template("sitemape.xml")

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

import os
from datetime import timezone
from flask import render_template, redirect, url_for, request, send_from_directory
from transliterate import translit, exceptions
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import UploadForm
from app.generators import generate_short_link
from app.models import Image

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        image = form.image.data
        deletion_date = form.deletion_date.data
        deletion_date_utc = deletion_date.astimezone(timezone.utc) if deletion_date else None # convert deletion date to UTC

        short_link = generate_short_link()

        # transliterate image filename to latin
        try:
            trans_filename = translit(image.filename, reversed=True)
        # ignore transliteraing if image filename already latin
        except exceptions.LanguageDetectionError:
            trans_filename = image.filename
        
        filename = secure_filename(trans_filename)

        # create folder for uploaded image
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], short_link)
        os.makedirs(upload_folder, exist_ok=True)

        # save image in created folder
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        # add image to database
        new_image = Image(filename=filename, short_link=short_link, deletion_date=deletion_date_utc)
        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('image_page', short_link=short_link))
    allowed_extensions = sorted(app.config['ALLOWED_EXTENSIONS'])
    return render_template('upload.html', title='Upload Image', form=form, allowed_extensions=allowed_extensions)

@app.route('/gallery')
def gallery():
    if app.config['ENABLE_GALLERY'] != 1:
        return redirect(url_for('index'))
    image_counter = Image.query.count()
    page = request.args.get('page', 1, type=int)
    pagination = Image.query.order_by(Image.id.desc()).paginate(page=page, per_page=app.config['GALLERY_IMAGES_PER_PAGE'], error_out=False)
    images = pagination.items
    return render_template('gallery.html', title='Gallery', image_counter=image_counter, pagination=pagination, images=images)

@app.route('/<short_link>')
def image_page(short_link):
    image = Image.query.filter_by(short_link=short_link).first_or_404()
    clear_filename = os.path.splitext(os.path.basename(image.filename))[0]
    short_link = request.base_url
    full_image_link = f"{short_link}/{image.filename}"
    return render_template('image_page.html', title=clear_filename, image=image, clear_filename=clear_filename, short_link=short_link, full_image_link=full_image_link)

@app.route('/<short_link>/<filename>')
def uploaded_image(short_link, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], short_link)
    return send_from_directory(os.path.abspath(directory), filename)
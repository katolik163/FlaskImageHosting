from datetime import datetime, timezone
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, DateTimeLocalField, SubmitField
from wtforms.validators import Optional
from app import app

class UploadForm(FlaskForm):
    image = FileField('Choose Image', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_EXTENSIONS'], 'Images only!')])
    deletion_date = DateTimeLocalField('Deletion Time (Optional)', validators=[Optional()], format='%Y-%m-%dT%H:%M', render_kw={'min': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')})
    submit = SubmitField('Upload')
import os
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone

def delete_expired_images(app, db):
    from app.models import Image

    with app.app_context():
        expired_images = Image.query.filter(Image.deletion_date < datetime.now(timezone.utc)).all()
        for image in expired_images:
            try:
                image_directory = os.path.join(app.config['UPLOAD_FOLDER'], image.short_link)
                image_path = os.path.abspath(image_directory) + '/' + image.filename
                
                if os.path.exists(image_path):
                    os.remove(image_path)
                    
                if os.path.exists(image_directory) and not os.listdir(image_directory):
                    shutil.rmtree(image_directory)

                db.session.delete(image)
                db.session.commit()
            except FileNotFoundError:
                pass # ignore FileNotFoundError

def init_scheduler(app, db):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_expired_images, trigger="cron", second=0, args=[app, db])
    scheduler.start()
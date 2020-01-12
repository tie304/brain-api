
from modules.image_collector import GoogleImageCollector


def gather_google_images(project, subclass, search_term, max_images, username):
    try:
        GoogleImageCollector(project=project, subclass=subclass, search_term=search_term, max_images=max_images, username=username).collect_images()
    except Exception as e:
        print('failed gathering images images,', e)

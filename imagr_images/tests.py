from django.test import TestCase
from models import Photo, Album
from imagr_users.models import ImagrUser
from imagr_images.models import get_file_owner_username
from admin import PhotoAdmin, AlbumAdmin, ImageSizeListFilter
from django.contrib.admin.sites import AdminSite
import datetime
# Create your tests here.


class ImagrTests(TestCase):

    def setUp(self):
        ImagrUser.objects.create(username='testuser')
        test_user = ImagrUser.objects.get(username='testuser')
        Photo.objects.create(
            image='test.png',
            title='test image',
            owner=test_user,
            published=1)
        Album.objects.create(
            title='test album',
            owner=test_user,
            published=1,
            )
        self.site = AdminSite()

    def test_get_file_owner(self):
        test_photo = Photo.objects.get(title='test image')
        test_filename = '/usr/john/photos/test.png'
        result = get_file_owner_username(test_photo, test_filename)
        today = datetime.datetime.utcnow()
        expected = 'testuser/{}/{}/{}'.format(unicode(today.year), unicode(today.month), u'test.png')
        self.assertEquals(result, expected)

    def test_photo_save(self):
        test_photo = Photo.objects.get(title='test image')
        self.assertGreater(test_photo.image_size, 0)

    def test_album_owner_link(self):
        test_album = Album.objects.get(title='test album')
        expected = "<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(
            test_album.owner.id,
            test_album.owner)
        test_album_admin = AlbumAdmin(test_album, self.site)
        self.assertEquals(test_album_admin.owner_link(test_album), expected)

    def test_photo_owner_link(self):
        test_photo = Photo.objects.get(title='test image')
        expected = "<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(
            test_photo.owner.id,
            test_photo.owner)
        test_photo_admin = AlbumAdmin(test_photo, self.site)
        self.assertEquals(test_photo_admin.owner_link(test_photo), expected)
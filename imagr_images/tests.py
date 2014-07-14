from django.test import TestCase
from models import Photo, Album
from imagr_users.models import ImagrUser
from imagr_images.models import get_file_owner_username
from admin import PhotoAdmin, AlbumAdmin, ImageSizeListFilter
from django.core.urlresolvers import reverse
from django.contrib.admin.sites import AdminSite
import datetime
from django.test.utils import setup_test_environment
setup_test_environment()
from django.test.client import Client
client = Client()

class ImagrTests(TestCase):

    def setUp(self):
        u1 = ImagrUser.objects.create(username='testuser')
        u2 = ImagrUser.objects.create(username='testuser2')
        u3 = ImagrUser.objects.create(username='testuser3')

        u1.follow(u2)
        u1.follow(u3)

        Photo.objects.create(
            image='test.png',
            title='u1 test image',
            owner=u1,
            published=1)
        Photo.objects.create(
            image='test.png',
            title='u2 test image',
            owner=u2,
            published=1)
        Photo.objects.create(
            image='test.png',
            title='u3 test image',
            owner=u3,
            published=1)
        Album.objects.create(
            title='test album',
            owner=u1,
            published=1,
            )
        self.site = AdminSite()

    def test_get_file_owner(self):
        test_photo = Photo.objects.get(title='u1 test image')
        self.assertEqual(isinstance(test_photo, Photo), True)
        test_filename = '/garbage/garbage/garbage/test.png'
        result = get_file_owner_username(test_photo, test_filename)
        today = datetime.datetime.utcnow()
        expected = 'testuser/{}/{}/{}'.format(unicode(today.year), unicode(today.month), u'test.png')
        self.assertEquals(result, expected)

    def test_photo_save(self):
        test_photo = Photo.objects.get(title='u1 test image')
        self.assertGreater(test_photo.image_size, 0)

    def test_album_owner_link(self):
        test_album = Album.objects.get(title='test album')
        expected = "<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(
            test_album.owner.id,
            test_album.owner)
        test_album_admin = AlbumAdmin(test_album, self.site)
        self.assertEquals(test_album_admin.owner_link(test_album), expected)

    def test_photo_owner_link(self):
        test_photo = Photo.objects.get(title='u1 test image')
        expected = "<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(
            test_photo.owner.id,
            test_photo.owner)
        test_photo_admin = AlbumAdmin(test_photo, self.site)
        self.assertEquals(test_photo_admin.owner_link(test_photo), expected)

    def test_view_stream_page(self):

        #client.logout()
        user = ImagrUser.objects.get(username='testuser')
        client.logout()
        #client.login()
        # self.assertEqual(client.session['_auth_user_id'], user.pk)
        response = client.get(reverse('stream_page'))
        self.assertEquals(response.status_code, 200)
        actual_photos = response.context['photos']
        self.assertEquals(len(actual_photos), 3)
        self.assertEquals(actual_photos[0].title, 'u3 test image')
        self.assertEquals(actual_photos[1].title, 'u2 test image')
        self.assertEquals(actual_photos[2].title, 'u1 test image')

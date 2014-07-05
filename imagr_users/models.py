from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

FOLLOWER_STATUSES = (
    (0, u'not following'),
    (1, u'left following right'),
    (2, u'right following left'),
    (3, u'both following'),
)

FOLLOWER_SYMBOLS = {
    0: u' x ',
    1: u' ->',
    2: u'<- ',
    3: u'<->',
}


class ImagrUser(AbstractUser):
    relationships = models.ManyToManyField(
        'imagr_users.ImagrUser',
        related_name="+",
        symmetrical=False,
        through='imagr_users.Relationship',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'user'
        verbose_name_plural = u'users'

    def __unicode__(self):
        if self.first_name and self.last_name:
            name = self.get_full_name()
        else:
            name = self.username
        return name

    def follow(self, other):
        """Self follows other

        This action will create a relationship between self and other if it
        does not already exist
        """

    def unfollow(self, other):
        """Self stops following other

        This action will not remove existing relationship objects, but only
        appropriately set the follower status of existing relationships
        """
        raise NotImplementedError

    def request_friendship(self, other):
        """Self requests a friendship with other

        This will not create a relationship if one does not already exist
        """
        raise NotImplementedError

    def accept_friendship(self, other):
        """Self accepts a friendship request from other

        This action will create a relationship between self and other if it
        does not already exist
        """
        raise NotImplementedError

    def end_friendship(self, other):
        """Self terminates friendship with other
        """
        raise NotImplementedError

    def friends(self):
        """Return queryset of self's friends"""
        friends = ImagrUser.objects.filter(
            (Q(relationships_from__right=self) &
             Q(relationships_from__friendship__exact=True)) |
            (Q(relationships_to__left=self) &
             Q(relationships_to__friendship__exact=True))
        )
        return friends

    def followers(self):
        """Return queryset of self's followers"""
        # people who are following and are left in the relationship

        left_followers = (
            Q(relationships_from__right=self) &
            Q(relationships_from__follower_status__in=[1, 3])
        )
        right_followers = (
            Q(relationships_to__left=self) &
            Q(relationships_to__follower_status__in=[2, 3])
        )
        followers = ImagrUser.objects.filter(
            Q(left_followers | right_followers)
        )
        return followers

    def following(self):
        """Return queryset of those self is following"""
        following_left = (
            Q(relationships_to__left=self) &
            Q(relationships_to__follower_status__in=[1, 3]))
        following_right = (
            Q(relationships_from__right=self) &
            Q(relationships_from__follower_status__in=[2, 3])
        )
        following = ImagrUser.objects.filter(
            Q(following_left | following_right)
        )
        return following


class Relationship(models.Model):
    left = models.ForeignKey('imagr_users.ImagrUser', related_name='relationships_from')
    right = models.ForeignKey('imagr_users.ImagrUser', related_name='relationships_to')
    follower_status = models.IntegerField(choices=FOLLOWER_STATUSES)
    friendship = models.NullBooleanField(null=True, blank=True)

    def __unicode__(self):
        symbol = FOLLOWER_SYMBOLS.get(self.follower_status, ' - ')
        representation = u'{} {} {}'.format(
            unicode(self.left), symbol, unicode(self.right))
        if self.friendship:
            representation = representation.replace(u'-', u'F')
        return representation

    def clean(self):
        left = self.left
        right = self.right
        l2r = Q(left=left) & Q(right=right)
        r2l = Q(left=right) & Q(right=left)
        if self.__class__.objects.filter(Q(l2r | r2l)).exists():
            msg = u"A relationship already exists between {} and {}"
            raise ValidationError(msg.format(left, right))

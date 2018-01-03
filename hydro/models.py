from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

# @receiver(post_save, sender=Model, dispatch_uid="model_postsave")
# def model_postsave(sender, instance, created, **kwargs):
# 	pass
#
#
# class Model(models.Model):
# 	pass


class AdjustmentRequest(models.Model):
    fullname = models.CharField(max_length=25, null=False, default='')
    date_requested = models.IntegerField(null=False)
    reason = models.CharField(max_length=10, null=False, default='')
    date = models.DateTimeField()
    explanation = models.TextField(max_length=400, null=True)
    approval = models.BooleanField(default=False)


class AdminSettings(models.Model):
    default_day = models.IntegerField(null=True)
    num_sliders = models.IntegerField(null=True)
    num_lc_sliders = models.IntegerField(null=True)
    num_mins_count_active = models.IntegerField(null=True)
    second_semester_to_publish = models.IntegerField(null=True)
    ldap_users_login = models.IntegerField(null=True)
    disabled = models.IntegerField(null=True)
    default_semester = models.IntegerField(null=True)


class Audit(models.Model):
    employee = models.ForeignKey('Employee', null=True)
    original_timestamp = models.DateTimeField(null=True)
    original_note = models.CharField(max_length=25, null=True)
    manager = models.CharField(max_length=25, null=True)
    new_timestamp = models.DateTimeField(null=True)
    new_note = models.CharField(max_length=25, null=False, default='')
    date_of_change = models.DateTimeField(null=True)


class BugReport(models.Model):
    type = models.CharField(max_length=15, null=True)
    report = models.TextField(max_length=500, null=True) # text?
    user = models.CharField(max_length=15, null=True)
    ipaddress = models.CharField(max_length=39, null=True)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    phone_num = models.CharField(max_length=50, null=True)
    phone_net = models.CharField(max_length=50, null=True)
    tstamp = models.BigIntegerField(null=True)
    groups = models.CharField(max_length=50, null=False, default='Help Desk'),
    office = models.CharField(max_length=50, null=False, default='OIT')
    time_code = models.CharField(max_length=10, null=False, default='')
    hr_code = models.CharField(max_length=10, null=False, default='')
    empl_rec = models.CharField(max_length=3, null=False, default='')
    empl_id = models.CharField(max_length=8, null=False, default='')
    admin = models.BooleanField(default=False)
    reports = models.BooleanField(default=False)
    nonsched_emp = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    hour_limit = models.IntegerField(null=True, default=20)
    aup = models.BigIntegerField(null=True)
    aup_date = models.BigIntegerField(null=True)
    cc_skill = models.IntegerField(default=0)
    cc_sen = models.IntegerField(default=0)
    hc_skill = models.IntegerField(default=0)
    hc_sen = models.IntegerField(default=0)
    rc_skill = models.IntegerField(default=0)
    rc_sen = models.IntegerField(default=0)
    lc_skill = models.IntegerField(default=0)
    lc_sen = models.IntegerField(default=0)


class Group(models.Model):
    name = models.CharField(max_length=50, null=False, default='')
    office_id = models.IntegerField(null=False, default=0) # Foreign Key?
    dept_id = models.CharField(max_length=10, null=True) # Foreign Key?


class Holiday(models.Model):
    date_info = models.DateField(null=True)
    day_num = models.IntegerField(default=0)
    info = models.TextField()


class Info(models.Model):
    full_name = models.CharField(max_length=50, null=False, default='')
    in_out = models.CharField(max_length=50, null=False, default='')
    timestamp = models.DateTimeField(null=True) # date?
    notes = models.CharField(max_length=250, null=True)
    ipaddress = models.CharField(max_length=39, null=False, default='')


class Metar(models.Model):
    metar = models.CharField(max_length=255, null=False, default='')
    timestamp = models.DateTimeField(auto_now=True)
    station = models.CharField(max_length=4, null=False, default='')


class Office(models.Model):
    name = models.CharField(max_length=50, null=False, default='')


class PostedShift(models.Model):
    date_info = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)
    poster = models.TextField()
    taker = models.TextField()
    reason = models.CharField(max_length=20, null=True)
    message = models.TextField(max_length=300, null=True)
    posted_on = models.DateField(null=True)
    manager_posting = models.CharField(max_length=10, null=True)
    excused_status = models.CharField(max_length=20, null=True)
    shift_type = models.CharField(max_length=4, null=True)
    shift_id = models.IntegerField(null=True)
    taken_id = models.IntegerField(null=True)
    is_partial = models.NullBooleanField()


class Punchlist(models.Model):
    punchitems = models.CharField(max_length=50, null=False, default='')
    color = models.CharField(max_length=7, null=False, default='')
    in_or_out = models.NullBooleanField() # better name?


class SchedPrefs(models.Model):
    net_id = models.CharField(max_length=20, null=True)
    default_view = models.IntegerField(null=True)


class SchoolSemesters(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    name = models.CharField(max_length=30, null=False, default='')


class Semester(models.Model):
    name = models.CharField(max_length=255, null=False, default='')
    last_updated = models.BigIntegerField(null=True)
    exclude_viewing = models.IntegerField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    semester = models.CharField(max_length=10, null=False, default='')


class Shift(models.Model):
    semester = models.ForeignKey('Semester', null=True)
    employee = models.ForeignKey('Employee', null=True)
    day_num = models.IntegerField(null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)
    lc_shift = models.NullBooleanField()
    needs_lc_slider = models.BooleanField(default=False)
    shift_type = models.CharField(max_length=4, null=True)
    day_num_end = models.IntegerField(null=True)
    is_partial = models.NullBooleanField()


class TakenWeek(models.Model):
    start_sunday = models.DateField(null=False)
    end_saturday = models.DateField(null=False)
    schedule_id = models.IntegerField(null=False)


class UserNotif(models.Model):
    employee = models.ForeignKey('Employee', null=False)
    timestamp = models.DateTimeField(null=False)
    message = models.TextField(max_length=250, null=True)
    type = models.CharField(max_length=15, null=False, default='')
    urgency = models.CharField(max_length=15, null=False, default='')
    color = models.CharField(max_length=8, null=False, default='')


class Wishlist(models.Model):
    employee = models.ForeignKey('Employee', null=False)
    from_time = models.TimeField(null=False)
    to_time = models.TimeField(null=False)
    want = models.BooleanField(default=False)
    cant = models.BooleanField(default=False)
    day = models.DateField(null=False)
    semester = models.ForeignKey('Semester', null=False)

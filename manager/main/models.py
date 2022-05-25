# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse



class TblSettingWeb(models.Model):
    ads_key_banner = models.TextField()
    ads_key_interstial = models.TextField()
    ad_display_count = models.IntegerField()
    ads_key_openads = models.TextField()
    arr_vid_trend = models.TextField(db_column='arr_Vid_trend')  # Field name made lowercase.
    arr_tv_trend = models.TextField(db_column='arr_TV_trend')  # Field name made lowercase.
    arr_radi_trend = models.TextField(db_column='arr_Radi_trend')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'tbl_setting_web'
        
    def __str__(self):
        return self.ads_key_banner + ' ' + self.ads_key_interstial

class TblCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100, db_collation='utf8_unicode_ci')
    cat_image = models.TextField(db_collation='utf8_unicode_ci')
    cat_type = models.IntegerField()
    cat_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_category'

    def __str__(self):
        return self.cat_name


class TblComment(models.Model):
    cmt_id = models.AutoField(primary_key=True)
    vid = models.ForeignKey('TblVideo', models.DO_NOTHING)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    cmt_time = models.DateTimeField()
    cmt_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'tbl_comment'

    def __str__(self):
        return self.cmt_text[0:30]


class TblFav(models.Model):
    vid = models.OneToOneField('TblVideo', models.DO_NOTHING, primary_key=True)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    is_fav = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_fav'
        unique_together = (('vid', 'uid'),)

    def __str__(self):
        return self.vid


class TblRating(models.Model):
    vid = models.OneToOneField('TblVideo', models.DO_NOTHING, primary_key=True)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    rate_score = models.IntegerField()
    rate_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_rating'
        unique_together = (('vid', 'uid'),)

    def __str__(self):
        return self.vid


class TblReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    vid = models.ForeignKey('TblVideo', models.DO_NOTHING, db_column='vid_id')
    report_content = models.TextField()
    report_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_report'
    
    def __str__(self):
        return self.report_content[0:30]

    def get_absolute_url_report(self):
        return reverse("report:detail_report", kwargs={"report_id": self.report_id})

    def get_absolute_url_report_delete(self):
        return reverse("report:delete_report", kwargs={"report_id": self.report_id})

    def get_absolute_url_report_main(self):
        return reverse("report:report_main", kwargs={"video_id": self.vid.vid_id})


class TblUsers(models.Model):
    uid = models.CharField(primary_key=True, max_length=100, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'tbl_users'

    def __str__(self):
        return self.uid


class TblVideo(models.Model):
    vid_id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(TblCategory, models.DO_NOTHING)
    vid_title = models.CharField(max_length=500, db_collation='utf8_unicode_ci')
    vid_url = models.TextField(db_collation='utf8_unicode_ci')
    vid_thumbnail = models.TextField(db_collation='utf8_unicode_ci')
    vid_description = models.TextField(db_collation='utf8_unicode_ci')
    vid_view = models.IntegerField()
    vid_duration = models.IntegerField()
    vid_time = models.DateTimeField()
    vid_avg_rate = models.FloatField()
    vid_status = models.IntegerField()
    vid_type = models.IntegerField()
    vid_is_premium = models.IntegerField()

    def __str__(self):
        return self.vid_title

    class Meta:
        managed = False
        db_table = 'tbl_video'

    

from django.db import models
import time
from django.contrib.auth.models import User
from django.conf import settings
from versatileimagefield.fields import VersatileImageField, PPOIField
from auditlog.registry import auditlog
from datetime import datetime

# Create your models here.

class BaseModel(models.Model):
   created_on = models.IntegerField(null=True, blank=True)
   modified_on = models.IntegerField(null=True, blank=True)
   is_active = models.BooleanField(default=True)
   deleted_at = models.IntegerField(blank=True, null=True)
   is_deleted = models.BooleanField(default=False)
   updated_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,related_name='%(class)s_updated_by', blank=True,on_delete=models.PROTECT)
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,related_name='%(class)s_createdby', blank=True,on_delete=models.PROTECT)
   class Meta:
       abstract = True


class AuthTokenMstr(BaseModel):
	auth_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.PROTECT,null=False)
	jwt_token = models.TextField(null=False)
	expire_ts = models.IntegerField(null=False)
	
	class Meta:
		managed = True
		db_table = 'Tl_Authtoken_tbl'

class UserLoginHistory(BaseModel):
	usrlog_id =models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.PROTECT,null=False)
	jwt_token = models.TextField(null=False)
	login_time =  models.IntegerField(null=False)
	logout_time = models.IntegerField(blank=True,null=True)
	expire_ts = models.IntegerField(null=False)
	
	class Meta:
		managed = True
		db_table = 'Tl_UserLoginHistory'


class TestMstr(BaseModel):
	test_id = models.AutoField(primary_key=True)	
	user_id = models.ForeignKey(User, on_delete=models.PROTECT,null=False)
	test_name  =  models.CharField(max_length=255,unique=False,blank=True)
	test_desc = models.TextField(blank=True,null=True)
	test_desc1 = models.TextField(blank=True,null=True)
	testtype =  models.CharField(max_length=255,null=True,blank=True)
	banners = models.TextField(blank=True,null=True)
	target_var =  models.CharField(max_length=255,null=True,blank=True)
	store_grid =  models.TextField(blank=True,null=True)
	territory_name =  models.CharField(max_length=255,null=True,blank=True)
	store_segment =  models.CharField(max_length=255,null=True,blank=True)
	category_name =  models.CharField(max_length=255,null=True,blank=True)
	confidence_lev =  models.CharField(max_length=255,null=True,blank=True)
	margin_oferror = models.IntegerField(blank=True,null=True)
	no_of_teststore = models.IntegerField(blank=True,null=True)
	pre_start = models.TextField(blank=True,null=True)
	pre_end = models.TextField(blank=True,null=True)
	test_window =  models.CharField(max_length=255,null=True,blank=True)
	testwin_start = models.CharField(max_length=255,null=True,blank=True)
	testwin_end = models.CharField(max_length=255,null=True,blank=True)
	stage_id = models.IntegerField(blank=True,null=True)
	stepper_id = models.IntegerField(blank=True,null=True)

	class Meta:
		managed = True
		db_table = 'Tl_TestMstr'


class StoreMstr(BaseModel):
	store_id = models.AutoField(primary_key=True)	
	Freq_rating_2019 = models.CharField(max_length=255,unique=False,blank=True)
	Freq_rating_2020 = models.CharField(max_length=255,unique=False,blank=True)
	Banner = models.CharField(max_length=255,unique=False,blank=True) 
	Business_Model = models.CharField(max_length=255,unique=False,blank=True) 
	CSV_of_outlet = models.CharField(max_length=255,unique=False,blank=True)
	CSV_of_outlet_Segment = models.CharField(max_length=255,unique=False,blank=True) 
	Channel = models.CharField(max_length=255,unique=False,blank=True) 
	Chocolate_RSV = models.CharField(max_length=255,unique=False,blank=True) 
	City = models.CharField(max_length=255,unique=False,blank=True) 
	City_Rural = models.CharField(max_length=255,unique=False,blank=True) 
	Classification = models.CharField(max_length=255,unique=False,blank=True)
	Classification_RTM = models.CharField(max_length=255,unique=False,blank=True) 
	Department = models.CharField(max_length=255,unique=False,blank=True) 
	Fulltime_total_duration = models.CharField(max_length=255,unique=False,blank=True)
	Fulltime_visits = models.CharField(max_length=255,unique=False,blank=True)
	House_Number = models.CharField(max_length=255,unique=False,blank=True)
	House_Number_Rural = models.CharField(max_length=255,unique=False,blank=True)
	Influence_Chocolate = models.CharField(max_length=255,unique=False,blank=True) 
	Influence_Overall = models.CharField(max_length=255,unique=False,blank=True) 
	Influence_Petcare = models.CharField(max_length=255,unique=False,blank=True) 
	Influence_Segment  = models.CharField(max_length=255,unique=False,blank=True) 
	Influence_on_activation = models.CharField(max_length=255,unique=False,blank=True)
	Influence_on_checkout = models.CharField(max_length=255,unique=False,blank=True)
	Influence_on_permanent_siting = models.CharField(max_length=255,unique=False,blank=True)
	Influence_on_shelf = models.CharField(max_length=255,unique=False,blank=True)
	Outlet_Banner_Code = models.CharField(max_length=255,unique=False,blank=True)
	Outlet_surface = models.CharField(max_length=255,unique=False,blank=True)
	Overall_Segment = models.CharField(max_length=255,unique=False,blank=True) 
	Partner_ID = models.CharField(max_length=255,unique=False,blank=True)
	Partner_Name = models.CharField(max_length=255,unique=False,blank=True) 
	Partner_Name_Rural = models.CharField(max_length=255,unique=False,blank=True) 
	Petcare_RSV = models.CharField(max_length=255,unique=False,blank=True) 
	Rural_vs_Urban = models.CharField(max_length=255,unique=False,blank=True) 
	Sales_Throughout_Year = models.CharField(max_length=255,unique=False,blank=True) 
	Segment = models.CharField(max_length=255,unique=False,blank=True) 
	Segment_Based = models.CharField(max_length=255,unique=False,blank=True) 
	Shelf_meters_Cat = models.CharField(max_length=255,unique=False,blank=True) 
	Shelf_meters_Choc = models.CharField(max_length=255,unique=False,blank=True) 
	Shelf_meters_Dog = models.CharField(max_length=255,unique=False,blank=True) 
	Status = models.CharField(max_length=255,unique=False,blank=True) 
	Street = models.CharField(max_length=255,unique=False,blank=True) 
	Street_Rural = models.CharField(max_length=255,unique=False,blank=True) 
	Sub_Channel = models.CharField(max_length=255,unique=False,blank=True) 
	Total_RSV = models.CharField(max_length=255,unique=False,blank=True)
	V4_invloed_op_activatie = models.CharField(max_length=255,unique=False,blank=True)
	V4_invloed_op_kassa = models.CharField(max_length=255,unique=False,blank=True) 
	V4_invloed_op_permanente_siting = models.CharField(max_length=255,unique=False,blank=True)
	V4_invloed_op_schap = models.CharField(max_length=255,unique=False,blank=True)
	ZIP_code = models.CharField(max_length=255,unique=False,blank=True) 
	ZIP_code_Rural = models.CharField(max_length=255,unique=False,blank=True)
	ZIP_code_4_digitis_Rural = models.CharField(max_length=255,unique=False,blank=True)
	thirdparty_total_duration = models.CharField(max_length=255,unique=False,blank=True)
	thirdparty_visits = models.CharField(max_length=255,unique=False,blank=True)
	Territory = models.CharField(max_length=255,unique=False,blank=True)
	Chocolate_Annual_RSV_2018 = models.CharField(max_length=255,unique=False,blank=True)
	Chocolate_Annual_Volume_2018 = models.CharField(max_length=255,unique=False,blank=True)
	Petcare_Annual_RSV_2018 = models.CharField(max_length=255,unique=False,blank=True)
	Petcare_Annual_Volume_2018 = models.CharField(max_length=255,unique=False,blank=True)
	Annual_RSV_2018 = models.CharField(max_length=255,unique=False,blank=True)
	Annual_Volume_2018 = models.CharField(max_length=255,unique=False,blank=True)
	Chocolate_Annual_RSV_2019 = models.CharField(max_length=255,unique=False,blank=True)
	Chocolate_Annual_Volume_2019 = models.CharField(max_length=255,unique=False,blank=True)
	Petcare_Annual_RSV_2019 = models.CharField(max_length=255,unique=False,blank=True)
	Petcare_Annual_Volume_2019 = models.CharField(max_length=255,unique=False,blank=True)
	Annual_RSV_2019 = models.CharField(max_length=255,unique=False,blank=True)
	Annual_Volume_2019 = models.CharField(max_length=255,unique=False,blank=True)

	class Meta:
		managed = True
		db_table = 'Tl_StoreMstr'

class TestStoreMap(BaseModel):
	storemap_id = models.AutoField(primary_key=True)	
	test_id   = models.ForeignKey(TestMstr, on_delete=models.PROTECT,null=False)
	store_id = models.ForeignKey(StoreMstr, on_delete=models.PROTECT,null=False)
	
	class Meta:
		managed = True
		db_table = 'Tl_Teststore_map'


class ControlStoreMstr(BaseModel):
	constore_id = models.AutoField(primary_key=True)	
	test_id = models.ForeignKey(TestMstr, on_delete=models.PROTECT,null=False)
	store_id = models.ForeignKey(StoreMstr, on_delete=models.PROTECT,null=False)
	test_option = models.BooleanField(default=False)
	constore_matchno = models.IntegerField(blank=True,null=True)
	constore_exclude =  models.CharField(max_length=255,null=True,blank=True)
	
	class Meta:
		managed = True
		db_table = 'Tl_Controlstore_Mstr'

class HierachyMstr(BaseModel):
	hier_id = models.AutoField(primary_key=True)	
	level = models.IntegerField(blank=True,null=True)
	value =  models.CharField(max_length=255,null=True,blank=True)
	
	class Meta:
		managed = True
		db_table = 'Tl_HierachyMstr'

class HierachyMapTbl(BaseModel):
	himap_id = models.AutoField(primary_key=True)	
	hier_id = models.ForeignKey(HierachyMstr, on_delete=models.PROTECT,null=False)
	test_id = models.ForeignKey(TestMstr, on_delete=models.PROTECT,null=False)
	
	class Meta:
		managed = True
		db_table = 'Tl_Hierachymap_tbl'


class MeasurementTbl(BaseModel):
	
	measure_id = models.AutoField(primary_key=True)	
	test_id = models.ForeignKey(TestMstr, on_delete=models.PROTECT,null=False)
	mesmetric_name =  models.CharField(max_length=255,null=True,blank=True)
	preperiod_start =  models.CharField(max_length=255,null=True,blank=True)
	preperiod_end =  models.CharField(max_length=255,null=True,blank=True)
	postperiod_start =  models.CharField(max_length=255,null=True,blank=True)
	postperiod_end =  models.CharField(max_length=255,null=True,blank=True)
	
	class Meta:
		managed = True
		db_table = 'Tl_Measurement_Tbl'

class RecordMstr(BaseModel):
	
	record_id = models.AutoField(primary_key=True)	
	test_id = models.ForeignKey(TestMstr, on_delete=models.PROTECT,null=False)
	stage_id = models.IntegerField(blank=True,null=False)
	stepper_id = models.IntegerField(blank=True,null=False)
	record_value = models.TextField(null=False)
	
	class Meta:
		managed = True
		db_table = 'Tl_RecordMstr'

import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.core.urlresolvers import reverse
# Create your models here.
class Profile(models.Model):
	"""
	扩展用户模型
	"""
	user = models.OneToOneField(
		User,
		primary_key=True,
	)

	nickname = models.CharField(
		'昵称',
		max_length=40,
		blank=True,
	)

	wei = models.CharField(
		'微信',
		max_length=40,
		blank=True,
	)

	birthday = models.DateField(
		'生日',
		blank=True,
		null=True,
	)

	location = models.CharField(
		'住址',
		max_length=40,
		blank=True,
	)

	Freshman = '大一'
	Sophomore = '大二'
	Junior = '大三'
	Senior = '大四'
	other = '其他'

	GRADE_CATEGORY_CHOICES = (
		(Freshman, '大一'),
		(Sophomore, '大二'),
		(Junior, '大三'),
		(Senior, '大四'),
		(other, '其他'),
	)
	grade = models.CharField(
		'年级',
		max_length=40,
		blank=True,
		choices=GRADE_CATEGORY_CHOICES,
		default=Senior)

	college = models.CharField(
		'学院',
		max_length=40,
		blank=True,
	)

	bio = models.TextField(
		'简介',
		blank=True,
	)
	def age(self):
		"""
		计算用户的年龄
		"""
		if not self.birthday:
			return "21"
		n, b = now().date(), self.birthday
		return n.year - b.year - (0 if n.month > b.month or n.month == b.month and n.day >= b.day else 1)        

	@models.permalink
	def get_absolute_url(self):
		kwargs, slug = {'id': self.user.id}, slugify(self)
		if slug:
			kwargs['slug'] = slug
		return ('trade:profile', (), kwargs)

	def __str__(self):
		return self.user.get_full_name() or self.user.get_username()

	class Meta:
		ordering = ('-user__last_login',)
		verbose_name = '用户'
		verbose_name_plural = '用户列表'

@receiver(models.signals.post_save, sender=User)
def create_profile(instance, created, **kwargs):
	"""
	当新用户被创建同时为其创建扩展
	"""
	if created:
		Profile.objects.create(user=instance)

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Category(models.Model):
	"""
	分类模型
	"""
	name = models.CharField('类别名称',max_length=50)

	class Meta:
		verbose_name = '类别'
		verbose_name_plural = '分类列表'

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField('标签名', max_length=40)
	description = models.CharField('描述', max_length=1000)

	class Meta:
		verbose_name = '标签'
		verbose_name_plural = '标签列表'

	def __str__(self):
		return self.name

class Goods(models.Model):
	"""
	物品模型
	"""
	RECOMMENDED = 'R'
	APPROVED = 'A'
	VIP = 'V'
	STATUS = (
		(RECOMMENDED, 'Recommended'),
		(APPROVED, 'Approved'),
		(VIP, 'V'),
	)
	user = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag)
	goods_title = models.CharField('物品名称', max_length=128)
	goods_price = models.DecimalField('价格', max_digits=9, decimal_places=2)
	status = models.CharField('状态', max_length=1, choices=STATUS, default=RECOMMENDED)
	kw = models.CharField('关键词', max_length=225)
	description = models.TextField('描述')
	view_count = models.PositiveIntegerField('浏览次数', default=0)
	image = models.ImageField('上传图片', upload_to=upload_location,
								width_field="width_field",
								height_field="height_field")
	height_field = models.IntegerField('高度', default=334)
	width_field = models.IntegerField('宽度', default=254)
	updated = models.DateTimeField('更新时间', null=True, blank=True)
	timestamp = models.DateTimeField('发布时间', auto_now_add=True)

	def update_view_count(self):
		self.view_count += 1
		self.save()

	class Meta:
		ordering = ['-timestamp']
		verbose_name = '物品'
		verbose_name_plural = '物品列表'

	def __str__(self):
		return self.goods_title	


class Seek(models.Model):
	lost_found = '招领'
	demand = '求购'
	STATUS = (
		(lost_found, '招领'),
		(demand, '求购'),
	)
	status = models.CharField('状态', max_length=40, choices=STATUS, default=demand)
	name = models.CharField('名称', max_length=225)
	kw = models.CharField('关键词', max_length=225)
	description = models.TextField('描述')
	timestamp = models.DateTimeField('发布时间', auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']
		verbose_name = '需求'
		verbose_name_plural = '需求列表'

	def __str__(self):
		return self.name	

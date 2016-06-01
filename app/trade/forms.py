from django import forms
from .models import Profile, Goods, Seek
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.ModelForm):
	"""
	用户资料编辑表单
	"""
	class Meta:
		model = Profile
		fields = ("nickname", "wei", "birthday", "location", "grade", "college", "bio")
		labels = {
			'nickname':_('昵称'),
			'weichat':_('微信'),
			'birthday': _('生日'),
			'location':_('住址'),
			'grade':_('年级'),
			'college':_('所在学院'),
			'bio':_('个人简介'),
		}

class ContactForm(forms.Form):
	"""
	联系表单
	"""
	full_name = forms.CharField(required=False, label=("姓名"))
	email = forms.EmailField(label=("邮箱"))
	message = forms.CharField(label=("您的建议"))
	
class PostForm(forms.ModelForm):
	"""
	发布物品
	"""
	class Meta:
		model = Goods
		fields = ("goods_title", "goods_price", "category", "image", "description")
		labels = {
			'goods_title':_('物品名称'),
			'goods_price':_('价格'),
			'category': _('分类'),
			'image':_('实物图片'),
			'description':_('描述你的物品'),
		}

class SeekForm(forms.ModelForm):
	class Meta:
		model = Seek
		fields = ("status", "name", "description")
		labels = {
			'status':_('招领求购'),
			'name':_('物品名称'),
			'description': _('描述'),
		}		



		

		




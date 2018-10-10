#coding:utf-8

# Register your models here.

from myAdmin.service.site import site, ModelAdmin
from app01 import models
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.conf.urls import url
class BookConfig(ModelAdmin):
    '''
    可以人一定以函数来自定义表格的标题和内容，注意下面函数的格式，必须定义两个默认参数model_obj=None, isHeader=False，（查看函数和后端的处理逻辑）
    '''
    # def edit(self, model_obj=None, isHeader=False):
    #     if not self.model_config.list_display_links:
    #         if isHeader:
    #             return '编辑'
    #         return mark_safe('<a href="%s/change/">编辑</a>'%model_obj.pk)  # 注意href="%s/change/ 和 href="/%s/change/的区别,前者为当前目录，后者为根目录
    #     else:
    #         return None

    # def checkbox(self,model_obj=None, isHeader=False):
    #     if isHeader:
    #         return '选择'
    #     return mark_safe('<input type="checkbox" value="%s" name="selected_item"/>'%model_obj.pk)
    #list_display = (checkbox, 'id', 'title', 'price', 'author', 'publish', edit)  #自定义函数来增加显示的项目

    #自定义批处理函数
    def batch_init_price(self,queryset):
        queryset.update(price=35)
    batch_init_price.short_description = '批量初始化价格'

    # 通过下面三个函数，为book添加一条单独的url处理逻辑，实现点击id值，为title添加喜欢或不喜欢
    def list_id(self,model_obj=None, isHeader=False):
        if isHeader:
            return 'ID'
        return mark_safe('<a href="like_book/%s">%s</a>'%(model_obj.pk, model_obj.pk))
    def like_book(self,request,obj_id):
        model_obj = models.Book.objects.get(id = obj_id)
        if '(喜欢)' not in model_obj.title:
            new_title = '%s  (喜欢)'%model_obj.title
        else:
            new_title = model_obj.title.replace('(喜欢)','')
        models.Book.objects.filter(id=obj_id).update(title = new_title)
        return redirect(self.get_list_url())
    def extra_url(self):
        temp = [url(r'like_book/(\d+)',self.like_book)]
        return temp


    list_display = (list_id, 'title','price','author','publish')
    list_display_links = ('title')
    search_field = ('title','price',)  #此处不能定义多对多或一对多关系字段
    actions = (batch_init_price,)
    list_filter = ('author','publish')
    #list_filter = ('title', 'author', 'publish')

site.register(models.Book,BookConfig)
site.register(models.Author)
site.register(models.Publish)
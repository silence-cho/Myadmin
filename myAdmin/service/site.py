# coding:utf-8

from django.conf.urls import url
from django.urls import reverse
from django.db import models
from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.db.models import Q
from django.db.models.fields.related import ForeignKey,ManyToManyField
import copy
from django.forms.models import ModelChoiceField
from myAdmin.mypage import page

class Showlist(object):
    '''
        需要四个参数来初始化实例：
        model_config: ModelAdmin 的实例对象，决定了其相关配置项
        model_list: 发送给前端的表格中要展示的数据对象（Queryset）
        model：数据表对象
        request：视图函数中的request参数
    '''

    def __init__(self,model_config,model_list,model,request):
        self.model_config = model_config
        self.model_list = model_list
        self.model = model
        self.request = request

        # 设置分页
        current_page = int(request.GET.get('page',1))
        params = self.request.GET
        base_url = self.request.path
        all_count = self.model_list.count()
        #print 'all_count',all_count
        self.page = page.Pagination(current_page, all_count, base_url, params, per_page_num=4, pager_count=3,)
        self.page_data = self.model_list[self.page.start:self.page.end]

    # 前端actions的显示数据
    def get_action_desc(self):
        # actions
        list_actions = []
        if self.model_config.get_actions():
            for action in self.model_config.get_actions():
                list_actions.append({
                    "name": action.__name__,       #批处理函数的名字
                    "desc": action.short_description
                })
        return list_actions

    # 前端过滤器的显示数据
    def get_filter_dict(self):
        # list_filter
        filter_dict = {}
        for field in self.model_config.list_filter:
            params = copy.deepcopy(self.request.GET)
            # print params
            selection = self.request.GET.get(field, 0)

            field_obj = self.model._meta.get_field(field)

            if isinstance(field_obj, ForeignKey) or isinstance(field_obj, ManyToManyField):     #对于多对多或外键字段的处理
                data_list = field_obj.rel.to.objects.all()    #field_obj.rel.to 能拿到多对多或外键字段对应的另一张model表对象
            else:
                data_list = self.model.objects.all().values('pk', field)
            temp = []
            if params.get(field):     #url参数的过滤条件中，如果有该字段的过滤条件，则点击全部时应该删除该字段的过滤条件，从而显示全部数据；不含有该字段的过滤条件，点击时不处理
                del params[field]
                temp.append("<a href='?%s' class='list-group-item is_selected'>全部</a>" % params.urlencode())
            else:
                temp.append("<a href='#' class='list-group-item'>全部</a>")
            for item in data_list:
                if isinstance(field_obj, ForeignKey) or isinstance(field_obj, ManyToManyField):    #多对多或外键字段，拿到的为对象
                    id = item.pk
                    text = str(item)
                    params[field] = id        #多对多或外键字段，以id做为过滤条件
                else:                               #普通字段拿到的为字典
                    id = item['pk']
                    text = item[field]
                    params[field] = text       #普通字段以字段名称做为过滤条件
                # print params
                tag_url = params.urlencode()
                if selection == str(id) or selection == text:   #判断此时url过滤字段中选中的条件，为其添加特殊style样式
                    temp.append("<a href='?%s' class='list-group-item is_selected'>%s</a>" % (tag_url, text))
                else:
                    temp.append("<a href='?%s' class='list-group-item'>%s</a>" % (tag_url, text))
            filter_dict[field_obj] = temp
        return filter_dict

    #前端表格表头的显示数据
    def get_head_list(self):
        head_list = []
        for field in self.model_config.get_list_display():
            if isinstance(field, str):  #判断函数和字符窜
                if field == '__str__':   #用户未配置时默认的list_play=('__str__',)
                    value = self.model._meta.model_name
                else:
                    field_obj = self.model._meta.get_field(field)  # 拿到字符窜对应的field对象
                    value = field_obj.verbose_name  # 通过拿到verbose_name 来显示中文
            else:
                value = field(self.model_config, isHeader=True)  # 获取标题，传入isHeader,  注意此处传入的self.model_config？？
            if value:
                head_list.append(value)
        return head_list

    #前端表格内容的显示数据
    def get_data_list(self):
        data_list = []
        for model_obj in self.page_data:   #分页截取的某一页的数据列表,不是全部的数据列表
            row_list = []
            for field in self.model_config.get_list_display():
                if isinstance(field, str):    #判断是字符窜或函数
                    try :
                        field_obj = self.model_config.model._meta.get_field(field)    #判断设置的显式列是否为多对多关系，处理相应的多个数据
                        if isinstance(field_obj, ManyToManyField):
                            temp_list = getattr(model_obj, field).all()
                            #print temp_list
                            ret = []
                            for temp in temp_list:
                                #print temp
                                ret.append(str(temp))    #转换为字符窜后进行拼接
                            value = ','.join(ret)
                            #print value
                        else:
                            value = getattr(model_obj, field)  # 通过反射拿到字符窜对应的值
                            if field in self.model_config.list_display_links:             # 判断该字段是否设置为超链接，放在此处表明了多对多关系设置超链接列中无效
                                value = mark_safe('<a href="%s/change/">%s</a>' % (model_obj.pk, value))
                    except Exception as e:
                        #print e
                        value = getattr(model_obj, field)
                else:
                    value = field(self.model_config, model_obj)  # 获取内容，传入model_obj,不用传入isHeader
                if value:
                    row_list.append(value)
            data_list.append(row_list)
        # print data_list
        return data_list

class ModelAdmin(object):
    list_display = ('__str__',)
    list_display_links = ()
    list_filter = ()
    search_field = ()
    actions = ()

    def __init__(self, model):
        self.model = model
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label
    @property
    def urls(self):
        return self.get_urls(), None, None

    def get_urls(self):

        patterns = [url(r'^$', self.list_view, name='%s_%s_list'%(self.model_name,self.app_label)),
                    url(r'^add/$', self.add_view,name='%s_%s_add'%(self.model_name,self.app_label)),
                    url(r'^(.+)/change/$', self.change_view,name='%s_%s_change'%(self.model_name,self.app_label)),
                    url(r'^(.+)/delete/$', self.delete_view,name='%s_%s_delete'%(self.model_name,self.app_label)),
                    ]
        patterns.extend(self.extra_url())
        return patterns

    #定义url接口，modelConfigure通过继承覆盖来配置额外的url
    def extra_url(self):
        return []

    #通过反射，拿到增删改查的url
    def get_list_url(self):
        _url = reverse('%s_%s_list'%(self.model_name,self.app_label))  #url反射，通过url路由中定义的名字，拿到对应路径，和路由分发相反
        return _url

    def get_add_url(self):
        _url = reverse('%s_%s_add' % (self.model_name, self.app_label))
        return _url

    def get_delete_url(self,model_obj):
        _url = reverse('%s_%s_delete' % (self.model_name, self.app_label),args=(model_obj.pk,))   #若对应的路径中有匹配参数，应传入参数
        return _url

    def get_change_url(self,model_obj):
        _url = reverse('%s_%s_change' % (self.model_name, self.app_label),args=(model_obj.pk,))   #若对应的路径中有匹配参数，应传入参数
        return _url

    # 定义默认要显式的内容， 编辑，删除操作和选择框，并设置list_display
    def edit(self,model_obj=None,isHeader=False):         #model_obj: 一个model表对象；isHeader是否是表格的表头字段
        if isHeader:
            return '操作'
        return mark_safe(
            '<a href="%s/change/">编辑</a>' % model_obj.pk)  # 注意href="%s/change/ 和 href="/%s/change/的区别,前者为当前目录，后者为根目录

    def checkbox(self,model_obj=None, isHeader=False):
        if isHeader:
            return '选择'
        return mark_safe('<input type="checkbox" value="%s" name="selected_item"/>'%model_obj.pk)

    def delete(self,model_obj=None, isHeader=False):
        if isHeader:
            return '操作'
        return mark_safe(
            '<a href="%s/delete/">删除</a>' % model_obj.pk)

    def get_list_display(self):
        new_list_display = []
        new_list_display.append(ModelAdmin.checkbox)      #加入选择框
        new_list_display.extend(self.list_display)        #加入用户配置的list_display
        if not self.list_display_links:
            new_list_display.append(ModelAdmin.edit)    #如果用户未配置超链接字段，加入编辑操作
        new_list_display.append(ModelAdmin.delete)      #加入删除操作
        return new_list_display

    #定义默认的批量删除函数，并设置action
    def batch_delete(self,queryset):
        queryset.delete()
    batch_delete.short_description = '批量删除'

    def get_actions(self):
        new_actions = []
        new_actions.append(ModelAdmin.batch_delete)     # 加入批量删除操作
        new_actions.extend(self.actions)                  # 扩展用户配置的actions，未配置时为空元祖
        return new_actions



    #处理搜索框提交的请求
    def get_search_condition(self,request):
        search_connector = Q()
        if request.method=='GET':
            search_content = request.GET.get('search_content','')
            search_connector.connector = 'or'
            if search_content and self.search_field:
                for field in self.search_field:
                    # field_obj = self.model._meta.get_field(field)
                    # if isinstance(field_obj,ManyToManyField) or isinstance(field_obj,ForeignKey):
                    #     search_connector.children.append((field + '__name__contains', search_content)) #对于多对多关系,如何实现动态？
                    # else:
                    search_connector.children.append((field + '__contains', search_content))
        return search_connector

    #处理过滤标签的<a>标签提交的请求
    def get_filter_condition(self,request):
        filter_connector = Q()
        if request.method == 'GET':
            for filter_field, value in request.GET.items():
                if filter_field in self.list_filter:        # 设置分页后url会出现page参数，不应做为过滤条件
                    filter_connector.children.append((filter_field, value))
        return filter_connector

    #查看：显示数据
    def list_view(self, request):

        model = self.model

        if request.method == 'POST':
            #print request.POST
            choice_item = request.POST.get('choice_item')
            selected_item = request.POST.getlist('selected_item')
            action_func = getattr(self,choice_item)
            queryset = model.objects.filter(id__in =selected_item)
            #print action_func,queryset
            action_func(queryset)

        # search_fields
        search_condition = self.get_search_condition(request)
        # list_filter
        filter_condition = self.get_filter_condition(request)

        model_list = model.objects.all().filter(search_condition).filter(filter_condition)
        #print 'model_list',model_list

        # print model_list[0].__str__()

        showlist= Showlist(self,model_list,model,request)    #单独抽象出一个类，用来配置前端数据的显示

        return render(request, 'list_view.html', locals())

    def get_modelform_class(self):
        class Model_form(ModelForm):
            class Meta:
                model = self.model
                fields = '__all__'
        return Model_form                  #返回类对象

    def change_modelform(self,modelform):

        for item in modelform:

            if isinstance(item.field, ModelChoiceField):   #ModelChoiceField,表示field字段对应的为外键或多对多关系，为其绑定一个属性，从而前端渲染“+”，点击能弹出该字段的添加页面
                pop_item_name = item.name
                item.is_pop=True #为实例动态绑定属性
                item_model_name = item.field.queryset.model._meta.model_name
                item_app_label = item.field.queryset.model._meta.app_label
                item.pop_url = '/myAdmin/{0}/{1}/add/?pop_item_name={2}'.format(item_app_label, item_model_name,pop_item_name)
        return modelform

    #增加数据
    def add_view(self, request):
        modelform_class = self.get_modelform_class()

        form = modelform_class()
        form = self.change_modelform(form)

        if request.method == 'POST':
            form = modelform_class(request.POST)
            field_obj = form.save()
            # url = request.path[:-4]
            # print url
            pop_item_name = request.GET.get('pop_item_name')
            if pop_item_name:
                result = {'pk':field_obj.pk,'text':str(field_obj),'pop_item_name':pop_item_name}
                return render(request, 'process_pop.html', {'result':result})
            return redirect(self.get_list_url())

        return render(request, 'add_view.html', locals())

    # 改变数据
    def change_view(self, request, number):

        modelform_class = self.get_modelform_class()

        model_obj = self.model.objects.filter(id=number).first()
        form = modelform_class(instance=model_obj)
        form = self.change_modelform(form)
        if request.method == 'POST':
            form = modelform_class(request.POST, instance=model_obj)
            form.save()
            return redirect(self.get_list_url())

        return render(request, 'change_view.html', locals())

    # 删除数据
    def delete_view(self, request, number):
        model_obj = self.model.objects.get(id=number)
        list_url = self.get_list_url()
        edit_url = self.get_change_url(model_obj)
        if request.method=='POST':
            model_obj.delete()
            return redirect(list_url)
        return render(request, 'delete_view.html', locals())



class AdminSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, admin_class=None):

        if not admin_class:
            admin_class = ModelAdmin
        admin_obj = admin_class(model)
        self._registry[model] = admin_obj

    @property
    def urls(self):
        return self.get_urls(), None, None

    def get_urls(self):
        patterns = []
        for model, admin_obj in self._registry.items():
            urls = url(r'^{0}/{1}/'.format(model._meta.app_label, model._meta.model_name), admin_obj.urls)
            patterns.append(urls)
        return patterns


site = AdminSite()

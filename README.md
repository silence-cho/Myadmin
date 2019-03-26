# myAdmin app
A backend management system plug-in based on Django (可插拔式的后台管理系统)

#使用方式：

1，配置myAdmin app
       拷贝myAdmin app（源码中整个myAdmin文件夹）到自己的Django项目中，并在项目settings.py文件中INSTALLED_APPS末尾添加myAdmin app，如下：
       
       INSTALLED_APPS = [
          'myAdmin.apps.MyadminConfig',
          ]
          
2，配置路由
      在项目urls.py文件中，配置app的路由，如下：
          
          from myAdmin.service.site import site
           urlpatterns = [
            url(r'^myAdmin/', site.urls),
            ]
            
3，在自己的app中使用
       若app名为app01,在app01目录下的admin.py中注册你的models数据，如下注册了Book,Author,Publish三个model：
       
           from myAdmin.service.site import site, ModelAdmin
           from app01 import models

           site.register(models.Book)
           site.register(models.Author)
           site.register(models.Publish)
      
  设置完后启动自己的项目，浏览器访问http://127.0.0.1:8080/myAdmin/app01/Book , 就能访问后台管理系统，对Book中数据进行增删改查。（Author, Publish操作也类似）
    
4，高级属性设置
     在注册models数据的时候，还可以对后端数据显示进行设置和自定义，如下面的设置中注册Book时，添加了一个BookConfig类：
           
           from myAdmin.service.site import site, ModelAdmin
            from app01 import models
            class BookConfig(ModelAdmin):
                list_display = ( 'title','price','author','publish')  #设置后台显示表中的某几列，此处会显示Book表中的'title','price','author','publish'四列
                list_display_links = ('title')   # 为某列数据添加编辑连接，此处点击Book表中的'title'列能进入数据编辑页面
                search_field = ('title','price',)  #此处不能定义多对多或一对多关系字段，设置搜索框的搜索字段匹配项，此处搜索时会将搜索字段和Book表中的'title','price'两列数据匹配
                actions = (batch_init_price,)  #添加自定义的批处理函数，此处添加了一个价格批量初始化函数
                list_filter = ('author','publish')  #添加数据分类字段，此处会根据Book表中的'author','publish'对数据进行分类
                
                #自定义批处理函数
                def batch_init_price(self,queryset):
                    queryset.update(price=35)
                batch_init_price.short_description = '批量初始化价格'

            site.register(models.Book,BookConfig)
            site.register(models.Author)
            site.register(models.Publish)

     
      
      
    


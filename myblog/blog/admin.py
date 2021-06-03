from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from myblog.custom_site import custom_site


# class PostInline(admin.TabularInline):  # StackedInline式样不同
#     fields = ('title', 'desc')
#     extra = 1
#     model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    # inlines = [PostInline, ]  # 在分类界面增加添加文章的操作

    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 自动保存当前登录者为作者
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)  # super里面的参数可省略


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status')

    def post_count(self, obj):
        return obj.post_set.count()

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_display = ('title', 'category', 'status', 'created_time', 'owner', 'operator')
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top =True
    actions_on_bottom = True

    save_on_top = True

    exclude = ('owner',)  # 指定不展示的字段

    # 编辑页面展示字段及顺序
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # 比fields高级一些的设置
    fieldsets = (
        ('基础配置', {
            # 'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            )
        }),
        ('内容', {
            'fields': (
                'desc', 'content'
            )
        }),
        ('额外信息', {
            # 'classes': ('collapse',),  # 折叠
            'fields': ('tag',)
        })
    )

    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    # 自定义字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    # 自定义静态资源引入
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)



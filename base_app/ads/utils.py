class DataMixin:
    title_page = None
    extra_context = {}

    menu = [
        {'title':'Главная', 'url_name':'home_page'},
        {'title':'Добавить Объявление', 'url_name':'create_ad'},
        {'title':'Смотреть Объявления', 'url_name':'show_ads'},
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get parent context
        context['menu'] = self.menu  # Inject menu
        if self.title_page:
            context['title'] = self.title_page
        context.update(self.extra_context)  # Add extra_context
        return context
    
    def get_mixin_context(self, context:dict, **kwargs):
        context['menu'] = self.menu
        context.update(kwargs)
        return context
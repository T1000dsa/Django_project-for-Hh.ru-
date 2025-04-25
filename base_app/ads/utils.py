#menu = [{'title':'about site', 'url_name':'about'}, 
        #{'title':'sign in', 'url_name':'autorise'},
        #{'title':'sign up', 'url_name':'register'},
        #{'title':'add book', 'url_name':'add'},
        #{'title':'get book', 'url_name':'get_books'},
        #]

class DataMixin:
    title_page = None
    
    extra_context  = {}
    
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context:dict, **kwargs):
        #context['menu'] = menu
        context.update(kwargs)
        return context
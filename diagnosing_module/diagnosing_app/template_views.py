

# Create your views here.
from django.views.generic import TemplateView
from asgiref.sync import sync_to_async

class AsyncTemplateView(TemplateView):
    template_name = "hello.html"

    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    


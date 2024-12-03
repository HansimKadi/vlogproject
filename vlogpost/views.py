from django.shortcuts import render
from .models import VlogPost
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import VlogPost, Category
from .forms import VlogPostForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


# Create your views here.

class ParentListView(ListView):
    """Parent class for ListViews."""
    model = None  # specified in children
    template_name = None  # specified in children
    context_object_name = 'object'
    paginate_by = 10  # default pagination value

    def filtering(self):
        return self.get_queryset()

class ParentDetailView(DetailView):
    """Parent class for DetailViews."""
    model = None
    template_name = None
    context_object_name = 'object'

class ParentCreateView(CreateView):
    """Parent class for CreateViews."""
    model = None
    template_name = None
    form_class = None

class ParentUpdateView(UpdateView):
    """Parent class for UpdateViews."""
    model = None
    template_name = None
    form_class = None

class VlogPostListView(ParentListView):
    """Child class for listing VlogPosts with specific filtering."""
    model = VlogPost
    template_name = "vlogpost/vlogpost_list.html"
    context_object_name = "vlogs"
    paginate_by = 10

    def filtering(self):
        """
        Implement filtering for the child class.
        Filters based on query parameters like title, author, tags, or published_date.
        """
        queryset = super().filtering()

        # Dynamic filters from query parameters
        title = self.request.GET.get("title")
        author = self.request.GET.get("author")
        tags = self.request.GET.get("tags")
        published_date = self.request.GET.get("published_date")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if tags:
            # Split and filter tags if provided
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            queryset = queryset.filter(tags__icontains=",".join(tag_list))
        if published_date:
            queryset = queryset.filter(published_date=published_date)

        return queryset

class VlogPostDetailView(ParentDetailView):
    """Child class for viewing VlogPost details."""
    model = VlogPost
    template_name = "vlogpost/vlog_detail.html"
    context_object_name = "vlogpost"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vlogpost = context['vlogpost']

        def extract_youtube_id(video_url):
            """Extract YouTube video ID from various URL formats."""
            import re
            youtube_regex = (
                r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)|.*[?&]v=)|youtu\.be/)'
                r'([^"&?/ ]{11})'
            )
            match = re.match(youtube_regex, video_url)
            if match:
                return match.group(1)  # Extract the video ID
            return None

        # Extract video ID and create the embed URL
        video_id = extract_youtube_id(vlogpost.video_url)
        if video_id:
            context['embed_url'] = f"https://www.youtube.com/embed/{video_id}"
        else:
            context['embed_url'] = None  # Fallback for invalid URLs

        return context

class VlogPostCreateView(LoginRequiredMixin,ParentCreateView):
    """Child class for creating a VlogPost."""
    model = VlogPost
    form_class = VlogPostForm
    template_name = 'vlogpost/vlogpost_form.html'
    success_url = reverse_lazy('vlogpost_list')  # Corrected to match the expected URL pattern name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass all categories to the template
        context['view'] = self  # Pass the view itself to use the view attributes in the template
        return context
    

    def form_valid(self, form):
        form.instance.author = self.request.user #assigning logged in user
        # Set the category before saving if it's not provided in the form data
        category_id = self.request.POST.get('category')
        if not category_id:
            # Assign a default category if none is provided
            default_category = Category.objects.get(name='Default Category')
            form.instance.category = default_category
        else:
            # Handle if a valid category is provided
            try:
                category = Category.objects.get(id=category_id)
                form.instance.category = category
            except Category.DoesNotExist:
                form.add_error('category', 'Selected category does not exist.')
                return self.form_invalid(form)

        return super().form_valid(form)

class VlogPostUpdateView(ParentUpdateView):
    """Child class for updating a VlogPost."""
    model = VlogPost
    template_name = "vlogpost/vlogpost_form.html"
    form_class = VlogPostForm
    success_url = reverse_lazy('vlogpost_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass all categories to the template
        context['view'] = self  # Pass the view itself to use the view attributes in the template
        return context
    def dispatch(self, request, *args, **kwargs):
        # Restrict access to only the author
        obj = self.get_object()
        if obj.author != request.user:
            return HttpResponseForbidden("You are not allowed to edit this post.")
        return super().dispatch(request, *args, **kwargs)



class RegisterView(FormView):
    template_name = 'vlogpost/registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        form.save()  # Save the user to the database
        return super().form_valid(form)
    

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('vlogpost_list')  # Use the name of your URL pattern


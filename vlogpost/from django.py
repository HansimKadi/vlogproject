from django.db import models




class VlogPost_model(models.Model):
    title = models.CharField(max_length = 255, default = "Untitled")
    video_url = models.CharField(max_length = 500, default = "No url available")
    description = models.CharField(max_length = 500,default = "No description available")
    author = models.CharField(max_length = 50, default = "Anonymous")
    published_date = models.DateField() #YYYY-MM-DD
    tags = models.CharField(max_length = 200, blank= True,default= " " ) # Separated by comma
    
    def __str__(self):
        return self.title
    
    def show_published_date(self): # Give us the date the vlog was published
        return self.published_date.strftime('%d,%m,%Y')
    
    def show_tags(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def show_author(self):
        return self.author
    
    def show_description(self):
        return self.description
    
    def show_info(self):
        info = f""""
        Title: {self.title}
        Video URL: {self.video_url}
        Description: {self.description}
        Author: {self.author}
        Published on: {self.published_date.strftime('%d,%m,%Y')}
        Tags: {self.tags}
        """
        return info.strip()

    
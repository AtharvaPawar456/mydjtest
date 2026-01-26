from django.db import models
from django.contrib.auth.models import User

# User --------
class UserDetails(models.Model):
    myuid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    
    address = models.TextField(default="*")
    contactno = models.TextField(default="*")
    refid = models.TextField(default="*")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of this object."""
        return (
            f"{self.myuid} | {self.user.username} | {self.contactno} | {self.refid} | "
            f"Added:{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class UserFavProjects(models.Model):
    favid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_fav')
    
    prod = models.ForeignKey('ProductInfo', on_delete=models.CASCADE)
    metadata = models.TextField(default="*")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of this object."""
        return (
            f"{self.favid} | {self.user.username} | {self.prod.productname} | "
            f"Added:{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )




class Contactus(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.TextField()
    emailid = models.TextField()
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.cid} | title:{self.msg} | Added:{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"




class TeamMember(models.Model):
    devid           = models.AutoField(primary_key=True)
    name            = models.TextField(default="*")
    role            = models.TextField(default="*")
    experience      = models.TextField(default="*")
    linkedin_url    = models.URLField(max_length=200, blank=True, null=True)
    github_url      = models.URLField(max_length=200, blank=True, null=True)
    photo_base64    = models.TextField(default="*")
    metadata        = models.TextField(default="*")
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.devid} | {self.name} | {self.role}"


class InternDetails(models.Model):
    internid        = models.AutoField(primary_key=True)
    
    name            = models.TextField(default="*")
    role            = models.TextField(default="*")
    experience      = models.TextField(default="*")
    linkedin_url    = models.URLField(max_length=200, blank=True, null=True)
    github_url      = models.URLField(max_length=200, blank=True, null=True)
    photo_base64    = models.TextField(default="*")
    metadata        = models.TextField(default="*") # safe HTML
    
    applicationlink = models.TextField(default="*")
    certificatelink = models.TextField(default="*")
    
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.internid} | {self.name} | {self.role}"


# --------

class Homeimgs(models.Model):
    hiid            = models.AutoField(primary_key=True)
    
    imgtitle        = models.TextField(default="*")
    imglink         = models.TextField(default="*")
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hiid} | {self.imgtitle} | {self.imglink}"



class ProductInfo(models.Model):
    prodid = models.AutoField(primary_key=True)
    productname = models.TextField(default="*")
    productcat = models.TextField(default="*")
    mainimgbasetxt = models.TextField(default="*")
    prodtags = models.TextField(default="*")
    
    prodcost = models.TextField(default="*")
    
    highlighttitle = models.TextField(default="*")
    prodinfo = models.TextField(default="*")
    
    gallery = models.TextField(default="*") #; seprated image.links
    ytlinks = models.TextField(default="*")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.prodid} | {self.productname} | {self.productcat} | Added:{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    

class YTvideos(models.Model):
    ytid           = models.AutoField(primary_key=True)
    
    videotitle    = models.TextField(default="*")
    videolink        = models.TextField(default="*")
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ytid} | {self.videotitle} | {self.videolink}"


class EarnTask(models.Model):
    etid = models.AutoField(primary_key=True)

    etitle = models.TextField(default="*")
    eamount = models.TextField(default="*")
    edescribe = models.TextField(default="*")
    estatus = models.TextField(default="active")
    eimglink = models.TextField(default="*")
    eseatscap = models.TextField(default="*")
    emetadata = models.TextField(default="*")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """String representation: id, title, and timestamp"""
        return f"{self.etid} | {self.etitle} | Added: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class AccessoriesProd(models.Model):
    apid = models.AutoField(primary_key=True)

    aptitle     = models.TextField(default="*")
    apheader    = models.TextField(default="*")
    apdesc      = models.TextField(default="*")
    apprice     = models.TextField(default="*")
    apsale      = models.TextField(default="*")
    apimglink   = models.TextField(default="*")
    aptag       = models.TextField(default="*")

    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of this object."""
        return (
            f"{self.apid} | {self.aptitle} | {self.apprice} | "
            f"Added:{self.timestamp.strftime('%d-%m-%Y')}"
        )


class AicontentProd(models.Model):
    aiid = models.AutoField(primary_key=True)

    aititle     = models.TextField(default="*")
    aiheader    = models.TextField(default="*")
    aidesc      = models.TextField(default="*")
    aiprice     = models.TextField(default="*")
    aisale      = models.TextField(default="*")
    aiimglink   = models.TextField(default="*")
    aitag       = models.TextField(default="*")

    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (f"{self.aiid} | {self.aititle} | {self.aiprice} | Added:{self.timestamp.strftime('%d-%m-%Y')}")



















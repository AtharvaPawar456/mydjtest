from django.db import models


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

    is_stipend = models.BooleanField(
        default=False,
        help_text="Toggle ON for stipend (paid) internship; OFF for unstipend (unpaid).",
    )
    
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        pay = "stipend" if self.is_stipend else "unstipend"
        return f"{self.internid} | {self.name} | {self.role} | {pay}"


class InternOpportunity(models.Model):
    """Open internship roles for /internship/opportunities/ (seeded from intern-ops.txt)."""

    opid = models.PositiveIntegerField(
        primary_key=True,
        help_text="Stable catalog ID from intern-ops.txt.",
    )
    title = models.TextField(default="*")
    track = models.TextField(default="*")
    mode = models.TextField(default="*")
    duration = models.TextField(default="*")
    stipend = models.TextField(default="*")
    is_stipend = models.BooleanField(
        default=False,
        help_text="Toggle ON for stipend (paid); OFF for unstipend (unpaid).",
    )
    skills = models.TextField(default="*")
    description = models.TextField(default="*")
    is_visible = models.BooleanField(
        default=True,
        help_text="If unchecked, hidden from the public list. In intern-ops.txt: | = visible, - = hide.",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["opid"]
        verbose_name_plural = "intern opportunities"

    def __str__(self):
        vis = "visible" if self.is_visible else "hidden"
        pay = "stipend" if self.is_stipend else "unstipend"
        return f"{self.opid} | {self.title} | {self.track} | {pay} | {vis}"


# --------

class Homeimgs(models.Model):
    hiid            = models.AutoField(primary_key=True)

    imgtitle        = models.TextField(
        default="*",
        help_text='Public visibility: set a real title to show on hero/gallery. Empty or "*" hides the image.',
    )
    imglink         = models.TextField(
        default="*",
        help_text='Image URL. Empty or "*" is treated as missing and excluded from public pages.',
    )
    timestamp       = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_placeholder(value) -> bool:
        """True when value is blank or the '*' placeholder."""
        return (value or "").strip() in ("", "*")

    @property
    def is_visible(self) -> bool:
        """Visible on public pages when imgtitle is set (not empty / '*')."""
        return not self.is_placeholder(self.imgtitle)

    @classmethod
    def public_qs(cls):
        """
        Hero + gallery queryset: real title (visible) and real image link.
        Hide rule: imgtitle is "" or "*" → not shown.
        """
        return (
            cls.objects.exclude(imgtitle__in=["", "*"])
            .exclude(imglink__in=["", "*"])
            .order_by("-timestamp")
        )

    def __str__(self):
        vis = "visible" if self.is_visible else "hidden"
        return f"{self.hiid} | {self.imgtitle} | {vis}"



class ProductCategory(models.Model):
    """
    Catalog categories for projects (Software, Hardware, …).
    Kept in a separate table so free-text productcat values do not drift.
    """

    catid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True, help_text="Display name, e.g. Software")
    slug = models.SlugField(
        max_length=64,
        unique=True,
        help_text="URL key, e.g. software (used as ?productcat=software)",
    )
    legacy_slugs = models.TextField(
        blank=True,
        default="",
        help_text="Comma-separated old productcat values (e.g. softwareprojects,kidsscience).",
    )
    hashtags = models.TextField(
        blank=True,
        default="",
        help_text="Comma-separated sub-category hashtags shown as quick filters.",
    )
    description = models.TextField(blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "product categories"

    def __str__(self) -> str:
        return f"{self.catid} | {self.name} ({self.slug})"

    @property
    def legacy_slug_list(self) -> list[str]:
        return [s.strip().lower() for s in (self.legacy_slugs or "").split(",") if s.strip()]

    @property
    def hashtag_list(self) -> list[str]:
        return [t.strip() for t in (self.hashtags or "").split(",") if t.strip()]

    def matches_query(self, value: str) -> bool:
        """True if value is this category's slug or a legacy slug."""
        v = (value or "").strip().lower()
        if not v:
            return False
        if v == self.slug.lower():
            return True
        return v in self.legacy_slug_list


class ProductBase(models.Model):
    """
    Shared project fields. Concrete per-category tables inherit this abstract base
    so Software / Hardware / … stay in separate models instead of one mixed ProductInfo table.
    """

    prodid = models.AutoField(primary_key=True)
    productname = models.TextField(default="*")
    mainimgbasetxt = models.TextField(default="*")
    prodtags = models.TextField(default="*")
    prodcost = models.TextField(default="*")
    highlighttitle = models.TextField(default="*")
    prodinfo = models.TextField(default="*")
    gallery = models.TextField(default="*")  # ; separated image links
    ytlinks = models.TextField(default="*")
    # Component photos (BOM / parts): same format as gallery
    components = models.TextField(
        default="*",
        help_text=(
            "Semicolon-separated component image URLs. "
            "Optional label: Label|https://example.com/part.jpg"
        ),
    )
    # Project docs (ppt/pptx/pdf/doc/docx/…): semicolon-separated URLs.
    # Optional label per entry: "Project Report|https://…/file.pdf"
    documents = models.TextField(
        default="*",
        help_text=(
            "Semicolon-separated document URLs (ppt, pptx, pdf, doc, docx, xls, xlsx, …). "
            "Optional label: Label|https://example.com/file.pdf"
        ),
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    # Set on each concrete subclass
    category_slug = ""
    category_name = ""

    class Meta:
        abstract = True
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return (
            f"{self.prodid} | {self.productname} | {self.category_name} | "
            f"Added:{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    @property
    def productcat(self) -> str:
        """Canonical category slug (template/API compatibility)."""
        return self.category_slug

    @property
    def category_label(self) -> str:
        return self.category_name or self.category_slug


class Project_Software(ProductBase):
    category_slug = "software"
    category_name = "Software"

    class Meta(ProductBase.Meta):
        verbose_name = "Project Software"
        verbose_name_plural = "Project Software"


class Project_Hardware(ProductBase):
    category_slug = "hardware"
    category_name = "Hardware"

    class Meta(ProductBase.Meta):
        verbose_name = "Project Hardware"
        verbose_name_plural = "Project Hardware"


class Project_Mechanical(ProductBase):
    category_slug = "mechanical"
    category_name = "Mechanical"

    class Meta(ProductBase.Meta):
        verbose_name = "Project Mechanical"
        verbose_name_plural = "Project Mechanical"


class Project_Simulation(ProductBase):
    category_slug = "simulation"
    category_name = "Simulation"

    class Meta(ProductBase.Meta):
        verbose_name = "Project Simulation"
        verbose_name_plural = "Project Simulation"


class Project_Science(ProductBase):
    category_slug = "science"
    category_name = "Science"

    class Meta(ProductBase.Meta):
        verbose_name = "Project Science"
        verbose_name_plural = "Project Science"


class Project_Craft(ProductBase):
    category_slug = "craft"
    category_name = "Craft"

    class Meta(ProductBase.Meta):
        verbose_name = "Project Craft"
        verbose_name_plural = "Project Craft"


class ProductInfo(models.Model):
    """
    Legacy unified product table — kept only until data is split into the
    per-category models above, then removed in a follow-up migration.
    """

    prodid = models.AutoField(primary_key=True)
    productname = models.TextField(default="*")
    productcat = models.TextField(default="*")
    category = models.ForeignKey(
        ProductCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
        help_text="Legacy FK — prefer per-category product models.",
    )
    mainimgbasetxt = models.TextField(default="*")
    prodtags = models.TextField(default="*")
    prodcost = models.TextField(default="*")
    highlighttitle = models.TextField(default="*")
    prodinfo = models.TextField(default="*")
    gallery = models.TextField(default="*")
    ytlinks = models.TextField(default="*")
    components = models.TextField(
        default="*",
        help_text="Semicolon-separated component image URLs (optional Label|URL).",
    )
    documents = models.TextField(
        default="*",
        help_text=(
            "Semicolon-separated document URLs (ppt, pdf, doc, …). "
            "Optional label: Label|https://example.com/file.pdf"
        ),
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.prodid} | {self.productname} | {self.productcat}"


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





class Businesswebinfo(models.Model):
    bid         = models.AutoField(primary_key=True)
    bname       = models.TextField(default="*")
    bcat        = models.TextField(default="*")
    bmainimg    = models.TextField(default="*")
    btags       = models.TextField(default="*")#, seprated image.links
    
    bhighlight  = models.TextField(default="*")
    binfo       = models.TextField(default="*")
    bownerimgs  = models.TextField(default="*") #; seprated image.links
    
    bgallery    = models.TextField(default="*") #; seprated image.links
    bytlinks    = models.TextField(default="*") #; seprated image.links
    bweblinks   = models.TextField(default="*") #; seprated image.links

    is_visible  = models.BooleanField(
        default=True,
        help_text="If unchecked/hidden, shop is hidden from the public directory.",
    )
    
    btimestamp  = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        vis = "visible" if self.is_visible else "hidden"
        return f"{self.bid} | {self.bname} | {self.bcat} | {vis} | {self.btimestamp.strftime('%d-%m-%Y %H:%M:%S')}"
    














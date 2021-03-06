from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.core.models import Page, Orderable
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException

from roadrunner.fields import RoadRunnerField

class HomePage(Page):
    pass


class NewsPage(Page):
    date = models.DateField(_("Post date"))
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )

    subtitle = models.CharField(max_length=255, blank=True, null=True)
    summary = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
        index.SearchField("subtitle"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("summary"),
            ],
            heading="Optional extras",
            classname="collapsed",
        ),
    ]


class VideoPage(Page):
    youtube_embed = models.TextField(null=True, blank=True)
    youtube = models.CharField(max_length=1024)

    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("youtube"),
        StreamFieldPanel("body"),
    ]

    def clean(self, *args, **kwargs):
        try:
            embed = get_embed(self.youtube, max_width=1024, max_height=768)
            self.youtube_embed = embed.html
        except EmbedException:
            self.youtube_embed = ""


class GalleryPage(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        InlinePanel("galleryitems", label=_("Gallery items")),
        StreamFieldPanel("body"),
    ]


class GalleryItem(Orderable):
    page = ParentalKey(
        GalleryPage, on_delete=models.CASCADE, related_name="galleryitems"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = RichTextField(blank=True)

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]


class GalleryPageButton(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    label = blocks.CharBlock()

    class Meta:
        template = "blocks/gallerypagebutton.html"

class GalleryLinkButton(blocks.StructBlock):
    link = blocks.URLBlock()
    label = blocks.CharBlock()

    class Meta:
        template = "blocks/gallerylinkbutton.html"


class GalleryImageItem(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(required=False)
    buttons = blocks.StreamBlock([
        ("page", GalleryPageButton()),
        ("link", GalleryLinkButton())
    ], required=False)

    class Meta:
        template = "blocks/galleryimageitem.html"


class GalleryVideoItem(blocks.StructBlock):
    video = EmbedBlock(max_width=1024, max_height=768)

    class Meta:
        template = "blocks/galleryvideoitem.html"


class GalleryPageEndResult(Page):
    galleryitems = StreamField([
        ("image", GalleryImageItem()),
        ("video", GalleryVideoItem())
    ])
    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("galleryitems"),
        StreamFieldPanel("body"),
    ]


class GalleryBlock(blocks.StructBlock):
    galleryitems = blocks.StreamBlock([
        ("image", GalleryImageItem()),
        ("video", GalleryVideoItem())
    ])

    class Meta:
        template = "blocks/galleryblock.html"


class NewPageEndResult(Page):
    date = models.DateField(_("Post date"))
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("gallery", GalleryBlock()),
        ]
    )

    subtitle = models.CharField(max_length=255, blank=True, null=True)
    summary = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
        index.SearchField("subtitle"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("summary"),
            ],
            heading="Optional extras",
            classname="collapsed",
        ),
    ]


class RoadrunnerPage(Page):
    content = RoadRunnerField()

    content_panels = Page.content_panels + [StreamFieldPanel("content")]
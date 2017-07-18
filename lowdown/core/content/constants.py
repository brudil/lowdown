FORM_ARTICLE = 1
FORM_VIDEO = 2
FORM_INTERACTIVE = 3
FORM_GALLERY = 4

FORM_CHOICES = (
    (FORM_ARTICLE, 'Article'),
    (FORM_VIDEO, 'Video'),
    (FORM_INTERACTIVE, 'Interactive'),
    (FORM_GALLERY, 'Gallery')
)

TONE_CONTENT = 1
TONE_REVIEW = 2
TONE_VIEWPOINT = 3
TONE_STORYTELLING = 4
TONE_INTERACTIVE = 5
TONE_GUIDE = 6

TONE_CHOICES = (
    (TONE_CONTENT, 'Content'),
    (TONE_REVIEW, 'Review'),
    (TONE_VIEWPOINT, 'Viewpoint'),
    (TONE_STORYTELLING, 'Storytelling'),
    (TONE_INTERACTIVE, 'Interactive'),
    (TONE_GUIDE, 'Guide'),
)

STATUS_STUB = 1
STATUS_DRAFT = 5
STATUS_REVIEW = 7
STATUS_FINAL = 9

STATUS_CHOICES = (
    (1, 'Stub'),
    (5, 'Draft'),
    (7, 'Review'),
    (9, 'Final'),
)

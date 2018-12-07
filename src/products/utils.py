from django.utils.text import slugify
import random, string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    model = instance.__class__
    qs = model.objects.filter(slug=slug)
    if qs.exists():
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return slug_generator(instance, new_slug=new_slug)
    return slug

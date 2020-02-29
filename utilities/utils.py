from pytils.translit import slugify


def unique_slug_generator(model, title):
    slug = slugify(title)

    filter = model.objects.filter(slug=slug)
    if filter.exists():
        id = model.objects.latest("id").id + 1
        slug = f"{slug}-{id}"
    return slug


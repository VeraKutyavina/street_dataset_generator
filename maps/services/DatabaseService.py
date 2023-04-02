from maps.models import OsmTag


def create_osm_tag(key, value, description):
    obj, created = OsmTag.objects.get_or_create(key=key, value=value)
    if created:
        obj.description = description
        obj.save()

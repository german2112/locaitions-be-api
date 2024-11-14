from app.repositories import TagRepository
from app.exceptions.InternalServerError import InternalServerError


def autocomplete_search(search_argument):
    try:
        tags_found = TagRepository.find_distinct("label", {"label": {
            "$regex": search_argument,
            "$options": 'i'
        }})
        return tags_found
    except Exception as e:
        raise InternalServerError(str(e))

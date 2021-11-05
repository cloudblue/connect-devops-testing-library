from typing import List, Optional


def find_by_id(collection: List, element_id: str) -> Optional[dict]:
    """
    Searches for a parameter/item with the given ``id`` within the ``list``.

    :param collection: The list of parameters/items to search.
    :param element_id: The id of the parameter/item to find.
    :return: The parameter/list, or ``None`` if it was not found.
    """
    filtered = list(filter(lambda element: element['id'] == element_id, collection))
    return filtered[0] if filtered else None

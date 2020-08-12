import logging
from banal import ensure_list
from flask import Blueprint, request

from aleph.authz import ActionEnum
from aleph.index.entities import iter_entities, PROXY_INCLUDES
from aleph.views.util import get_db_collection
from aleph.views.util import require, stream_ijson

log = logging.getLogger(__name__)
blueprint = Blueprint("bulk_api", __name__)


@blueprint.route("/api/2/entities/_stream")
@blueprint.route("/api/2/collections/<int:collection_id>/_stream")
def entities(collection_id=None):
    """
    ---
    get:
      summary: Stream collection entities.
      description: >
        Stream a JSON form of each entity in the given collection, or
        throughout the entire database.
      parameters:
      - description: The collection ID.
        in: path
        name: collection_id
        required: true
        schema:
          minimum: 1
          type: integer
      responses:
        '200':
          description: OK
          content:
            application/x-ndjson:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Entity'
      tags:
      - Entity
    """
    require(request.authz.can_stream())
    log.debug("Stream entities [%r] begins... (coll: %s)", request.authz, collection_id)
    schemata = ensure_list(request.args.getlist("schema"))
    includes = ensure_list(request.args.getlist("include"))
    includes = includes or PROXY_INCLUDES
    if collection_id is not None:
        get_db_collection(collection_id, ActionEnum.READ)
    entities = iter_entities(
        authz=request.authz,
        collection_id=collection_id,
        schemata=schemata,
        includes=includes,
    )
    return stream_ijson(entities)

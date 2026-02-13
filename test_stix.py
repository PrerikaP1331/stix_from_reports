from app.stix.stix_builder import (
    create_indicator_for_ip,
    create_bundle
)

ip_obj, indicator = create_indicator_for_ip("8.8.8.8")

bundle = create_bundle([ip_obj, indicator])

print(bundle.serialize(pretty=True))

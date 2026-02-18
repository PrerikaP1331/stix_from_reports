# test_atlas_update.py
from app.knowledge.updater import AtlasDatasetUpdater

updater = AtlasDatasetUpdater("app/data/atlas.json")
updater.update()

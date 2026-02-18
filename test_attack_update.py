# test_attack_update.py
from app.knowledge.updater import AttackDatasetUpdater

updater = AttackDatasetUpdater("app/data/attack-enterprise.json")
updater.update()

# Tibia Character Verification

This branch hosts an independent Tibia character registration website. The archived application source is unpacked at build time using unpack.py.

The deployment uses a persistent disk for screenshot uploads and SQLite, secure admin sessions, and TibiaData v5 public character data.

The admin password is generated securely at deployment. Change it under Render > Environment before sharing the admin URL.

Image storage bucket for ygo-db

---

* The folder, 'packages' should be bunch of zip files, each named "timestamp.zip", that contains all the card images added during that updates.

* updates are made manually by running updateImages.py

* clients should compare their existing packages and only download the missing packages.

---
TODOS

* add support for cards with alt arts, like blue eyes, dark magicians, ash blossom, etc. This requires a new json obj that maps the original id to all the alt art image code, along with the alt art's set code. Might be *a lot* of work to do manually.
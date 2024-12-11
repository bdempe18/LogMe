from django.db import models


class LogManager(models.Manager):
    def dedup(self, *fields):
        if not fields:
            msg = "You must provide at least one field"
            raise ValueError(msg)

        duplicates = (
            self.values(*fields).annotate(count=models.Count("id")).filter(count__gt=1)
        )

        delete_count = 0

        for duplicate in duplicates:
            filter_kwargs = {field: duplicate[field] for field in fields}
            entries = self.filter(**filter_kwargs)

            n, _ = entries.exclude(pk=entries.first().pk).delete()
            delete_count += n

        return delete_count


class ReadManager(models.Manager):
    def unread(self):
        return self.filter(is_read=False)

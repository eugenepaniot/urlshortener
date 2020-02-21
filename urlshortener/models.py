"""
A model is the single, definitive source of information about your data.
It contains the essential fields and behaviors of the data you’re storing.
Generally, each model maps to a single database table.
"""
from django.core.validators import URLValidator
from django.db import models


class URL(models.Model):
    """
        URL model:

            * target - target address;
            * tiny - "shortener" address;
            * created - datatime when record's created. Default current;
            * usage_count - how many time this record was called
    """

    target = models.CharField(max_length=2048, primary_key=True,
                              validators=[URLValidator(schemes=['http', 'https'])])
    tiny = models.CharField(max_length=2048, unique=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        """
            Model metadata is “anything that’s not a field”, such as ordering options (ordering),
            database table name (db_table), or human-readable singular
            and plural names (verbose_name and verbose_name_plural).
        """
        get_latest_by = 'created'

    def __str__(self):
        return self.tiny

    def save(self, *args, **kwargs):
        self.validate_unique()
        self.full_clean()

        super(URL, self).save(*args, **kwargs)

from django.core.mail.backends.filebased import EmailBackend as FileBaseEmailBackend

import datetime
import os

class EmailBackend(FileBaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)

    def _get_filename(self):
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fname = "%s-%s.eml" % (timestamp, abs(id(self)))
            self._fname = os.path.join(self.file_path, fname)
        return self._fname
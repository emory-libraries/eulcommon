# file eulcommon/djangoextras/validators.py
#
#   Copyright 2012 Emory University Libraries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
'''
Custom form validators for use with Django forms & form fields.

----
'''

import magic
from django.core.exceptions import ValidationError

class FileTypeValidator(object):
    '''Validator for a :class:`django.forms.FileField` to check the
    mimetype of an uploaded file using :mod:`magic`.  Takes a list of
    mimetypes and optional message; raises a
    :class:`~django.core.exceptions.ValidationError` if the mimetype
    of the uploaded file is not in the list of allowed types.

    :param types: list of acceptable mimetypes (defaults to empty list)
    :param message: optional error validation error message

    Example use::

        pdf = forms.FileField(label="PDF",
            validators=[FileTypeValidator(types=["application/pdf"],
                        message="Upload a valid PDF document.")])

    '''
    allowed_types = []

    def __init__(self, types=None, message=None):
        self.allowed_types = types or []
        if message is not None:
            self.message = message
        else:
            self.message = 'Upload a file in an allowed format: %s' % \
                           ', '.join(self.allowed_types)

        self.mime = magic.Magic(mime=True)

    def __call__(self, data):
        """
        Validates that the input matches the specified mimetype.

        :param data: file data, expected to be an instance of
        :class:`django.core.files.uploadedfile.UploadedFile`;
            handles both
        :class:`~django.core.files.uploadedfile.TemporaryUploadedFile`
            and :class:`~django.core.files.uploadedfile.InMemoryUploadedFile`.
        """
        # FIXME: check that data is an instance of
        # django.core.files.uploadedfile.UploadedFile ?

        # temporary file uploaded to disk (i.e., handled TemporaryFileUploadHandler)
        if hasattr(data, 'temporary_file_path'):
            mimetype = self.mime.from_file(data.temporary_file_path())

        # in-memory file (i.e., handled by MemoryFileUploadHandler)
        else:
            if hasattr(data, 'read'):
                content = data.read()
            else:
                content = data['content']
            mimetype = self.mime.from_buffer(content)

        mtype, separator, options = mimetype.partition(';')
        if mtype not in self.allowed_types:
            raise ValidationError(self.message)

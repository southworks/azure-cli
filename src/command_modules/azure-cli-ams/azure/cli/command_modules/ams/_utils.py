# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from datetime import datetime, timedelta

import uuid
import re
import isodate


def _gen_guid():
    return uuid.uuid4()


def _is_guid(guid):
    try:
        uuid.UUID(guid)
        return True
    except ValueError:
        pass
    return False

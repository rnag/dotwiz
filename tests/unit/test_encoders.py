import json
from datetime import datetime

import pytest

from dotwiz import DotWizPlus
from dotwiz.encoders import DotWizPlusEncoder


def test_dotwiz_plus_encoder_default():
    """:meth:`DotWizPlusEncoder.default` when :class:`AttributeError` is raised."""
    dw = DotWizPlus(this={'is': {'a': [{'test': True}]}})
    assert dw.this.is_.a[0].test

    string = json.dumps(dw, cls=DotWizPlusEncoder)
    assert string == '{"this": {"is": {"a": [{"test": true}]}}}'

    with pytest.raises(TypeError) as e:
        _ = json.dumps({'dt': datetime.min}, cls=DotWizPlusEncoder)

    assert str(e.value) == 'Object of type datetime is not JSON serializable'

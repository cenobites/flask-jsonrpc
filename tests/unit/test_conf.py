# Copyright (c) 2023-2025, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# * Neither the name of the Cenobit Technologies nor the names of
#    its contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import pytest

from flask_jsonrpc.conf import Settings, LazySettings, empty, settings, global_settings, new_method_proxy


def test_empty_sentinel() -> None:
    assert empty is not None
    assert empty is not False
    assert empty != 0
    assert empty != ''
    assert empty != []
    assert empty != {}
    from flask_jsonrpc.conf import empty as empty2

    assert empty is empty2


def test_settings_initialization() -> None:
    s = Settings()

    assert hasattr(s, 'DEFAULT_JSONRPC_METHOD_VALIDATE')
    assert hasattr(s, 'DEFAULT_JSONRPC_METHOD_NOTIFICATION')
    assert s.DEFAULT_JSONRPC_METHOD_VALIDATE is True  # type: ignore
    assert s.DEFAULT_JSONRPC_METHOD_NOTIFICATION is True  # type: ignore


def test_settings_only_copies_uppercase() -> None:
    s = Settings()

    for setting in dir(global_settings):
        if setting.isupper() and not setting.startswith('_'):
            assert hasattr(s, setting)
            assert getattr(s, setting) == getattr(global_settings, setting)


def test_settings_can_be_modified() -> None:
    s = Settings()
    original_validate = s.DEFAULT_JSONRPC_METHOD_VALIDATE

    s.DEFAULT_JSONRPC_METHOD_VALIDATE = False
    assert s.DEFAULT_JSONRPC_METHOD_VALIDATE is False
    assert original_validate != s.DEFAULT_JSONRPC_METHOD_VALIDATE

    s.DEFAULT_JSONRPC_METHOD_VALIDATE = original_validate
    assert original_validate == s.DEFAULT_JSONRPC_METHOD_VALIDATE


def test_settings_can_add_custom_attributes() -> None:
    s = Settings()

    s.CUSTOM_SETTING = 'custom_value'
    assert s.CUSTOM_SETTING == 'custom_value'

    s.ANOTHER_SETTING = 42
    assert s.ANOTHER_SETTING == 42


def test_lazy_settings_initialization() -> None:
    """Test LazySettings initializes with empty sentinel."""
    ls = LazySettings()
    assert ls._wrapped is empty


def test_lazy_settings_wrapped_attribute_access() -> None:
    """Test that _wrapped attribute can be accessed directly."""
    ls = LazySettings()
    assert ls._wrapped is empty

    ls._setup()
    assert isinstance(ls._wrapped, Settings)


def test_lazy_settings_setup() -> None:
    """Test LazySettings _setup creates Settings instance."""
    ls = LazySettings()
    assert ls._wrapped is empty

    ls._setup()
    assert ls._wrapped is not empty
    assert isinstance(ls._wrapped, Settings)


def test_lazy_settings_auto_setup_on_getattr() -> None:
    """Test that accessing attributes triggers automatic setup."""
    ls = LazySettings()
    assert ls._wrapped is empty

    value = ls.DEFAULT_JSONRPC_METHOD_VALIDATE
    assert ls._wrapped is not empty
    assert isinstance(ls._wrapped, Settings)
    assert value is True


def test_lazy_settings_getattr_proxy() -> None:
    ls = LazySettings()

    assert ls.DEFAULT_JSONRPC_METHOD_VALIDATE is True
    assert ls.DEFAULT_JSONRPC_METHOD_NOTIFICATION is True


def test_lazy_settings_setattr_before_setup() -> None:
    ls = LazySettings()
    assert ls._wrapped is empty

    ls.CUSTOM_SETTING = 'test_value'

    # Should have triggered setup
    assert ls._wrapped is not empty
    assert isinstance(ls._wrapped, Settings)
    assert ls.CUSTOM_SETTING == 'test_value'


def test_lazy_settings_setattr_after_setup() -> None:
    ls = LazySettings()
    ls._setup()

    ls.CUSTOM_SETTING = 'test_value'
    assert ls.CUSTOM_SETTING == 'test_value'

    ls.DEFAULT_JSONRPC_METHOD_VALIDATE = False
    assert ls.DEFAULT_JSONRPC_METHOD_VALIDATE is False


def test_lazy_settings_setattr_wrapped() -> None:
    ls = LazySettings()
    custom_settings = Settings()
    custom_settings.CUSTOM = 'value'

    ls._wrapped = custom_settings
    assert ls._wrapped is custom_settings
    assert ls.CUSTOM == 'value'


def test_lazy_settings_delattr() -> None:
    ls = LazySettings()
    ls.CUSTOM_SETTING = 'test_value'
    assert ls.CUSTOM_SETTING == 'test_value'

    del ls.CUSTOM_SETTING

    with pytest.raises(AttributeError):
        _ = ls.CUSTOM_SETTING


def test_lazy_settings_delattr_triggers_setup() -> None:
    ls = LazySettings()
    with pytest.raises(AttributeError):
        del ls.NONEXISTENT_ATTRIBUTE


def test_lazy_settings_delattr_after_manual_setup() -> None:
    ls = LazySettings()
    _ = ls.DEFAULT_JSONRPC_METHOD_VALIDATE
    ls.CUSTOM_SETTING = 'test_value'
    assert ls.CUSTOM_SETTING == 'test_value'

    del ls.CUSTOM_SETTING

    with pytest.raises(AttributeError):
        _ = ls.CUSTOM_SETTING


def test_lazy_settings_delattr_wrapped_raises_error() -> None:
    ls = LazySettings()

    with pytest.raises(TypeError, match="can't delete _wrapped"):
        del ls._wrapped


def test_lazy_settings_getattribute_wrapped() -> None:
    ls = LazySettings()

    wrapped_value = ls.__getattribute__('_wrapped')
    assert wrapped_value is empty


def test_lazy_settings_getattribute_masked() -> None:
    ls = LazySettings()

    with pytest.raises(AttributeError):
        ls.__getattribute__('__getattr__')


def test_new_method_proxy() -> None:
    def test_getter(obj: object, arg: str) -> str:
        if arg == 'invalid':
            raise AttributeError
        return f'{obj}-{arg}'

    proxied = new_method_proxy(test_getter)
    assert hasattr(proxied, '_mask_wrapped')
    assert proxied._mask_wrapped is False


def test_new_method_proxy_with_lazy_object() -> None:
    ls = LazySettings()

    assert ls._wrapped is empty

    value = ls.DEFAULT_JSONRPC_METHOD_VALIDATE

    assert ls._wrapped is not empty
    assert isinstance(ls._wrapped, Settings)
    assert value is True


def test_new_method_proxy_calls_setup_once() -> None:
    ls = LazySettings()

    _ = ls.DEFAULT_JSONRPC_METHOD_VALIDATE
    wrapped_after_first = ls._wrapped

    _ = ls.DEFAULT_JSONRPC_METHOD_NOTIFICATION
    wrapped_after_second = ls._wrapped

    assert wrapped_after_first is wrapped_after_second


def test_new_method_proxy_fallback_settings() -> None:
    ls = LazySettings(fallback_settings={'FLASK_JSONRPC_TEST_FALLBACK_VAR': 'fallback_value'})
    ls._setup()

    value = ls.TEST_FALLBACK_VAR

    assert value == 'fallback_value'
    assert hasattr(ls._wrapped, 'TEST_FALLBACK_VAR')
    assert ls._wrapped.TEST_FALLBACK_VAR == 'fallback_value'


def test_global_settings_instance() -> None:
    assert isinstance(settings, LazySettings)

    assert settings.DEBUG is False
    assert settings.DEFAULT_JSONRPC_METHOD_VALIDATE is True
    assert settings.DEFAULT_JSONRPC_METHOD_NOTIFICATION is True


def test_settings_isolation() -> None:
    s1 = Settings()
    s2 = Settings()

    s1.CUSTOM = 'value1'
    s2.CUSTOM = 'value2'

    assert s1.CUSTOM == 'value1'
    assert s2.CUSTOM == 'value2'
    assert s1.CUSTOM != s2.CUSTOM


def test_lazy_settings_isolation() -> None:
    ls1 = LazySettings()
    ls2 = LazySettings()

    ls1.CUSTOM = 'value1'
    ls2.CUSTOM = 'value2'

    assert ls1.CUSTOM == 'value1'
    assert ls2.CUSTOM == 'value2'
    assert ls1.CUSTOM != ls2.CUSTOM


def test_lazy_object_protocol() -> None:
    ls = LazySettings()

    assert hasattr(ls, '_wrapped')
    assert hasattr(ls, '_setup')
    assert callable(ls._setup)

    assert ls._wrapped is empty


def test_settings_persistence() -> None:
    s = Settings()

    s.TEST_SETTING_1 = 100
    s.TEST_SETTING_2 = 'test'
    s.TEST_SETTING_3 = [1, 2, 3]

    assert s.TEST_SETTING_1 == 100
    assert s.TEST_SETTING_2 == 'test'
    assert s.TEST_SETTING_3 == [1, 2, 3]

    s.TEST_SETTING_1 = 200
    assert s.TEST_SETTING_1 == 200


def test_lazy_settings_persistence() -> None:
    ls = LazySettings()

    ls.TEST_SETTING_1 = 100
    ls.TEST_SETTING_2 = 'test'
    ls.TEST_SETTING_3 = [1, 2, 3]

    assert ls.TEST_SETTING_1 == 100
    assert ls.TEST_SETTING_2 == 'test'
    assert ls.TEST_SETTING_3 == [1, 2, 3]

    ls.TEST_SETTING_1 = 200
    assert ls.TEST_SETTING_1 == 200


def test_lazy_settings_multiple_setups() -> None:
    ls = LazySettings()

    ls._setup()
    first_wrapped = ls._wrapped

    ls._setup()
    second_wrapped = ls._wrapped

    assert first_wrapped is not second_wrapped
    assert isinstance(second_wrapped, Settings)


def test_settings_with_different_types() -> None:
    s = Settings()

    s.INT_SETTING = 42
    s.FLOAT_SETTING = 3.14
    s.STR_SETTING = 'hello'
    s.BOOL_SETTING = True
    s.LIST_SETTING = [1, 2, 3]
    s.DICT_SETTING = {'key': 'value'}
    s.NONE_SETTING = None

    assert s.INT_SETTING == 42
    assert s.FLOAT_SETTING == 3.14
    assert s.STR_SETTING == 'hello'
    assert s.BOOL_SETTING is True
    assert s.LIST_SETTING == [1, 2, 3]
    assert s.DICT_SETTING == {'key': 'value'}
    assert s.NONE_SETTING is None


def test_lazy_settings_with_different_types() -> None:
    ls = LazySettings()

    ls.INT_SETTING = 42
    ls.FLOAT_SETTING = 3.14
    ls.STR_SETTING = 'hello'
    ls.BOOL_SETTING = True
    ls.LIST_SETTING = [1, 2, 3]
    ls.DICT_SETTING = {'key': 'value'}
    ls.NONE_SETTING = None

    assert ls.INT_SETTING == 42
    assert ls.FLOAT_SETTING == 3.14
    assert ls.STR_SETTING == 'hello'
    assert ls.BOOL_SETTING is True
    assert ls.LIST_SETTING == [1, 2, 3]
    assert ls.DICT_SETTING == {'key': 'value'}
    assert ls.NONE_SETTING is None

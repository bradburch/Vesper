"""Module containing class `ClipCollectionViewSettingsPreset`."""


from vesper.util.yaml_preset import YamlPreset
import vesper.util.case_utils as case_utils


class ClipCollectionViewSettingsPreset(YamlPreset):
    
    """
    Preset that specifies clip collection view settings.
    
    The preset body is YAML that specifies a mapping from setting names
    to setting values.
    """
    
    extension_name = 'Clip Collection View Settings'
    
    
    @property
    def camel_case_data(self):
        return case_utils.snake_to_camel(self.data)
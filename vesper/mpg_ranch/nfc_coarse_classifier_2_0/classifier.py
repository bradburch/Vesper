"""
Module containing MPG Ranch NFC coarse classifier, version 2.0.

An NFC coarse classifier classifies an unclassified clip of the
classifier's clip type (either `'Tseep'` or `'Thrush'`) as a `'Call'`
if it appears to be a nocturnal flight call, and as a `'Noise'` otherwise.
The classifier does not alter the classification of a clip if the clip
is not of the classifier's clip type, or if it is not unclassified.
"""


import resampy
import yaml

from vesper.command.annotator import Annotator
from vesper.mpg_ranch.nfc_coarse_classifier_2_0.feature_computer import \
    FeatureComputer
from vesper.util.settings import Settings
import vesper.django.app.model_utils as model_utils
import vesper.mpg_ranch.nfc_coarse_classifier_2_0.classifier_utils as \
    classifier_utils


class _Classifier(Annotator):
    
    
    def __init__(self, clip_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clip_type = clip_type
        self._model = self._load_model()
        self._settings = self._load_settings()
        self._feature_computer = FeatureComputer(self._settings)
    
    
    def _load_model(self):
        
        # We put this here rather than at the top of this module since
        # Keras can be rather slow to import (we have seen load times of
        # about ten seconds), so we want to import it only when we know
        # we are about to use it.
        import keras
        
        path = classifier_utils.get_model_file_path(self.clip_type)
        return keras.models.load_model(path)
    
    
    def _load_settings(self):
        path = classifier_utils.get_settings_file_path(self.clip_type)
        text = path.read_text()
        d = yaml.load(text)
        return Settings.create_from_dict(d)
        
        
    def annotate(self, clip):
        
        annotated = False
        
        classification = self._get_annotation_value(clip)
        
        if classification is None:
            # clip is unclassified
            
            clip_type = model_utils.get_clip_type(clip)
        
            if clip_type == self.clip_type:
                # clip is of this classifier's type
                
                classification = self._classify(clip)
                
                if classification is not None:
                    self._annotate(clip, classification)
                    annotated = True
                    
        return annotated
    
    
    def _classify(self, clip):
        
        waveform = self._get_waveform(clip)
        
        if len(waveform) < self._feature_computer.min_waveform_length:
            # clip is too short to classify
            
            return 'Noise'
        
        else:
            # clip is not too short to classify
        
            # Add extra initial dimension to waveform array for feature
            # computer.
            waveforms = waveform.reshape((1,) + waveform.shape)
            
            features = self._feature_computer.compute_features(waveforms)
            
            value = self._model.predict(features, batch_size=1)[0]
            
            if value >= self._settings.classification_threshold:
                return 'Call'
            else:
                return 'Noise'
        
        
    def _get_waveform(self, clip):
        
        sound = clip.sound
        waveform = sound.samples
        sample_rate = sound.sample_rate
        
        classifier_sample_rate = self._settings.waveform_sample_rate
        
        if sample_rate != classifier_sample_rate:
            # waveform is not at classifier sample rate
            
            waveform = resampy.resample(
                waveform, sample_rate, classifier_sample_rate)
            
        return waveform


class ThrushClassifier(_Classifier):
    
    extension_name = 'MPG Ranch Thrush Coarse Classifier 2.0'
    
    def __init__(self, *args, **kwargs):
        super().__init__('Thrush', *args, **kwargs)


class TseepClassifier(_Classifier):
    
    extension_name = 'MPG Ranch Tseep Coarse Classifier 2.0'
    
    def __init__(self, *args, **kwargs):
        super().__init__('Tseep', *args, **kwargs)
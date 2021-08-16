"""Module containing class `UntagClipsCommand`."""


import logging
import random
import time

from django.db import transaction

from vesper.command.clip_set_command import ClipSetCommand
from vesper.django.app.models import Job, Tag, TagEdit, TagInfo
import vesper.command.command_utils as command_utils
import vesper.django.app.model_utils as model_utils
import vesper.util.archive_lock as archive_lock
import vesper.util.text_utils as text_utils
import vesper.util.time_utils as time_utils


_logger = logging.getLogger()


class UntagClipsCommand(ClipSetCommand):
    
    
    extension_name = 'untag_clips'
    
    
    def __init__(self, args):
        
        super().__init__(args, True)
        
        get = command_utils.get_required_arg
        self._retain_count = get('retain_count', args)
        
        
    def execute(self, job_info):
        self._job_info = job_info
        retain_indices = self._get_retain_clip_indices()
        self._untag_clips(retain_indices)
        return True
    
    
    def _get_retain_clip_indices(self):
        
        if self._retain_count == 0:
            indices = []
            
        else:
            
            _logger.info(
                'Getting indices of clips for which to retain tags...')
            
            clip_count = self._count_clips()
            
            if clip_count <= self._retain_count:
                # will retain all clips
                
                indices = list(range(clip_count))
                
            else:
                # will not retain all clips
                
                indices = random.sample(range(clip_count), self._retain_count)
            
        return frozenset(indices)
    
    
    def _count_clips(self):
        
        value_tuples = self._create_clip_query_values_iterator()
        count = 0
        
        for station, mic_output, date, detector in value_tuples:
            
            clips = model_utils.get_clips(
                station=station,
                mic_output=mic_output,
                date=date,
                detector=detector,
                annotation_name=self._annotation_name,
                annotation_value=self._annotation_value,
                tag_name=self._tag_name,
                order=False)
            
            count += clips.count()
            
        return count
            

    def _untag_clips(self, retain_indices):
        
        start_time = time.time()
        
        retaining_tags = len(retain_indices) == 0
        
        value_tuples = self._create_clip_query_values_iterator()
        
        index = 0
        total_retained_count = 0
        
        for station, mic_output, date, detector in value_tuples:
            
            # Get clips for this station, mic_output, date, and detector
            clips = model_utils.get_clips(
                station=station,
                mic_output=mic_output,
                date=date,
                detector=detector,
                annotation_name=self._annotation_name,
                annotation_value=self._annotation_value,
                tag_name=self._tag_name,
                order=False)
            
            
            # Figure out which clips to untag
            
            count = 0
            retained_count = 0
            clips_to_untag = []
            
            for clip in clips:
                
                if index not in retain_indices:
                    clips_to_untag.append(clip)
                else:
                    retained_count += 1
                    
                count += 1
                index += 1
                
                
            # Untag clips.
            try:
                self._untag_clip_batch(clips_to_untag)
            except Exception as e:
                batch_text = \
                    _get_batch_text(station, mic_output, date, detector)
                command_utils.log_and_reraise_fatal_exception(
                    e, f'Untagging of clips for {batch_text}')

            # Log clip counts.
            if retaining_tags:
                prefix = 'Untagged'
            else:
                untagged_count = count - retained_count
                prefix = (
                    f'Untagged {untagged_count} and left tagged '
                    f'{retained_count} of')
            count_text = text_utils.create_count_text(count, 'clip')
            batch_text = _get_batch_text(station, mic_output, date, detector)
            _logger.info(f'{prefix} {count_text} for {batch_text}.')

            total_retained_count += retained_count
                
        # Log total clip counts and untagging rate.
        if total_retained_count == 0:
            prefix = 'Untagged'
        else:
            untagged_count = index - total_retained_count
            prefix = (
                f'Untagged {untagged_count} and left tagged '
                f'{total_retained_count} of')
        count_text = text_utils.create_count_text(index, 'clip')
        elapsed_time = time.time() - start_time
        timing_text = command_utils.get_timing_text(
            elapsed_time, index, 'clips')
        _logger.info(f'{prefix} a total of {count_text}{timing_text}.')


    def _untag_clip_batch(self, clips):
        
        with archive_lock.atomic():
             
            with transaction.atomic():
            
                # Untag clips in chunks to limit the number of clip IDs
                # we pass to `Clip.objects.filter`.
                
                # Setting this too large can result in a
                # django.db.utils.OperationalError exception with the
                # message "too many SQL variables". We have seen this
                # happen with a maximum chunk size of 1000 on Windows,
                # though not on macOS. The web page
                # https://stackoverflow.com/questions/7106016/
                # too-many-sql-variables-error-in-django-witih-sqlite3
                # suggests that the maximum chunk size that will work
                # on Windows is somewhere between 900 and 1000, and
                # 900 seems to work.
                max_chunk_size = 900
                
                tag_info = TagInfo.objects.get(name=self._tag_name)
                action = TagEdit.ACTION_DELETE
                creation_time = time_utils.get_utc_now()
                creating_job = Job.objects.get(id=self._job_info.job_id)
                
                for i in range(0, len(clips), max_chunk_size):
                    
                    chunk = clips[i:i + max_chunk_size]
                    
                    # Delete tags from archive database.
                    ids = [clip.id for clip in chunk]
                    Tag.objects.filter(info=tag_info, clip_id__in=ids).delete()
                    
                    # Create tag edits.
                    TagEdit.objects.bulk_create([
                        TagEdit(
                            clip=clip,
                            info=tag_info,
                            action=action,
                            creation_time=creation_time,
                            creating_user=None,
                            creating_job=creating_job,
                            creating_processor=None)
                        for clip in chunk])
                    
                    
def _get_batch_text(station, mic_output, date, detector):
    return (
        f'station "{station.name}", mic output "{mic_output.name}", '
        f'date {date}, and detector "{detector.name}"')

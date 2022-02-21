from pathlib import Path
import csv
import logging
import tempfile

from vesper.command.command import CommandExecutionError, CommandSyntaxError
import vesper.util.os_utils as os_utils


# TODO: Add type checking to functions that get arguments.


def get_required_arg(name, args):
    try:
        return args[name]
    except KeyError:
        raise CommandSyntaxError(
            'Missing required command argument "{}".'.format(name))


def get_optional_arg(name, args, default=None):
    return args.get(name, default)


def get_timing_text(elapsed_time, item_count, items_name):
    
    # Round elapsed time to nearest tenth of a second since it
    # will be displayed at that resolution. This will keep the
    # reported item count, elapsed time, and rate consistent.
    elapsed_time = round(10 * elapsed_time) / 10
    
    time_text = ' in {:.1f} seconds'.format(elapsed_time)
    
    if elapsed_time > 0:
        
        rate = item_count / elapsed_time
        return '{}, an average of {:.1f} {} per second'.format(
            time_text, rate, items_name)
        
    else:
        # elapsed time is zero
        
        return time_text


def write_csv_file(file_path, rows, header=None):
    
    handle_error = handle_command_execution_error

    # Create output CSV file in temporary file directory.
    try:
        temp_file = tempfile.NamedTemporaryFile(
            'wt', newline='', prefix='vesper-', suffix='.csv',
            delete=False)
    except Exception as e:
        handle_error('Could not open output CSV file.', e)
    
    # Create CSV writer.
    try:
        writer = csv.writer(temp_file)
    except Exception as e:
        handle_error('Could not create CSV file writer.', e)

    # Write header.
    if header is not None:
        try:
            writer.writerow(header)
        except Exception as e:
            handle_error('Could not write CSV file header.', e)

    # Write rows.
    try:
        writer.writerows(rows)
    except Exception as e:
        handle_error('Could not write CSV file rows.', e)

    temp_file_path = Path(temp_file.name)
    
    # Close output file.
    try:
        temp_file.close()
    except Exception as e:
        handle_error('Could not close output CSV file.', e)
    
    # Copy temporary output file to final path.
    try:
        os_utils.copy_file(temp_file_path, file_path)
    except Exception as e:
        handle_error('Could not copy temporary CSV file to final path.', e)


def handle_command_execution_error(message, exception):
    raise CommandExecutionError(
        f'{message} Error message was: {str(exception)}.')


_logger = logging.getLogger()


def log_and_reraise_fatal_exception(exception, action_text, result_text=None):
    
    error = _logger.error
    
    error('{} failed with an exception.'.format(action_text))
    error('The exception message was:')
    error('    {}'.format(str(exception)))
    
    if result_text is not None:
        error(result_text)
        
    raise

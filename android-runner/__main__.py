import argparse
import logging
import time
import os.path as op
import sys
from ExperimentRunner.ExperimentFactory import ExperimentFactory
from ExperimentRunner.util import makedirs
import paths

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = vars(parser.parse_args())

    config_file = op.abspath(args['file'])
    paths.CONFIG_DIR = op.dirname(config_file)
    log_dir = op.join(paths.CONFIG_DIR, 'output/%s/' % time.strftime('%Y.%m.%d_%H%M%S'))
    makedirs(log_dir)
    paths.OUTPUT_DIR = log_dir
    log_filename = op.join(log_dir, 'experiment.log')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_logger = logging.FileHandler(log_filename)
    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
    logger.addHandler(file_logger)

    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setLevel(logging.INFO)
    stdout_logger.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    logger.addHandler(stdout_logger)

    sys.path.append(op.join(paths.ROOT_DIR, 'ExperimentRunner'))

    try:
        experiment = ExperimentFactory.from_json(config_file)
        experiment.start()
    except Exception, e:
        logger.error('%s: %s' % (e.__class__.__name__, e.message))


if __name__ == "__main__":
    main()

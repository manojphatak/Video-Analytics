import unittest
import os
import logging
import logging.config
import yaml

from kafka_client import KafkaImageCli
import video_streamer
from video_consumer import consume_images_from_kafka
from common import get_env

logger = logging.getLogger(__name__)


def setup_logging():
    with open("logging.yml", 'rt') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
    logging.config.dictConfig(config)
    #logging.config.fileConfig("logging.yml")


class TestVideoConsumer(unittest.TestCase):
    def test_detect_known_faces(self):
        setup_logging()
        logger = logging.getLogger("my_module")
        inside_container= os.environ.get("RUN_TESTS_INSIDE_CONTAINER", False)
        logger.debug("Environment variable RUN_TESTS_INSIDE_CONTAINER: {v}".format(v=inside_container))
        if inside_container:
            bootstrap_servers= ['kafka:29092']
        else:
            bootstrap_servers= ['localhost:9092']
        
        videofile= os.environ.get("STREAMER_VIDEOFILE_FOR_TESTS", "")
        kafkatopic= "tests"
        outdir= "/tmp/VideoAnalytics/out"
        facesDir= "/tmp/VideoAnalytics/faces"

        assert os.path.exists(videofile), "file path does not exist! : " + videofile
        assert os.path.exists(outdir), "file path does not exist! : " + outdir
        assert os.path.exists(facesDir), "file path does not exist! : " + facesDir

        video_streamer.stream_video_from_file(videofile, kafkatopic,bootstrap_servers)

        kafkaCli = KafkaImageCli(
            bootstrap_servers=bootstrap_servers,
            topic=kafkatopic,
            stop_iteration_timeout= get_env("KAFKA_CLIENT_BLOCKING_TIMEOUT", 5000, int))


        kafkaCli.register_consumer()
        matched_titles = consume_images_from_kafka(kafkaCli, 
                                                   known_faces_path= facesDir,
                                                   outpath= outdir)
        print(matched_titles)
        #self.assertEqual(
        #    set(['Manoj_direct', 'Manoj_with_beard', 'Manoj_US_Visa']), matched_titles)


if __name__ == "__main__":
    unittest.main()

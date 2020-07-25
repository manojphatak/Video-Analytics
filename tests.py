import unittest

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic
from video_consumer import consume_images_from_kafka


class TestVideoConsumer(unittest.TestCase):
    def test_detect_known_faces(self):
        # todo:  Publish messages

        kafkaCli = KafkaImageCli(
            bootstrap_servers=bootstrap_servers,
            topic=topic,
            stop_iteration_timeout=3000)

        kafkaCli.register_consumer()
        matched_titles = consume_images_from_kafka(kafkaCli, known_faces_path= "/home/manoj/Pictures/known_faces")
        self.assertEqual(
            set(['Manoj_direct', 'Manoj_with_beard', 'Manoj_US_Visa']), matched_titles)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python
import logging
import argparse
import sys

import pixellib
from pixellib.torchbackend.instance import instanceSegmentation

logging.basicConfig(level=logging.INFO)


def detect_video_objects(model, source, output, frames_per_second):
    logging.info(f"🚀 BEGIN detecting objects from {source}...")

    # Instantiate instance segmentation
    ins = instanceSegmentation()

    # Load model
    ins.load_model(model)

    # Segment source video and output to output video
    ins.process_video(
        source,
        show_bboxes=True,
        output_video_name=output,
        frames_per_second=frames_per_second,
    )

    logging.info(f"✅ FINISH saving segmented video to {output}!")


if __name__ == "__main__":

    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write(f"\nerror: {message}\n\n")
            if not isinstance(sys.exc_info()[1], argparse.ArgumentError):
                self.print_help()
            sys.exit(2)

    parser = MyParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # required arguments
    parser.add_argument("source", help="Path to source video")
    parser.add_argument("output", help="Path to output video")

    # optional arguments
    parser.add_argument(
        "--model",
        required=False,
        default="pointrend_resnet50.pkl",
        help="Model with pre-trained weights",
    )
    parser.add_argument(
        "--frames_per_second",
        required=False,
        default=3,
        help="Parameter that sets the number of frames per second for the output video",
    )

    args = parser.parse_args()

    # Run detection
    detect_video_objects(args.model, args.source, args.output, args.frames_per_second)

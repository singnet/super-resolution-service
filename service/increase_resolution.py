from argparse import ArgumentParser
from pprint import pprint
from prosr import Phase
from prosr.data import DataLoader, Dataset
from prosr.logger import info
from prosr.metrics import eval_psnr_and_ssim
from prosr.utils import (get_filenames, IMG_EXTENSIONS, print_evaluation,
                         tensor2im)

import numpy as np
import os
import time
import os.path as osp
import prosr
import skimage.io as io
import torch
import sys
import logging

logging.basicConfig(
    level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s"
)
log = logging.getLogger("super_resolution_service")

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(osp.join(BASE_DIR, 'lib'))


def parse_args():
    parser = ArgumentParser(description='ProSR')
    parser.add_argument(
        '-c', '--checkpoint', type=str, required=True, help='Checkpoint')
    parser.add_argument(
        '-i',
        '--input',
        help=
        'Input images, either list or path to folder. If not given, use bicubically downsampled target image as input',
        type=str,
        nargs='*',
        required=False,
        default=[])
    parser.add_argument(
        '-t',
        '--target',
        help='Target images, either list or path to folder',
        type=str,
        nargs='*',
        required=False,
        default=[])
    parser.add_argument(
        '-s',
        '--scale',
        help='upscale ratio e.g. 2, 4 or 8',
        type=int,
        required=True)
    parser.add_argument(
        '-d',
        '--downscale',
        help='Bicubic downscaling of input to LR',
        action='store_true')
    parser.add_argument(
        '-f', '--fmt', help='Image file format', type=str, default='*')
    parser.add_argument(
        '-o', '--output-dir', help='Output folder.', required=True, type=str)

    parser.add_argument(
        '--cpu', help='Use CPU.', action='store_true')

    input_args = parser.parse_args()

    input_args.input = get_filenames(input_args.input, IMG_EXTENSIONS)
    input_args.target = get_filenames(input_args.target, IMG_EXTENSIONS)

    log.debug("Parsed inputs")

    return input_args


if __name__ == '__main__':
    # Parse command-line arguments
    input_args = parse_args()

    if input_args.cpu:
        log.debug("Using CPU")
        checkpoint = torch.load(input_args.checkpoint, map_location=lambda storage, loc: storage)
    else:
        log.debug("Using GPU!")
        checkpoint = torch.load(input_args.checkpoint)

    cls_model = getattr(prosr.models, checkpoint['class_name'])

    model = cls_model(**checkpoint['params']['G'])
    model.load_state_dict(checkpoint['state_dict'])

    info('phase: {}'.format(Phase.TEST))
    info('checkpoint: {}'.format(osp.basename(input_args.checkpoint)))

    params = checkpoint['params']
    pprint(params)

    model.eval()

    if torch.cuda.is_available() and not input_args.cpu:
        log.debug("Using CUDA!")
        model = model.cuda()

    # TODO Change
    dataset = Dataset(
        Phase.TEST,
        input_args.input,
        input_args.target,
        input_args.scale,
        input_size=None,
        mean=params['train']['dataset']['mean'],
        stddev=params['train']['dataset']['stddev'],
        downscale=input_args.downscale)

    data_loader = DataLoader(dataset, batch_size=1)

    mean = params['train']['dataset']['mean']
    stddev = params['train']['dataset']['stddev']

    if not osp.isdir(input_args.output_dir):
        os.makedirs(input_args.output_dir)
    info('Saving images in: {}'.format(input_args.output_dir))

    with torch.no_grad():
        if len(input_args.target):
            psnr_mean = 0
            ssim_mean = 0
        try:
            for iid, data in enumerate(data_loader):
                log.debug("Performing SR!")
                tic = time.time()
                input = data['input']
                if not input_args.cpu:
                    input = input.cuda()
                output = model(input, input_args.scale).cpu() + data['bicubic']
                sr_img = tensor2im(output, mean, stddev)
                toc = time.time()
                log.debug("Applied image through model!")
                if 'target' in data:
                    hr_img = tensor2im(data['target'], mean, stddev)
                    psnr_val, ssim_val = eval_psnr_and_ssim(
                        sr_img, hr_img, input_args.scale)
                    print_evaluation(
                        osp.basename(data['input_fn'][0]), psnr_val, ssim_val,
                        iid + 1, len(dataset), toc - tic)
                    psnr_mean += psnr_val
                    ssim_mean += ssim_val
                else:
                    print_evaluation(
                        osp.basename(data['input_fn'][0]), np.nan, np.nan, iid + 1,
                        len(dataset), toc - tic)

                fn = osp.join(input_args.output_dir, osp.basename(data['input_fn'][0]))
                log.debug("Saving file under: {}";.format(fn))
                io.imsave(fn, sr_img)
        except Exception as e:
            log.error(e)
            raise

        if len(input_args.target):
            psnr_mean /= len(dataset)
            ssim_mean /= len(dataset)
            print_evaluation("average", psnr_mean, ssim_mean)

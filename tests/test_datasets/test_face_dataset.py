import copy
import tempfile
from unittest.mock import MagicMock

import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from mmpose.datasets import DATASETS


def convert_db_to_output(db):
    outputs = []

    for item in db:
        keypoints = item['joints_3d'].reshape((1, -1, 3))
        center = item['center']
        scale = item['scale']
        box = np.array([
            center[0], center[1], scale[0], scale[1],
            scale[0] * scale[1] * 200 * 200, 1.0
        ],
                       dtype=np.float32).reshape(1, -1)
        img_path = []
        img_path[:0] = item['image_file']
        output = (keypoints, box, img_path, None)
        outputs.append(output)

    return outputs


def test_face_300W_dataset():
    dataset = 'Face300WDataset'
    # test Face 300W datasets
    dataset_class = DATASETS.get(dataset)
    dataset_class.load_annotations = MagicMock()
    dataset_class.coco = MagicMock()

    channel_cfg = dict(
        num_output_channels=68,
        dataset_joints=68,
        dataset_channel=[
            list(range(68)),
        ],
        inference_channel=list(range(68)))

    data_cfg = dict(
        image_size=[256, 256],
        heatmap_size=[64, 64],
        num_output_channels=channel_cfg['num_output_channels'],
        num_joints=channel_cfg['dataset_joints'],
        dataset_channel=channel_cfg['dataset_channel'],
        inference_channel=channel_cfg['inference_channel'])
    # Test
    data_cfg_copy = copy.deepcopy(data_cfg)
    _ = dataset_class(
        ann_file='tests/data/300w/test_300w.json',
        img_prefix='tests/data/300w/',
        data_cfg=data_cfg_copy,
        pipeline=[],
        test_mode=True)

    custom_dataset = dataset_class(
        ann_file='tests/data/300w/test_300w.json',
        img_prefix='tests/data/300w/',
        data_cfg=data_cfg_copy,
        pipeline=[],
        test_mode=False)

    assert custom_dataset.test_mode is False
    assert custom_dataset.num_images == 2
    _ = custom_dataset[0]

    outputs = convert_db_to_output(custom_dataset.db)
    with tempfile.TemporaryDirectory() as tmpdir:
        infos = custom_dataset.evaluate(outputs, tmpdir, ['NME'])
        assert_almost_equal(infos['NME'], 0.0)

        with pytest.raises(KeyError):
            _ = custom_dataset.evaluate(outputs, tmpdir, 'mAP')


def test_face_AFLW_dataset():
    dataset = 'FaceAFLWDataset'
    # test Face AFLW datasets
    dataset_class = DATASETS.get(dataset)
    dataset_class.load_annotations = MagicMock()
    dataset_class.coco = MagicMock()

    channel_cfg = dict(
        num_output_channels=19,
        dataset_joints=19,
        dataset_channel=[
            list(range(19)),
        ],
        inference_channel=list(range(19)))

    data_cfg = dict(
        image_size=[256, 256],
        heatmap_size=[64, 64],
        num_output_channels=channel_cfg['num_output_channels'],
        num_joints=channel_cfg['dataset_joints'],
        dataset_channel=channel_cfg['dataset_channel'],
        inference_channel=channel_cfg['inference_channel'])
    # Test
    data_cfg_copy = copy.deepcopy(data_cfg)
    _ = dataset_class(
        ann_file='tests/data/aflw/test_aflw.json',
        img_prefix='tests/data/aflw/',
        data_cfg=data_cfg_copy,
        pipeline=[],
        test_mode=True)

    custom_dataset = dataset_class(
        ann_file='tests/data/aflw/test_aflw.json',
        img_prefix='tests/data/aflw/',
        data_cfg=data_cfg_copy,
        pipeline=[],
        test_mode=False)

    assert custom_dataset.test_mode is False
    assert custom_dataset.num_images == 2
    _ = custom_dataset[0]

    outputs = convert_db_to_output(custom_dataset.db)
    with tempfile.TemporaryDirectory() as tmpdir:
        infos = custom_dataset.evaluate(outputs, tmpdir, ['NME'])
        assert_almost_equal(infos['NME'], 0.0)

        with pytest.raises(KeyError):
            _ = custom_dataset.evaluate(outputs, tmpdir, 'mAP')


def test_face_WFLW_dataset():
    dataset = 'FaceWFLWDataset'
    # test Face WFLW datasets
    dataset_class = DATASETS.get(dataset)
    dataset_class.load_annotations = MagicMock()
    dataset_class.coco = MagicMock()

    channel_cfg = dict(
        num_output_channels=98,
        dataset_joints=98,
        dataset_channel=[
            list(range(98)),
        ],
        inference_channel=list(range(98)))

    data_cfg = dict(
        image_size=[256, 256],
        heatmap_size=[64, 64],
        num_output_channels=channel_cfg['num_output_channels'],
        num_joints=channel_cfg['dataset_joints'],
        dataset_channel=channel_cfg['dataset_channel'],
        inference_channel=channel_cfg['inference_channel'])
    # Test
    data_cfg_copy = copy.deepcopy(data_cfg)
    _ = dataset_class(
        ann_file='tests/data/wflw/test_wflw.json',
        img_prefix='tests/data/wflw/',
        data_cfg=data_cfg_copy,
        pipeline=[],
        test_mode=True)

    custom_dataset = dataset_class(
        ann_file='tests/data/wflw/test_wflw.json',
        img_prefix='tests/data/wflw/',
        data_cfg=data_cfg_copy,
        pipeline=[],
        test_mode=False)

    assert custom_dataset.test_mode is False
    assert custom_dataset.num_images == 2
    _ = custom_dataset[0]

    outputs = convert_db_to_output(custom_dataset.db)

    with tempfile.TemporaryDirectory() as tmpdir:
        infos = custom_dataset.evaluate(outputs, tmpdir, ['NME'])
        assert_almost_equal(infos['NME'], 0.0)

        with pytest.raises(KeyError):
            _ = custom_dataset.evaluate(outputs, tmpdir, 'mAP')

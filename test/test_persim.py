import pytest

import numpy as np
from persim import PersImage

def test_landscape():
    bds = np.array([[1,1],[1,2]])

    ldsp = PersImage.to_landscape(bds)

    np.testing.assert_array_equal(ldsp, [[1,0],[1,1]])

def test_integer_diagrams():
    """ This test is inspired by gh issue #3 by gh user muszyna25.

    Integer diagrams return nan values.

    This does not work: dgm = [[0, 2], [0, 6], [0, 8]];

    This one works fine: dgm = [[0.0, 2.0], [0.0, 6.0], [0.0, 8.0]];

    """

    dgm = [[0, 2], [0, 6], [0, 8]]
    dgm2 = [[0.0, 2.0], [0.0, 6.0], [0.0, 8.0]]
    pim = PersImage()
    res = pim.transform(dgm2)
    res2 = pim.transform(dgm)

    np.testing.assert_array_equal(res, res2)
    

class TestWeighting:
    def test_zero_on_xaxis(self):
        pim = PersImage()

        wf = pim.weighting()

        assert wf([1,0]) == 0
        assert wf([100,0]) == 0
        assert wf([99, 1.4]) == 1.4

    def test_scales(self):
        pim = PersImage()

        wf = pim.weighting(np.array([[0,1],[1,2],[3,4]]))

        assert wf([1,0]) == 0
        assert wf([1,4]) == 1
        assert wf([1,2]) == .5
    

class TestKernels:
    def test_kernel_mean(self):
        pim = PersImage()
        kf = pim.kernel(2)

        data = np.array([[0,0]])
        assert kf(np.array([[0,0]]), [0,0]) >= kf(np.array([[1,1]]), [0,0]), "decreasing away"
        assert kf(np.array([[0,0]]), [1,1]) == kf(np.array([[1,1]]), [0,0]), "symmetric"


class TestTransforms:
    def test_lists_of_lists(self):
        pim = PersImage(pixels=(3,3))
        diagram = [[0,1], [1,1], [3,5]]
        img = pim.transform(diagram)

        assert img.shape == (3,3)


    def test_n_pixels(self):
        pim = PersImage(pixels=(3,3))
        diagram = np.array([[0,1], [1,1],[3,5]])
        img = pim.transform(diagram)

        assert img.shape == (3,3)

    def test_multiple_diagrams(self):
        pim = PersImage(pixels=(3,3))
        
        diagram1 = np.array([[0,1], [1,1],[3,5]])
        diagram2 = np.array([[0,1], [1,1],[3,6]])
        imgs = pim.transform([diagram1, diagram2])

        assert len(imgs) == 2
        assert imgs[0].shape == imgs[1].shape

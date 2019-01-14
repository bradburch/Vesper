"""Utility functions pertaining to NumPy arrays."""


import numpy as np


def arrays_equal(x, y):
    
    """
    Tests if two arrays have the same shape and values.
    
    Parameters
    ----------
    x : NumPy array
        the first array
    y : NumPy array
        the second array
        
    Returns
    -------
    bool
        `True` if and only if `x` and `y` have the same shape and values.
        Note that two arrays of different dtypes can be equal as long as
        their values are equal.
    """
    
    # We check shapes before calling np.all since np.all broadcasts its
    # arguments as needed but we don't want it to. We want, for example,
    # for np.zeros(1) to *not* equal np.zeros(2).
    
    if x.shape != y.shape:
        return False
    else:
        return np.all(x == y)
    
    
def arrays_close(x, y):
    
    """
    Tests if two arrays have the same shape and close values.
    
    Parameters
    ----------
    x : NumPy array
        the first array
    y : NumPy array
        the second array
        
    Returns
    -------
    bool
        `True` if and only if `x` and `y` have the same shape and close
        values. The closeness of values is tested by calling `np.allclose`.
        Note that two arrays of different dtypes can be close as long as
        their values are close.
    """
    
    # We check shapes before calling np.all since np.all broadcasts its
    # arguments as needed but we don't want it to. We want, for example,
    # for np.zeros(1) to *not* be close to np.zeros(2).
    
    if x.shape != y.shape:
        return False
    else:
        return np.allclose(x, y)
    
    
def find_local_maxima(x, threshold=None):
    
    """
    Finds the local maxima of the specified array.
    
    A local maximum in an array is an element that is greater than its
    neighbors to either side. Note that this means that the first and
    last elements of an array cannot be local maxima, since neither has
    neighbors on both sides. It also means that no element of a sequence
    of equal elements is a local maximum.
    
    Parameters
    ----------
    x : one-dimensional NumPy array
        the array in which to find local maxima.
    threshold : int, float, or None
        the smallest local maximum to find, or `None` to find all local maxima.
        
    Returns
    -------
    NumPy array
        the indices in `x` of all local maxima.
    """
    
    if len(x) < 3:
        # not enough elements for there to be any local maxima
        
        return np.array([], dtype='int32')
    
    else:
        # have enough elements for there to be local maxima
        
        x0 = x[:-2]
        x1 = x[1:-1]
        x2 = x[2:]
        
        indices = np.where((x0 < x1) & (x1 > x2))[0] + 1
        
        if threshold is not None:
            maxima = x[indices]
            keep_indices = np.where(maxima >= threshold)
            indices = indices[keep_indices]
            
        return indices
        
        
def find(x, y, tolerance=0):
    
    """
    Finds all occurrences of one one-dimensional array in another.
    
    The algorithm employed by this function is efficient when there are
    few occurrences of a small prefix of the first array in the second.
    It is inefficient in other cases.
    
    Parameters
    ----------
    x : one-dimensional NumPy array
        the array to be searched for.
    y : one-dimensional NumPy array
        the array to be searched in.
            
    Returns
    -------
    NumPy array
        the starting indices of all occurrences of `x` in `y`.
    """

    m = len(x)
    n = len(y)
    
    if m == 0:
        return np.arange(n)
    
    else:
        # x has at least one element
        
        # Find indices i of x[0] in y[:n - m + 1]. These are the indices in y
        # where matches of x might start.
        diffs = np.abs(y[:n - m + 1] - x[0])
        i = np.where(diffs <= tolerance)[0]
        
        for k in range(1, m):
            # loop invariant: matches of x[:k] start at indices i in y
            
            if len(i) <= 1:
                # zero or one matches of x[:k] in y
                break
            
            # Find indices j of x[k] in y[i + k]. These are the indices
            # in i of the indices in y where matches of x[:k + 1] start. 
            diffs = np.abs(y[i + k] - x[k])
            j = np.where(diffs <= tolerance)[0]
            
            i = i[j]
        
        if len(i) == 1:
            # might have looked for only initial portion of x
            
            p = i[0]
            diffs = np.abs(y[p:p + m] - x)
            if np.all(diffs <= tolerance):
                return i
            else:
                return np.array([], dtype='int64')
        
        else:
            # i is the answer
            
            return i


def reproducible_choice(x, size=None, replace=True, p=None):
    
    """
    Like NumPy's `random.choice`, but always returns the same thing for
    the same arguments.
    """
    
    return _rs().choice(x, size, replace, p)


def _rs():
    return np.random.RandomState(seed=1)


def reproducible_permutation(x):
    
    """
    Like NumPy's `random.permutation`, but always returns the same thing
    for a given argument.
    """
    
    return _rs().permutation(x)


def reproducible_shuffle(x):
    
    """
    Like NumPy's `random.shuffle`, but always has the same effect on a
    given argument.
    """
    
    _rs().shuffle(x)

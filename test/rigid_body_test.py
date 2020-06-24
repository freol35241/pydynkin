import pytest
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal

from dynkin import RigidBody, Frame

def test_constructor():
    
    with pytest.raises(AssertionError):
        RigidBody(mass=-1)
        
    with pytest.raises(AssertionError):
        RigidBody(mass=1, gyradius=-1)
        
    with pytest.raises(AssertionError):
        RigidBody(mass=1, gyradius=[-1, 1, 1])
        
def test_cog():
    rb = RigidBody(mass=1, gyradius=[1, 1, 1], cog=[-1, 1, 3])
    
    assert_almost_equal(
        [-1, 1, 3],
        rb.CoG.position
    )

def test_generalized_coordinates():
    rb = RigidBody(mass=1, gyradius=[1, 1, 1])
    rb.set_position([1,2,3])
    rb.set_attitude([0, 1, 1])
    pose = rb.generalized_coordinates()
    assert_equal(
        [1, 2, 3, 0, 1, 1],
        pose
    )
    
def test_generalized_velocities():
    rb = RigidBody(mass=1, gyradius=[1, 1, 1])
    rb.set_position([1, 1, 1])
    rb.set_attitude([90, 0, 90], degrees=True)
    rb.set_linear_velocity([1, 2, 3])
    rb.set_angular_velocity([0, 0, 1])
    vel = rb.generalized_velocities()
    assert_almost_equal(
        [3, 1, 2, 0, -1, 0],
        vel
    )

def test_coriolis_centripetal_acceleration_cog_offset():
    rb = RigidBody(mass=1, gyradius=[1,1,1], cog=[1, 0, 0])
    rb.set_angular_velocity([0,0,1])
    assert_equal(
        [1, 0, 0, 0, 0, 0], 
        rb.acceleration([0, 0, 0, 0, 0, 0])
    )
    
def test_coriolis_centripetal_acceleration_linear_velocity():
    rb = RigidBody(mass=1, gyradius=[1, 1, 1])
    rb.set_angular_velocity([0, 0, 1])
    rb.set_linear_velocity([1, 0, 0])
    assert_equal(
        [0, -1, 0, 0, 0, 0], 
        rb.acceleration([0, 0, 0, 0, 0, 0])
    )
    
def test_acceleration_wrench():
    rb = RigidBody(mass=1, gyradius=[1, 1, 1])
    wrench = np.ones(6)
    a = rb.acceleration(wrench)
    
    assert_almost_equal(
        a,
        np.ones(6)
    )
    
    rb = RigidBody(mass=1, gyradius=[1, 1, 1], cog=[1, 0, 0])
    wrench = np.ones(6)
    a = rb.acceleration(wrench)
    
    assert_almost_equal(
        a,
        [1, 1, 3, 1, 2, 0]
    )
    
def test_wrench_acceleration():
    rb = RigidBody(mass=1, gyradius=[1, 1, 1])
    a = np.ones(6)
    wrench = rb.wrench(a)
    
    assert_almost_equal(
        wrench,
        np.ones(6)
    )
    
    rb = RigidBody(mass=1, gyradius=[1, 1, 1], cog=[1, 0, 0])
    a = np.ones(6)
    wrench = rb.wrench(a)
    
    assert_almost_equal(
        wrench,
        [1, 2, 0, 1, 1, 3]
    )
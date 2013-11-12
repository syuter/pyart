""" Unit Tests for Py-ART's io/nexrad_cdm.py module. """

import bz2
import tempfile
import os

import numpy as np
from numpy.ma.core import MaskedArray

import pyart

###################################################
# read_nexrad_cdm tests (verify radar attributes) #
###################################################

# read in the sample file and create the radar objects
# We need to decompress the bz2 file for this making a tempfile
tmpfile = tempfile.mkstemp(suffix='.nc', dir='.')[1]
f = open(tmpfile, 'wb')
f.write(bz2.BZ2File(pyart.testing.NEXRAD_CDM_FILE).read())
f.close()
radar = pyart.io.read_nexrad_cdm(tmpfile)
os.remove(tmpfile)


# time attribute
def test_time():
    assert 'comment' in radar.time.keys()
    assert 'long_name' in radar.time.keys()
    assert 'standard_name' in radar.time.keys()
    assert 'units' in radar.time.keys()
    assert 'calendar' in radar.time.keys()
    assert 'data' in radar.time.keys()
    assert radar.time['units'] == 'seconds since 2013-07-17T19:50:21Z'
    assert radar.time['data'].shape == (7200, )
    assert round(radar.time['data'][1], 3) == 0.677


# range attribute
def test_range():
    assert 'long_name' in radar.range
    assert 'standard_name' in radar.range
    assert 'meters_to_center_of_first_gate' in radar.range
    assert 'meters_between_gates' in radar.range
    assert 'units' in radar.range
    assert 'data' in radar.range
    assert 'spacing_is_constant' in radar.range
    assert radar.range['data'].shape == (1832, )
    assert round(radar.range['data'][1]) == 2375.


# fields attribute is tested later


# metadata attribute
def test_metadata():
    assert 'instrument_name' in radar.metadata
    assert 'source' in radar.metadata


# scan_type attribute
def test_scan_type():
    assert radar.scan_type == 'ppi'


# latitude attribute
def test_latitude():
    assert 'data' in radar.latitude
    assert 'standard_name' in radar.latitude
    assert 'units' in radar.latitude
    assert radar.latitude['data'].shape == (1, )
    assert round(radar.latitude['data']) == 48.0


# longitude attribute
def test_longitude():
    assert 'data' in radar.longitude
    assert 'standard_name' in radar.longitude
    assert 'units' in radar.longitude
    assert radar.longitude['data'].shape == (1, )
    assert round(radar.longitude['data']) == -122.0


# altitude attribute
def test_altitude():
    assert 'data' in radar.altitude
    assert 'standard_name' in radar.altitude
    assert 'units' in radar.altitude
    assert 'positive' in radar.altitude
    assert radar.altitude['data'].shape == (1, )
    assert round(radar.altitude['data']) == 151.0   # 10 m different


# altitude_agl attribute
def test_altitude_agl():
    assert radar.altitude_agl is None


# sweep_number attribute
def test_sweep_number():
    assert 'standard_name' in radar.sweep_number
    assert np.all(radar.sweep_number['data'] == range(16))


# sweep_mode attribute
def test_sweep_mode():
    assert 'standard_name' in radar.sweep_mode
    assert radar.sweep_mode['data'].shape == (16, )
    assert np.all(radar.sweep_mode['data'] == ['azimuth_surveillance'])


# fixed_angle attribute
def test_fixed_angle():
    assert 'standard_name' in radar.fixed_angle
    assert 'units' in radar.fixed_angle
    assert radar.fixed_angle['data'].shape == (16, )
    assert round(radar.fixed_angle['data'][0], 2) == 0.53


# sweep_start_ray_index attribute
def test_sweep_start_ray_index():
    assert 'long_name' in radar.sweep_start_ray_index
    assert radar.sweep_start_ray_index['data'].shape == (16, )
    assert round(radar.sweep_start_ray_index['data'][0]) == 0.0


# sweep_end_ray_index attribute
def test_sweep_end_ray_index():
    assert 'long_name' in radar.sweep_end_ray_index
    assert radar.sweep_end_ray_index['data'].shape == (16, )
    assert round(radar.sweep_end_ray_index['data'][0]) == 719.0


# target_scan_rate attribute
def test_target_scan_rate():
    assert radar.target_scan_rate is None


# azimuth attribute
def test_azimuth():
    assert 'standard_name' in radar.azimuth
    assert 'long_name' in radar.azimuth
    assert 'units' in radar.azimuth
    assert 'axis' in radar.azimuth
    assert round(radar.azimuth['data'][0]) == 350.0
    assert round(radar.azimuth['data'][10]) == 355.0


# elevation attribute
def test_elevation():
    assert 'standard_name' in radar.elevation
    assert 'long_name' in radar.azimuth
    assert 'units' in radar.elevation
    assert 'axis' in radar.elevation
    assert radar.elevation['data'].shape == (7200, )
    assert round(radar.elevation['data'][0], 2) == 0.75


# scan_rate attribute
def test_scan_rate():
    assert radar.scan_rate is None


# antenna_transition attribute
def test_antenna_transition():
    assert radar.antenna_transition is None


# instrument_parameters attribute
def test_instument_parameters():
    assert radar.instrument_parameters is None


# radar_calibration attribute
def test_radar_calibration():
    assert radar.radar_calibration is None


# ngates attribute
def test_ngates():
    assert radar.ngates == 1832


# nrays attribute
def test_nrays():
    assert radar.nrays == 7200


# nsweeps attribute
def test_nsweeps():
    assert radar.nsweeps == 16


####################
# fields attribute #
####################


def test_field_dics():
    fields = ['differential_phase', 'spectrum_width',
              'correlation_coefficient', 'reflectivity',
              'differential_reflectivity', 'velocity']
    for field in fields:
        description = "field : %s, dictionary" % field
        check_field_dic.description = description
        yield check_field_dic, field


def check_field_dic(field):
    """ Check that the required keys are present in a field dictionary. """
    assert 'standard_name' in radar.fields[field]
    assert 'units' in radar.fields[field]
    assert '_FillValue' in radar.fields[field]
    assert 'coordinates' in radar.fields[field]


def test_field_shapes():
    fields = ['differential_phase', 'spectrum_width',
              'correlation_coefficient', 'reflectivity',
              'differential_reflectivity', 'velocity']
    for field in fields:
        description = "field : %s, shape" % field
        check_field_shape.description = description
        yield check_field_shape, field


def check_field_shape(field):
    assert radar.fields[field]['data'].shape == (7200, 1832)


def test_field_types():
    fields = {
        'differential_phase': MaskedArray,
        'spectrum_width': MaskedArray,
        'correlation_coefficient': MaskedArray,
        'reflectivity': MaskedArray,
        'differential_reflectivity': MaskedArray,
        'velocity': MaskedArray}
    for field, field_type in fields.iteritems():
        description = "field : %s, type" % field
        check_field_type.description = description
        yield check_field_type, field, field_type


def check_field_type(field, field_type):
    assert type(radar.fields[field]['data']) is field_type


def test_field_first_points():
    # these values can be found using:
    # [round(radar.fields[f]['data'][0,0]) for f in radar.fields]
    fields = {'differential_phase': 181.0,
              'spectrum_width': np.ma.masked,
              'correlation_coefficient': 0.0,
              'reflectivity': -32.0,
              'differential_reflectivity': -8.0,
              'velocity': np.ma.masked}
    for field, field_value in fields.iteritems():
        description = "field : %s, first point" % field
        check_field_first_point.description = description
        yield check_field_first_point, field, field_value


def check_field_first_point(field, value):
    if np.ma.is_masked(value):
        assert np.ma.is_masked(radar.fields[field]['data'][0, 0])
    else:
        assert round(radar.fields[field]['data'][0, 0]) == value